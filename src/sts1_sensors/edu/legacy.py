from enum import IntEnum

# /**\name Macro definitions */

# /**\name API success code */
BMM150_OK = 0

# /**\name API error codes */
BMM150_E_ID_NOT_CONFORM = -1
BMM150_E_INVALID_CONFIG = -2
BMM150_E_ID_WRONG = -3

# /**\name API warning codes */
BMM150_W_NORMAL_SELF_TEST_YZ_FAIL = 1
BMM150_W_NORMAL_SELF_TEST_XZ_FAIL = 2
BMM150_W_NORMAL_SELF_TEST_Z_FAIL = 3
BMM150_W_NORMAL_SELF_TEST_XY_FAIL = 4
BMM150_W_NORMAL_SELF_TEST_Y_FAIL = 5
BMM150_W_NORMAL_SELF_TEST_X_FAIL = 6
BMM150_W_NORMAL_SELF_TEST_XYZ_FAIL = 7
BMM150_W_ADV_SELF_TEST_FAIL = 8

BMM150_I2C_Address = 0x13

# /**\name CHIP ID & SOFT RESET VALUES      */
BMM150_CHIP_ID = 0x32
BMM150_SET_SOFT_RESET = 0x82


# /**\name POWER MODE DEFINITIONS      */
class PowerMode(IntEnum):
    """
    BMM150 power modes
    """

    NORMAL = 0x00  # doc: Normal power mode
    FORCED = 0x01  # doc: Forced power mode
    SLEEP = 0x03  # doc: Sleep mode
    SUSPEND = 0x04  # doc: Suspend power mode


# /**\name PRESET MODE DEFINITIONS  */
class PresetMode(IntEnum):
    """
    BMM150 preset modes
    """

    LOWPOWER = 0x01  # doc: Low power mode
    REGULAR = 0x02  # doc: Normal mode
    HIGHACCURACY = 0x03  # doc: High accuracy mode
    ENHANCED = 0x04  # doc: Enhanced  mode


# /**\name Power mode settings  */
class PowerControl(IntEnum):
    """
    BMM150 power control modes
    """

    DISABLE = 0x00  # doc: Disable
    ENABLE = 0x01  # doc: Enable


# /**\name Sensor delay time settings  */
BMM150_SOFT_RESET_DELAY = 1
BMM150_NORMAL_SELF_TEST_DELAY = 2
BMM150_START_UP_TIME = 3
BMM150_ADV_SELF_TEST_DELAY = 4

# /**\name ENABLE/DISABLE DEFINITIONS  */
BMM150_XY_CHANNEL_ENABLE = 0x00
BMM150_XY_CHANNEL_DISABLE = 0x03

# /**\name Register Address */
BMM150_CHIP_ID_ADDR = 0x40
BMM150_DATA_X_LSB = 0x42
BMM150_DATA_X_MSB = 0x43
BMM150_DATA_Y_LSB = 0x44
BMM150_DATA_Y_MSB = 0x45
BMM150_DATA_Z_LSB = 0x46
BMM150_DATA_Z_MSB = 0x47
BMM150_DATA_READY_STATUS = 0x48
BMM150_INTERRUPT_STATUS = 0x4A
BMM150_POWER_CONTROL_ADDR = 0x4B
BMM150_OP_MODE_ADDR = 0x4C
BMM150_INT_CONFIG_ADDR = 0x4D
BMM150_AXES_ENABLE_ADDR = 0x4E
BMM150_LOW_THRESHOLD_ADDR = 0x4F
BMM150_HIGH_THRESHOLD_ADDR = 0x50
BMM150_REP_XY_ADDR = 0x51
BMM150_REP_Z_ADDR = 0x52

# /**\name DATA RATE DEFINITIONS  */
BMM150_DATA_RATE_10HZ = 0x00
BMM150_DATA_RATE_02HZ = 0x01
BMM150_DATA_RATE_06HZ = 0x02
BMM150_DATA_RATE_08HZ = 0x03
BMM150_DATA_RATE_15HZ = 0x04
BMM150_DATA_RATE_20HZ = 0x05
BMM150_DATA_RATE_25HZ = 0x06
BMM150_DATA_RATE_30HZ = 0x07

# /**\name TRIM REGISTERS      */
# /* Trim Extended Registers */
BMM150_DIG_X1 = 0x5D
BMM150_DIG_Y1 = 0x5E
BMM150_DIG_Z4_LSB = 0x62
BMM150_DIG_Z4_MSB = 0x63
BMM150_DIG_X2 = 0x64
BMM150_DIG_Y2 = 0x65
BMM150_DIG_Z2_LSB = 0x68
BMM150_DIG_Z2_MSB = 0x69
BMM150_DIG_Z1_LSB = 0x6A
BMM150_DIG_Z1_MSB = 0x6B
BMM150_DIG_XYZ1_LSB = 0x6C
BMM150_DIG_XYZ1_MSB = 0x6D
BMM150_DIG_Z3_LSB = 0x6E
BMM150_DIG_Z3_MSB = 0x6F
BMM150_DIG_XY2 = 0x70
BMM150_DIG_XY1 = 0x71

# /**\name PRESET MODES - REPETITIONS-XY RATES */
BMM150_LOWPOWER_REPXY = 1
BMM150_REGULAR_REPXY = 4
BMM150_ENHANCED_REPXY = 7
BMM150_HIGHACCURACY_REPXY = 23

# /**\name PRESET MODES - REPETITIONS-Z RATES */
BMM150_LOWPOWER_REPZ = 2
BMM150_REGULAR_REPZ = 14
BMM150_ENHANCED_REPZ = 26
BMM150_HIGHACCURACY_REPZ = 82

# /**\name Macros for bit masking */
BMM150_PWR_CNTRL_MSK = 0x01

BMM150_CONTROL_MEASURE_MSK = 0x38
BMM150_CONTROL_MEASURE_POS = 0x03

BMM150_POWER_CONTROL_BIT_MSK = 0x01
BMM150_POWER_CONTROL_BIT_POS = 0x00

BMM150_OP_MODE_MSK = 0x06
BMM150_OP_MODE_POS = 0x01

BMM150_ODR_MSK = 0x38
BMM150_ODR_POS = 0x03

BMM150_DATA_X_MSK = 0xF8
BMM150_DATA_X_POS = 0x03

BMM150_DATA_Y_MSK = 0xF8
BMM150_DATA_Y_POS = 0x03

BMM150_DATA_Z_MSK = 0xFE
BMM150_DATA_Z_POS = 0x01

BMM150_DATA_RHALL_MSK = 0xFC
BMM150_DATA_RHALL_POS = 0x02

BMM150_SELF_TEST_MSK = 0x01

BMM150_ADV_SELF_TEST_MSK = 0xC0
BMM150_ADV_SELF_TEST_POS = 0x06

BMM150_DRDY_EN_MSK = 0x80
BMM150_DRDY_EN_POS = 0x07

BMM150_INT_PIN_EN_MSK = 0x40
BMM150_INT_PIN_EN_POS = 0x06

BMM150_DRDY_POLARITY_MSK = 0x04
BMM150_DRDY_POLARITY_POS = 0x02

BMM150_INT_LATCH_MSK = 0x02
BMM150_INT_LATCH_POS = 0x01

BMM150_INT_POLARITY_MSK = 0x01

BMM150_DATA_OVERRUN_INT_MSK = 0x80
BMM150_DATA_OVERRUN_INT_POS = 0x07

BMM150_OVERFLOW_INT_MSK = 0x40
BMM150_OVERFLOW_INT_POS = 0x06

BMM150_HIGH_THRESHOLD_INT_MSK = 0x38
BMM150_HIGH_THRESHOLD_INT_POS = 0x03

BMM150_LOW_THRESHOLD_INT_MSK = 0x07

BMM150_DRDY_STATUS_MSK = 0x01

# /**\name OVERFLOW DEFINITIONS  */
BMM150_XYAXES_FLIP_OVERFLOW_ADCVAL = -4096
BMM150_ZAXIS_HALL_OVERFLOW_ADCVAL = -16384
BMM150_OVERFLOW_OUTPUT = -32768
BMM150_NEGATIVE_SATURATION_Z = -32767
BMM150_POSITIVE_SATURATION_Z = 32767
# #ifdef BMM150_USE_FLOATING_POINT
#     BMM150_OVERFLOW_OUTPUT_FLOAT=0.0f
# #endif

# /**\name Register read lengths=*/
BMM150_SELF_TEST_LEN = 5
BMM150_SETTING_DATA_LEN = 8
BMM150_XYZR_DATA_LEN = 8

# /**\name Self test selection macros */
BMM150_NORMAL_SELF_TEST = 0
BMM150_ADVANCED_SELF_TEST = 1

# /**\name Self test settings */
BMM150_DISABLE_XY_AXIS = 0x03
BMM150_SELF_TEST_REP_Z = 0x04

# /**\name Advanced self-test current settings */
BMM150_DISABLE_SELF_TEST_CURRENT = 0x00
BMM150_ENABLE_NEGATIVE_CURRENT = 0x02
BMM150_ENABLE_POSITIVE_CURRENT = 0x03

# /**\name Normal self-test status */
BMM150_SELF_TEST_STATUS_XYZ_FAIL = 0x00
BMM150_SELF_TEST_STATUS_SUCCESS = 0x07

# /**\name Macro to SET and GET BITS of a register*/


def BMM150_SET_BITS(reg_data, bitname_mask, bitname_pos, data):

    return (reg_data & ~(bitname_mask)) | ((data << bitname_pos) & bitname_mask)


def BMM150_GET_BITS(reg_data, bitname_mask, bitname_pos):

    return (reg_data & (bitname_mask)) >> (bitname_pos)


def BMM150_SET_BITS_POS_0(reg_data, bitname_mask, data):

    return (reg_data & ~(bitname_mask)) | (data & bitname_mask)


def BMM150_GET_BITS_POS_0(reg_data, bitname_mask):

    return reg_data & (bitname_mask)


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


import ctypes
import time
from typing import Tuple

import smbus2  # type: ignore


class ChipIdNotConformError(Exception):
    """The chip ID was not conform."""


class BMM150:
    """BMM150's object.

    Args:
        presetmode (PresetMode, optional): Preset mode used. Defaults to PresetMode.LOWPOWER.
        bus_number (int, optional): I²C bus number. Defaults to 1.
        auto_init (bool, optional): Automatically start I²C init procedure. Defaults to True.
    """

    settings = bmm150_settings()
    raw_mag_data = bmm150_raw_mag_data()
    mag_data = bmm150_mag_data()
    trim_data = bmm150_trim_registers()

    def __init__(
        self,
        presetmode: PresetMode = PresetMode.LOWPOWER,
        bus_number: int = 1,
        auto_init: bool = True,
    ):

        self.presetmode: PresetMode = presetmode

        self.i2c_bus = smbus2.SMBus(bus_number)

        if auto_init:
            self.initialize()

    def initialize(self) -> None:
        """Initializes the bmm150.

        Returns:
            None
        """

        # Power up the sensor from suspend to sleep mode
        self.set_op_mode(PowerMode.SLEEP)
        time.sleep(BMM150_START_UP_TIME / 1000.0)

        # Check chip ID
        chip_id = self.i2c_bus.read_byte_data(BMM150_I2C_Address, BMM150_CHIP_ID_ADDR)
        if chip_id != BMM150_CHIP_ID:
            raise ChipIdNotConformError(
                "The chip ID was not conform. Are you sure you are trying to interface with a bmm150 ?"
            )

        # Function to update trim values
        self.read_trim_registers()

        # Setting the power mode as normal
        self.set_op_mode(PowerMode.NORMAL)

        #  Setting the preset mode as Low power mode
        #    i.e. data rate = 10Hz XY-rep = 1 Z-rep = 2
        self.set_presetmode(self.presetmode)

    def set_op_mode(self, pwr_mode: PowerMode) -> None:
        """Sets power mode

        Args:
            pwr_mode (PowerMode): Desired power mode
        """
        # Select the power mode to set
        if pwr_mode == PowerMode.NORMAL:
            #  If the sensor is in suspend mode
            #    put the device to sleep mode
            self.suspend_to_sleep_mode()
            # write the op mode
            self._write_op_mode(pwr_mode)
        elif pwr_mode == PowerMode.FORCED:
            #  If the sensor is in suspend mode
            #    put the device to sleep mode
            self.suspend_to_sleep_mode()
            # write the op mode
            self._write_op_mode(pwr_mode)
        elif pwr_mode == PowerMode.SLEEP:
            #  If the sensor is in suspend mode
            #    put the device to sleep mode
            self.suspend_to_sleep_mode()
            # write the op mode
            self._write_op_mode(pwr_mode)
        elif pwr_mode == PowerMode.SUSPEND:
            # Set the power control bit to zero
            self._set_power_control_bit(PowerControl.DISABLE)

    def set_presetmode(self, preset_mode: PresetMode):
        """Sets preset mode

        Args:
            preset_mode (PresetMode): Desired preset mode
        """
        if preset_mode == PresetMode.LOWPOWER:
            #  Set the data rate x,y,z repetition
            #    for Low Power mode
            self.settings.data_rate = BMM150_DATA_RATE_10HZ
            self.settings.xy_rep = BMM150_LOWPOWER_REPXY
            self.settings.z_rep = BMM150_LOWPOWER_REPZ
            self._set_odr_xyz_rep()
        elif preset_mode == PresetMode.REGULAR:
            #  Set the data rate x,y,z repetition
            #    for Regular mode
            self.settings.data_rate = BMM150_DATA_RATE_10HZ
            self.settings.xy_rep = BMM150_REGULAR_REPXY
            self.settings.z_rep = BMM150_REGULAR_REPZ
            self._set_odr_xyz_rep()
        elif preset_mode == PresetMode.HIGHACCURACY:
            #  Set the data rate x,y,z repetition
            #    for High Accuracy mode
            self.settings.data_rate = BMM150_DATA_RATE_20HZ
            self.settings.xy_rep = BMM150_HIGHACCURACY_REPXY
            self.settings.z_rep = BMM150_HIGHACCURACY_REPZ
            self._set_odr_xyz_rep()
        elif preset_mode == PresetMode.ENHANCED:
            #  Set the data rate x,y,z repetition
            #    for Enhanced Accuracy mode
            self.settings.data_rate = BMM150_DATA_RATE_10HZ
            self.settings.xy_rep = BMM150_ENHANCED_REPXY
            self.settings.z_rep = BMM150_ENHANCED_REPZ
            self._set_odr_xyz_rep()

    def suspend_to_sleep_mode(self):
        """ """
        self._set_power_control_bit(PowerControl.ENABLE)
        # Start-up time delay of 3ms
        time.sleep(BMM150_START_UP_TIME / 1000.0)

    def _write_op_mode(self, op_mode: PowerMode):
        """Writes chosen power mode to I²C register.

        Args:
            op_mode (PowerMode): Chosen power mode
        """

        reg_data = self.i2c_bus.read_byte_data(BMM150_I2C_Address, BMM150_OP_MODE_ADDR)
        # Set the op_mode value in Opmode bits of 0x4C
        reg_data = BMM150_SET_BITS(
            reg_data, BMM150_OP_MODE_MSK, BMM150_OP_MODE_POS, op_mode
        )
        self.i2c_bus.write_byte_data(BMM150_I2C_Address, BMM150_OP_MODE_ADDR, reg_data)

    def _set_power_control_bit(self, pwrcntrl_bit: PowerControl):
        """Enables or disables the power bit.

        Args:
            pwrcntrl_bit (PowerControl): _description_
        """
        # Power control register 0x4B is read
        reg_data = self.i2c_bus.read_byte_data(
            BMM150_I2C_Address, BMM150_POWER_CONTROL_ADDR
        )
        # Sets the value of power control bit
        reg_data = BMM150_SET_BITS_POS_0(reg_data, BMM150_PWR_CNTRL_MSK, pwrcntrl_bit)
        self.i2c_bus.write_byte_data(
            BMM150_I2C_Address, BMM150_POWER_CONTROL_ADDR, reg_data
        )

    def _set_odr_xyz_rep(self):
        """_summary_"""
        # Set the ODR
        self._set_odr()
        # Set the XY-repetitions number
        self.i2c_bus.write_byte_data(
            BMM150_I2C_Address, BMM150_REP_XY_ADDR, self.settings.xy_rep
        )
        # Set the Z-repetitions number
        self.i2c_bus.write_byte_data(
            BMM150_I2C_Address, BMM150_REP_Z_ADDR, self.settings.z_rep
        )

    def _set_odr(self):
        """_summary_"""
        reg_data = self.i2c_bus.read_byte_data(BMM150_I2C_Address, BMM150_OP_MODE_ADDR)
        # Set the ODR value
        reg_data = BMM150_SET_BITS(
            reg_data, BMM150_ODR_MSK, BMM150_ODR_POS, self.settings.data_rate
        )
        self.i2c_bus.write_byte_data(BMM150_I2C_Address, BMM150_OP_MODE_ADDR, reg_data)

    def soft_reset(self):
        """
        Soft resets the module.
        """
        reg_data = self.i2c_bus.read_byte_data(
            BMM150_I2C_Address, BMM150_POWER_CONTROL_ADDR
        )
        reg_data = reg_data | BMM150_SET_SOFT_RESET
        self.i2c_bus.write_byte_data(
            BMM150_I2C_Address, BMM150_POWER_CONTROL_ADDR, reg_data
        )
        time.sleep(BMM150_SOFT_RESET_DELAY / 1000.0)

    def read_trim_registers(self):
        """
        Reads the trim registers for calibration.
        """
        trim_x1y1 = self.i2c_bus.read_i2c_block_data(
            BMM150_I2C_Address, BMM150_DIG_X1, 2
        )
        trim_xyz_data = self.i2c_bus.read_i2c_block_data(
            BMM150_I2C_Address, BMM150_DIG_Z4_LSB, 4
        )
        trim_xy1xy2 = self.i2c_bus.read_i2c_block_data(
            BMM150_I2C_Address, BMM150_DIG_Z2_LSB, 10
        )

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
        reg_data = self.i2c_bus.read_i2c_block_data(
            BMM150_I2C_Address, BMM150_DATA_X_LSB, BMM150_XYZR_DATA_LEN
        )

        # Mag X axis data
        reg_data[0] = BMM150_GET_BITS(reg_data[0], BMM150_DATA_X_MSK, BMM150_DATA_X_POS)
        # Convert to a c-type int8, to add a twos-complement awareness
        reg_data[1] = ctypes.c_int8(reg_data[1]).value
        # Shift the MSB data to left by 5 bits
        # Multiply by 32 to get the shift left by 5 value
        msb_data = reg_data[1] * 32
        # Raw mag X axis data
        self.raw_mag_data.raw_datax = msb_data | reg_data[0]

        # Mag Y axis data
        reg_data[2] = BMM150_GET_BITS(reg_data[2], BMM150_DATA_Y_MSK, BMM150_DATA_Y_POS)
        # Convert to a c-type int8, to add a twos-complement awareness
        reg_data[3] = ctypes.c_int8(reg_data[3]).value
        # Shift the MSB data to left by 5 bits
        # Multiply by 32 to get the shift left by 5 value
        msb_data = reg_data[3] * 32
        # Raw mag Y axis data
        self.raw_mag_data.raw_datay = msb_data | reg_data[2]

        # Mag Z axis data
        reg_data[4] = BMM150_GET_BITS(reg_data[4], BMM150_DATA_Z_MSK, BMM150_DATA_Z_POS)
        # Convert to a c-type int8, to add a twos-complement awareness
        reg_data[5] = ctypes.c_int8(reg_data[5]).value
        # Shift the MSB data to left by 7 bits
        # Multiply by 128 to get the shift left by 7 value
        msb_data = reg_data[5] * 128
        # Raw mag Z axis data
        self.raw_mag_data.raw_dataz = msb_data | reg_data[4]

        # Mag R-HALL data
        # R-hall is always unsigned, no need for twos-complement awareness
        reg_data[6] = BMM150_GET_BITS(
            reg_data[6], BMM150_DATA_RHALL_MSK, BMM150_DATA_RHALL_POS
        )
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

        # /* Overflow condition check */
        if (
            (mag_data_x != BMM150_XYAXES_FLIP_OVERFLOW_ADCVAL)
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
            retval = BMM150_OVERFLOW_OUTPUT

        return retval

    def _compensate_y(self, mag_data_y, data_rhall):
        """This internal API is used to obtain the compensated
        magnetometer Y axis data(micro-tesla) in floating point.
        """
        # /* Overflow condition check */
        if (
            (mag_data_y != BMM150_XYAXES_FLIP_OVERFLOW_ADCVAL)
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
            retval = BMM150_OVERFLOW_OUTPUT

        return retval

    def _compensate_z(self, mag_data_z, data_rhall):
        """This internal API is used to obtain the compensated
        magnetometer Z axis data(micro-tesla) in floating point.
        """
        # /* Overflow condition check */
        if (
            (mag_data_z != BMM150_ZAXIS_HALL_OVERFLOW_ADCVAL)
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
            retval = BMM150_OVERFLOW_OUTPUT

        return retval

