from HarmonicDriveSystems import HDMotorUtils

#Utilites for handling Copley Controls CME datatypes
class CCM:  
    def import_ccm(self, filepath):
        # open the ccm motor file and read the data
        import_motor = open(filepath, "r")
        ccm_motor = {}
        current_line = 0
        for data in import_motor:
            if 2 == current_line:
                current_parameter = data.strip().split(",")
                if self.__is_int(current_parameter[3]):
                    ccm_motor[current_parameter[2]] = int(current_parameter[3])
                else:
                    ccm_motor[current_parameter[2]] = current_parameter[3]
            else:
                current_line += 1

        # If it's an HD Motor, check the voltage via name plate
        if "Harmonic" in ccm_motor["Motor Manufacturer"]:
            hdmotor = HDMotorUtils()
            voltage_data = hdmotor.check_voltage(ccm_motor["Motor Model Number"])
            ccm_motor["Motor Voltage"] = voltage_data[1]
            if voltage_data[0] == "AC":
                ccm_motor["Motor IsAc"] = "true"
            else:
                ccm_motor["Motor IsAc"] = "false"
            del hdmotor
        else:
            voltage_data = ("",0)
            voltage_data[0] = input("Please Input AC or DC for voltage:")
            voltage_data[1] = int(input("Please Input the value for voltage:"))

        import_motor.close()
        return ccm_motor

    #Check if a value is an Int type
    def __is_int(self, value):
        try:
            int(value)
            return True
        except:
            return False
