import sys
from sts1_sensors.pysatdosclient import SatDosClient, StatusCode, SensorType

'''
Description of data types

Enum SensorType
RADFET           TID measurement sensor
SRAM             SEE measurement sensor

Enum StatusCode
Ok               Request successful
InitFailed       Initialization of client library failed
InvalidCRC       CRC calculation of response failed
InvalidInput     Invalid input data given
I2CReadFailed    I2C read request failed
I2CWriteFailed   I2C write request failed
DataUnavailable  Measurement data currently unavailable
NotOperative     SATDOS board not fully operational - if persistent, contact mission operation (TU Wien Space Team)
TimeNotSet       SATDOS time has not been set since last boot

Structure Status
Code             StatusCode describing resquest result
Message          Status message applicable only if resulting Code <> Ok

Structure Response
Status           Status of request
Firmware         SATDOS firmware version, applicable only on reqStatus
Temperature      Temperature value taken from TMP175 sensor, applicable only on reqTemp
Inverval         Sensor interval of the given sensor type, applicable only on reqInterval
Uptime           Epoch time since last SATDOS boot, applicable only on reqUptime
RADFET_1         Accumulated Total Dose in units of rad of RADFET 1 sensor since mission start, applicable only on reqTID
RADFET_2         Accumulated Total Dose in units of rad of RADFET 2 sensor since mission start, applicable only on reqTID
RADFET_3         Accumulated Total Dose in units of rad of RADFET 3 sensor since mission start, applicable only on reqTID
RADFET_4         Accumulated Total Dose in units of rad of RADFET 4 sensor since mission start, applicable only on reqTID
CY62157          Accumulated Single Event Upsets (SEU) on SRAM 1 sensor (= Cypress CY62157) since last readout, applicable only on reqSEE
ISSI             Accumulated Single Event Upsets (SEU) on SRAM 2 sensor (= ISSI IS61) since last readout, applicable only on reqSEE

For a description of the SATDOS payload and its sensors (TMP175, RADFET, SRAM), please refer e.g. to 10.1109/RADECS53308.2021.9954463
'''

'''
Method:     Constructor
Purpose:    Create client object for communication with SATDOS board
Parameters: Executable name
Response:   Client object
'''
client = SatDosClient(sys.argv[0])


'''
Method:     init
Purpose:    Initialize client object
Parameters: None
Response:   Status       See above structure description
'''
response = client.init()
if response.Status.Code != StatusCode.Ok:
    print("Status:", str(response.Status.Code), "Message:", response.Status.Message)
    sys.exit(response.Status.Code)


'''
Method:     reqStatus
Purpose:    Request status of SATDOS board
Parameters: None
Response:   Status       See above structure description
            Firmware     String containing running firmware
'''
response = client.reqStatus()
if response.Status.Code != StatusCode.Ok:
    print("Status:", str(response.Status.Code), "Message:", response.Status.Message)

    if response.Status.Code != StatusCode.TimeNotSet:
        sys.exit(response.Status.Code)

print("Firmware version:", response.Version);


'''
Method:     setInterval
Purpose:    Set interval for a specific sensor type
Parameters: SensorType   See above type definition 
            Interval     Integer in seconds. Zero is treated as default
Response:   Status       See above structure description
'''
response = client.setInterval(SensorType.SRAM, 60);
if response.Status.Code != StatusCode.Ok:
    print("Status:", str(response.Status.Code), "Message:", response.Status.Message)
    sys.exit(response.Status.Code)


'''
Method:     reqInterval
Purpose:    Request interval for a specific sensor type
Parameters: SensorType   See above type definition 
Response:   Status       See above structure description
            Interval     Integer in seconds
'''
response = client.reqInterval(SensorType.SRAM);
if response.Status.Code != StatusCode.Ok:
    print("Status:", str(response.Status.Code), "Message:", response.Status.Message)
    sys.exit(response.Status.Code)

print("SRAM interval:", str(response.Interval))


'''
Method:     reqUptime
Purpose:    Request number of seconds since last SATDOS startup 
Parameters: None
Response:   Status       See above structure description
            Uptime       Integer in seconds
'''
response = client.reqUptime()
if response.Status.Code != StatusCode.Ok:
    print("Status:", str(response.Status.Code), "Message:", response.Status.Message)
    sys.exit(response.Status.Code)

print("Uptime:", str(response.Uptime))


'''
Method:     reqTemp
Purpose:    Request temperature value from TMP175 sensor
Parameters: None
Response:   Status       See above structure description
            Temperature  Float in degree celsius. Resolution 1/100 degree
'''
response = client.reqTemp()
if response.Status.Code != StatusCode.Ok:
    print("Status:", str(response.Status.Code), "Message:", response.Status.Message)
    sys.exit(response.Status.Code)

print("Temperature:", str(response.Temperature))


'''
Method:     reqTID
Purpose:    Request dose from the last reading of the RADFET sensors
Parameters: None
Response:   Status       See above structure description
            RADFET_1     Float in rad
            RADFET_2     Float in rad
            RADFET_3     Float in rad
            RADFET_4     Float in rad
'''
response = client.reqTID()
if response.Status.Code != StatusCode.Ok:
    print("Status:", str(response.Status.Code), "Message:", response.Status.Message)
    sys.exit(response.Status.Code)

print("RADFET 1 dose:", str(response.RADFET_1)
  + "\nRADFET 2 dose:", str(response.RADFET_2)
  + "\nRADFET 3 dose:", str(response.RADFET_3)
  + "\nRADFET 4 dose:", str(response.RADFET_4))


'''
Method:     reqSEE
Purpose:    Request number of SEU from the last reading of the SRAMs
Parameters: None
Response:   Status       See above structure description
            CY62157      Integer number of errors counted
            ISSI         Integer number of errors counted
'''
response = client.reqSEE()
if response.Status.Code != StatusCode.Ok:
    print("Status:", str(response.Status.Code), "Message:", response.Status.Message)
    sys.exit(response.Status.Code)

print("SRAM CY62157 error count:", str(response.CY62157)
  + "\nSRAM ISSI error count   :", str(response.ISSI))
