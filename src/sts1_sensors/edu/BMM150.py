import ctypes
from enum import IntEnum
import math
import os
import time
from typing import Tuple

from sts1_sensors.utils.AbstractSensor import AbstractSensor

class PowerMode(IntEnum):
    """
    BMM150 power modes
    """
    NORMAL = 0x00
    FORCED = 0x01
    SLEEP = 0x03
    SUSPEND = 0x04

class PresetMode(IntEnum):
    """
    BMM150 preset modes
    """
    LOWPOWER = 0x01
    REGULAR = 0x02
    HIGHACCURACY = 0x03
    ENHANCED = 0x04

class PowerControl(IntEnum):
    """
    BMM150 power control modes
    """
    DISABLE = 0x00
    ENABLE = 0x01

class bmm150_mag_data:
    x: int = 0
    y: int = 0
    z: int = 0

# /*
#     @brief bmm150 un-compensated (raw) magnetometer data
# */
class bmm150_raw_mag_data:
    # /*! Raw mag X data */
    raw_datax: int = 0
    # /*! Raw mag Y data */
    raw_datay: int = 0
    # /*! Raw mag Z data */
    raw_dataz: int = 0
    # /*! Raw mag resistance value */
    raw_data_r: int = 0


# /*!
#     @brief bmm150 trim data structure
# */
class bmm150_trim_registers:
    # /*! trim x1 data */
    dig_x1: int = 0
    # /*! trim y1 data */
    dig_y1: int = 0
    # /*! trim x2 data */
    dig_x2: int = 0
    # /*! trim y2 data */
    dig_y2: int = 0
    # /*! trim z1 data */
    dig_z1: int = 0
    # /*! trim z2 data */
    dig_z2: int = 0
    # /*! trim z3 data */
    dig_z3: int = 0
    # /*! trim z4 data */
    dig_z4: int = 0
    # /*! trim xy1 data */
    dig_xy1: int = 0
    # /*! trim xy2 data */
    dig_xy2: int = 0
    # /*! trim xyz1 data */
    dig_xyz1: int = 0

# /**
#     @brief bmm150 sensor settings
# */
class bmm150_settings:
    # /*! Control measurement of XYZ axes */
    xyz_axes_control: int = 0
    # /*! Power control bit value */
    pwr_cntrl_bit: int = 0
    # /*! Power control bit value */
    pwr_mode: int = 0
    # /*! Data rate value (ODR) */
    data_rate: int = 0
    # /*! XY Repetitions */
    xy_rep: int = 0
    # /*! Z Repetitions */
    z_rep: int = 0
    # /*! Preset mode of sensor */
    preset_mode: int = 0
    # /*! Interrupt configuration settings */
    # // struct bmm150_int_ctrl_settings int_settings: int


class BMM150(AbstractSensor):
    """Geomagnetic sensor.
    """
    START_UP_TIME_MS = 3
    POWER_CONTROL_ADDR = 0x4B
    OP_MODE_ADDR = 0x4C
    OVERFLOW_OUTPUT = -32768

    def __init__(self, preset_mode=1, address=None, bus=None):
        """Geomagnetic sensor.

        Builds on top of the library `bmm150 <https://gitlab.com/umoreau/bmm150>`_. by Ulysse Moreau.

        :param int preset_mode: Integer, either 1 (Low Power), 2 (Regular), 3 (High Accuracy) or 4 (Enhanced). Defaults to 1.
        :param hexadecimal address: Physical address of the sensor on the board (see `i2cdetect` command). Allowed values: `[0x10, 0x11, 0x12, 0x13]`. If None, the environment variable `STS1_SENSOR_ADDRESS_BMM150` will be used. If environment variable is not found, 0x10 will be used.
        :param SMBus bus: A SMBus object. If None, this class will generate its own, defaults to None.
        
        Example:

        .. code-block:: python

           mag = BMM150()
           x, y, z = mag.get_magnetic_data()
           print(f"{x=:.2f} µT, {y=:.2f} µT, {z=:.2f} µT")
           print(f"Heading: {mag.get_heading():.2f}°")
        """
        super().__init__(possible_addresses=[0x10, 0x11, 0x12, 0x13], bus=bus)
        
        self.address = address or int(os.environ.get("STS1_SENSOR_ADDRESS_BMM150", "0x10"), 16)
    
        for p in PresetMode:
            if preset_mode == p.value:
                self.presetmode = p
                break
        else:   
            raise ValueError(f"preset_mode has to be between 1 and 4, but was {preset_mode}")

        self.settings = bmm150_settings()
        self.raw_mag_data = bmm150_raw_mag_data()
        self.mag_data = bmm150_mag_data()
        self.trim_data = bmm150_trim_registers()

        # Power up the sensor from suspend to sleep mode
        self.set_op_mode(PowerMode.SLEEP)
        time.sleep(self.START_UP_TIME_MS / 1000.0)

        CHIP_ID = 0x32
        CHIP_ID_ADDR = 0x40

        chip_id = self.bus.read_byte_data(self.address, CHIP_ID_ADDR)
        if chip_id != CHIP_ID:
            raise ValueError("The chip ID was not conform. Are you sure you are trying to interface with a bmm150?")

        # Function to update trim values
        self.read_trim_registers()

        # Setting the power mode as normal
        self.set_op_mode(PowerMode.NORMAL)

        #  Setting the preset mode as Low power mode
        #    i.e. data rate = 10Hz XY-rep = 1 Z-rep = 2
        self.set_presetmode(self.presetmode)

        # Wait up to 10 secs for sensor to be ready
        for _ in range(20):
            if self.bus.read_byte_data(self.address, 0x48) & 1 == 1:
                break
            time.sleep(0.5)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        if address not in self.possible_addresses:
            s = f"The address {hex(address)} does not exist."
            s += f" Choose one of {self.possible_addresses}."
            raise ValueError(s)
        self._address = address
        
    def set_bits_pos0(self, reg_data, bitname_mask, data):
        return (reg_data & ~(bitname_mask)) | (data & bitname_mask)

    def get_bits(self, reg_data, bitname_mask, bitname_pos):
        return (reg_data & (bitname_mask)) >> (bitname_pos)

    def set_bits(self, reg_data, bitname_mask, bitname_pos, data):
        return (reg_data & ~(bitname_mask)) | ((data << bitname_pos) & bitname_mask)

    def set_op_mode(self, pwr_mode: PowerMode) -> None:
        """Sets power mode

        Args:
            pwr_mode (PowerMode): Desired power mode
        """
        # Select the power mode to set
        if pwr_mode == PowerMode.NORMAL:
            #  If the sensor is in suspend mode put the device to sleep mode
            self.suspend_to_sleep_mode()
            self._write_op_mode(pwr_mode)
        elif pwr_mode == PowerMode.FORCED:
            #  If the sensor is in suspend mode put the device to sleep mode
            self.suspend_to_sleep_mode()
            self._write_op_mode(pwr_mode)
        elif pwr_mode == PowerMode.SLEEP:
            #  If the sensor is in suspend mode put the device to sleep mode
            self.suspend_to_sleep_mode()
            self._write_op_mode(pwr_mode)
        elif pwr_mode == PowerMode.SUSPEND:
            # Set the power control bit to zero
            self._set_power_control_bit(PowerControl.DISABLE)

    def set_presetmode(self, preset_mode: PresetMode):
        """Sets preset mode

        Args:
            preset_mode (PresetMode): Desired preset mode
        """
        RATE_10HZ = 0x00
        RATE_02HZ = 0x01
        RATE_06HZ = 0x02
        RATE_08HZ = 0x03
        RATE_15HZ = 0x04
        RATE_20HZ = 0x05
        RATE_25HZ = 0x06
        RATE_30HZ = 0x07

        LOWPOWER_REPXY = 1
        REGULAR_REPXY = 4
        ENHANCED_REPXY = 7
        HIGHACCURACY_REPXY = 23

        LOWPOWER_REPZ = 2
        REGULAR_REPZ = 14
        ENHANCED_REPZ = 26
        HIGHACCURACY_REPZ = 82

        if preset_mode == PresetMode.LOWPOWER:
            #  Set the data rate x,y,z repetition for Low Power mode
            self.settings.data_rate = RATE_10HZ
            self.settings.xy_rep = LOWPOWER_REPXY
            self.settings.z_rep = LOWPOWER_REPZ
            self._set_odr_xyz_rep()
        elif preset_mode == PresetMode.REGULAR:
            #  Set the data rate x,y,z repetition for Regular mode
            self.settings.data_rate = RATE_10HZ
            self.settings.xy_rep = REGULAR_REPXY
            self.settings.z_rep = REGULAR_REPZ
            self._set_odr_xyz_rep()
        elif preset_mode == PresetMode.HIGHACCURACY:
            #  Set the data rate x,y,z repetition for High Accuracy mode
            self.settings.data_rate = RATE_20HZ
            self.settings.xy_rep = HIGHACCURACY_REPXY
            self.settings.z_rep = HIGHACCURACY_REPZ
            self._set_odr_xyz_rep()
        elif preset_mode == PresetMode.ENHANCED:
            #  Set the data rate x,y,z repetition for Enhanced Accuracy mode
            self.settings.data_rate = RATE_10HZ
            self.settings.xy_rep = ENHANCED_REPXY
            self.settings.z_rep = ENHANCED_REPZ
            self._set_odr_xyz_rep()

    def suspend_to_sleep_mode(self):
        self._set_power_control_bit(PowerControl.ENABLE)
        # Start-up time delay of 3ms
        time.sleep(self.START_UP_TIME_MS / 1000.0)

    def _write_op_mode(self, op_mode: PowerMode):
        """Writes chosen power mode to I²C register.

        Args:
            op_mode (PowerMode): Chosen power mode
        """
        OP_MODE_MSK = 0x06
        OP_MODE_POS = 0x01

        reg_data = self.bus.read_byte_data(self.address, self.OP_MODE_ADDR)
        # Set the op_mode value in Opmode bits of 0x4C
        reg_data = self.set_bits(reg_data, OP_MODE_MSK, OP_MODE_POS, op_mode)
        self.bus.write_byte_data(self.address, self.OP_MODE_ADDR, reg_data)

    def _set_power_control_bit(self, pwrcntrl_bit: PowerControl):
        """Enables or disables the power bit.

        Args:
            pwrcntrl_bit (PowerControl): _description_
        """
        PWR_CNTRL_MSK = 0x01

        # Power control register 0x4B is read
        reg_data = self.bus.read_byte_data(self.address, self.POWER_CONTROL_ADDR)
        # Sets the value of power control bit
        reg_data = self.set_bits_pos0(reg_data, PWR_CNTRL_MSK, pwrcntrl_bit)
        self.bus.write_byte_data(self.address, self.POWER_CONTROL_ADDR, reg_data)

    def _set_odr_xyz_rep(self):
        REP_XY_ADDR = 0x51
        REP_Z_ADDR = 0x52

        # Set the ODR
        self._set_odr()
        # Set the XY-repetitions number
        self.bus.write_byte_data(self.address, REP_XY_ADDR, self.settings.xy_rep)
        # Set the Z-repetitions number
        self.bus.write_byte_data(self.address, REP_Z_ADDR, self.settings.z_rep)

    def _set_odr(self):
        ODR_MSK = 0x38
        ODR_POS = 0x03

        reg_data = self.bus.read_byte_data(self.address, self.OP_MODE_ADDR)
        # Set the ODR value
        reg_data = self.set_bits(reg_data, ODR_MSK, ODR_POS, self.settings.data_rate)
        self.bus.write_byte_data(self.address, self.OP_MODE_ADDR, reg_data)

    def soft_reset(self):
        """
        Soft resets the module.
        """
        SOFT_RESET_DELAY_MS = 1
        SET_SOFT_RESET = 0x82

        reg_data = self.bus.read_byte_data(self.address, self.POWER_CONTROL_ADDR)
        reg_data = reg_data | SET_SOFT_RESET
        self.bus.write_byte_data(self.address, self.POWER_CONTROL_ADDR, reg_data)
        time.sleep(SOFT_RESET_DELAY_MS / 1000.0)

    def read_trim_registers(self):
        """
        Reads the trim registers for calibration.
        """
        DIG_X1 = 0x5D
        DIG_Z4_LSB = 0x62
        DIG_Z2_LSB = 0x68

        trim_x1y1 = self.bus.read_i2c_block_data(self.address, DIG_X1, 2)
        trim_xyz_data = self.bus.read_i2c_block_data(self.address, DIG_Z4_LSB, 4)
        trim_xy1xy2 = self.bus.read_i2c_block_data(self.address, DIG_Z2_LSB, 10)

        #  Trim data which is read is updated
        #    in the device structure
        self.trim_data.dig_x1 = trim_x1y1[0]
        self.trim_data.dig_y1 = trim_x1y1[1]

        self.trim_data.dig_x2 = trim_xyz_data[2]
        self.trim_data.dig_y2 = trim_xyz_data[3]

        temp_msb = trim_xy1xy2[3] << 8
        self.trim_data.dig_z1 = temp_msb | trim_xy1xy2[2]

        temp_msb = trim_xy1xy2[1] << 8
        self.trim_data.dig_z2 = temp_msb | trim_xy1xy2[0]

        temp_msb = trim_xy1xy2[7] << 8
        self.trim_data.dig_z3 = temp_msb | trim_xy1xy2[6]

        temp_msb = trim_xyz_data[1] << 8
        self.trim_data.dig_z4 = temp_msb | trim_xyz_data[0]

        self.trim_data.dig_xy1 = trim_xy1xy2[9]
        self.trim_data.dig_xy2 = trim_xy1xy2[8]

        temp_msb = trim_xy1xy2[5] & 0x7F << 8
        self.trim_data.dig_xyz1 = temp_msb | trim_xy1xy2[4]

    def read_raw_mag_data(self) -> Tuple[int, int, int, int]:
        """Reads registers containing X, Y, Z and R data from the device.

        Returns:
            tuple[int, int, int, int]: A tuple containing raw (X, Y, Z, R) data.
        """
        DATA_X_LSB = 0x42
        XYZR_DATA_LEN = 8

        DATA_X_MSK = 0xF8
        DATA_X_POS = 0x03
        DATA_Y_MSK = 0xF8
        DATA_Y_POS = 0x03
        DATA_Z_MSK = 0xFE
        DATA_Z_POS = 0x01

        DATA_RHALL_MSK = 0xFC
        DATA_RHALL_POS = 0x02

        reg_data = self.bus.read_i2c_block_data(self.address, DATA_X_LSB, XYZR_DATA_LEN)

        # Mag X axis data
        reg_data[0] = self.get_bits(reg_data[0], DATA_X_MSK, DATA_X_POS)
        # Convert to a c-type int8, to add a twos-complement awareness
        reg_data[1] = ctypes.c_int8(reg_data[1]).value
        # Shift the MSB data to left by 5 bits
        # Multiply by 32 to get the shift left by 5 value
        msb_data = reg_data[1] * 32
        # Raw mag X axis data
        self.raw_mag_data.raw_datax = msb_data | reg_data[0]

        # Mag Y axis data
        reg_data[2] = self.get_bits(reg_data[2], DATA_Y_MSK, DATA_Y_POS)
        # Convert to a c-type int8, to add a twos-complement awareness
        reg_data[3] = ctypes.c_int8(reg_data[3]).value
        # Shift the MSB data to left by 5 bits
        # Multiply by 32 to get the shift left by 5 value
        msb_data = reg_data[3] * 32
        # Raw mag Y axis data
        self.raw_mag_data.raw_datay = msb_data | reg_data[2]

        # Mag Z axis data
        reg_data[4] = self.get_bits(reg_data[4], DATA_Z_MSK, DATA_Z_POS)
        # Convert to a c-type int8, to add a twos-complement awareness
        reg_data[5] = ctypes.c_int8(reg_data[5]).value
        # Shift the MSB data to left by 7 bits
        # Multiply by 128 to get the shift left by 7 value
        msb_data = reg_data[5] * 128
        # Raw mag Z axis data
        self.raw_mag_data.raw_dataz = msb_data | reg_data[4]

        # Mag R-HALL data
        # R-hall is always unsigned, no need for twos-complement awareness
        reg_data[6] = self.get_bits(reg_data[6], DATA_RHALL_MSK, DATA_RHALL_POS)
        self.raw_mag_data.raw_data_r = reg_data[7] << 6 | reg_data[6]

        return (
            self.raw_mag_data.raw_datax,
            self.raw_mag_data.raw_datay,
            self.raw_mag_data.raw_dataz,
            self.raw_mag_data.raw_data_r,
        )

    def read_mag_data(self) -> Tuple[int, int, int]:
        """Reads and compensate the magnetic values for X, Y and Z.

        Returns:
            tuple[int, int, int]: A tuple containing raw (X, Y, Z) compensated data.
        """

        self.read_raw_mag_data()

        # Compensated Mag X data in floating point format
        self.mag_data.x = self._compensate_x(
            self.raw_mag_data.raw_datax, self.raw_mag_data.raw_data_r
        )
        # Compensated Mag Y data in floating point format
        self.mag_data.y = self._compensate_y(
            self.raw_mag_data.raw_datay, self.raw_mag_data.raw_data_r
        )
        # Compensated Mag Z data in floating point format
        self.mag_data.z = self._compensate_z(
            self.raw_mag_data.raw_dataz, self.raw_mag_data.raw_data_r
        )

        return self.mag_data.x, self.mag_data.y, self.mag_data.z

    def _compensate_x(self, mag_data_x, data_rhall):
        """This internal API is used to obtain the compensated
        magnetometer X axis data(micro-tesla) in floating point.
        """
        XYAXES_FLIP_OVERFLOW_ADCVAL = -4096

        # /* Overflow condition check */
        if (
            (mag_data_x != XYAXES_FLIP_OVERFLOW_ADCVAL)
            and (data_rhall != 0)
            and (self.trim_data.dig_xyz1 != 0)
        ):
            # /* Processing compensation equations */
            process_comp_x0 = (self.trim_data.dig_xyz1) * 16384.0 / data_rhall
            retval = process_comp_x0 - 16384.0
            process_comp_x1 = (self.trim_data.dig_xy2) * (retval * retval / 268435456.0)
            process_comp_x2 = (
                process_comp_x1 + retval * (self.trim_data.dig_xy1) / 16384.0
            )
            process_comp_x3 = (self.trim_data.dig_x2) + 160.0
            process_comp_x4 = mag_data_x * ((process_comp_x2 + 256.0) * process_comp_x3)
            retval = (
                (process_comp_x4 / 8192.0) + ((self.trim_data.dig_x1) * 8.0)
            ) / 16.0
        else:
            # /* Overflow, set output to 0.0 */
            retval = self.OVERFLOW_OUTPUT

        return retval

    def _compensate_y(self, mag_data_y, data_rhall):
        """This internal API is used to obtain the compensated
        magnetometer Y axis data(micro-tesla) in floating point.
        """
        XYAXES_FLIP_OVERFLOW_ADCVAL = -4096
        
        # /* Overflow condition check */
        if (
            (mag_data_y != XYAXES_FLIP_OVERFLOW_ADCVAL)
            and (data_rhall != 0)
            and (self.trim_data.dig_xyz1 != 0)
        ):
            # /* Processing compensation equations */
            process_comp_y0 = (self.trim_data.dig_xyz1) * 16384.0 / data_rhall
            retval = process_comp_y0 - 16384.0
            process_comp_y1 = (self.trim_data.dig_xy2) * (retval * retval / 268435456.0)
            process_comp_y2 = (
                process_comp_y1 + retval * (self.trim_data.dig_xy1) / 16384.0
            )
            process_comp_y3 = (self.trim_data.dig_y2) + 160.0
            process_comp_y4 = mag_data_y * (
                ((process_comp_y2) + 256.0) * process_comp_y3
            )
            retval = (
                (process_comp_y4 / 8192.0) + ((self.trim_data.dig_y1) * 8.0)
            ) / 16.0
        else:
            # /* Overflow, set output to 0.0 */
            retval = self.OVERFLOW_OUTPUT

        return retval

    def _compensate_z(self, mag_data_z, data_rhall):
        """This internal API is used to obtain the compensated
        magnetometer Z axis data(micro-tesla) in floating point.
        """
        ZAXIS_HALL_OVERFLOW_ADCVAL = -16384
        
        # /* Overflow condition check */
        if (
            (mag_data_z != ZAXIS_HALL_OVERFLOW_ADCVAL)
            and (self.trim_data.dig_z2 != 0)
            and (self.trim_data.dig_z1 != 0)
            and (self.trim_data.dig_xyz1 != 0)
            and (data_rhall != 0)
        ):
            #  /* Processing compensation equations */
            process_comp_z0 = (mag_data_z) - (self.trim_data.dig_z4)
            process_comp_z1 = (data_rhall) - (self.trim_data.dig_xyz1)
            process_comp_z2 = (self.trim_data.dig_z3) * process_comp_z1
            process_comp_z3 = (self.trim_data.dig_z1) * (data_rhall) / 32768.0
            process_comp_z4 = (self.trim_data.dig_z2) + process_comp_z3
            process_comp_z5 = (process_comp_z0 * 131072.0) - process_comp_z2
            retval = (process_comp_z5 / ((process_comp_z4) * 4.0)) / 16.0
        else:
            # /* Overflow, set output to 0.0 */
            retval = self.OVERFLOW_OUTPUT

        return retval

    def get_raw_magnetic_data(self):
        """Get raw magnetic data in µT.
        """
        return self.read_raw_mag_data()

    def get_magnetic_data(self):
        """Get magnetic data in µT.
        """
        return self.read_mag_data()
    
    def get_heading(self):
        """Get heading direction in degrees. Uses only x and y for calculation (z is ignored).
        """
        x, y, _ = self.get_magnetic_data()
        return math.degrees(math.atan2(x, y))
