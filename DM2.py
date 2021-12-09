from math import sqrt
from CME import CCM
import os

class MotorUtility:
    def __init__(self):
        #Motor Vendor
        self.Vendor = "N\A"
        #Motor Model Number
        self.OrderCode = "N\A"
        #Motor Voltage
        self.Voltage = 0
        # DC Bus Voltage
        self.DcBusVoltage = 0
        #Nominal Current in Amps
        self.Inrms = 0.0
        #Peak Current in Amps
        self.Iprms = 0.0
        #Max Speed in RPMs
        self.Nmax = 0.0
        #Torque Constant in Nm/Amp
        self.kT = 0.0
        #Voltage Constant in V/Rpm
        self.kErms = 0.0
        #Motor Pole Pairs
        self.PolePairs = 0
        #Inertia in kgm^2
        self.J = 0.0
        #Termanl time constant in minutes
        self.Mtc = 0
        #Peak motor time constant in seconds
        self.Ti2t = 0
        #EL7411 specific
        self.IsAc = "false"
        self.ConstrType = 6
        self.IsBeckhoffMotorShaftSpeicified = "false"
        #Motor Type
        self.ElecType = ""
        #Nominal current
        self.I0rms = 0.0
        #Drive Voltage and Nominal Torque
        self.MnUnrms = (0.0, 0.0)
        #Drive Voltage and Nominal Speed
        self.NnUnrms = (0.0, 0.0)
        #Resistance in Ohms
        self.R = 0.0
        #Inductance in Henrys
        self.Lq = 0.0
    
    #Imports the CCM data from a file and converts it to the proper EL7411 data
    def import_ccm_motordata(self, file_path):
        # open the ccm motor file and read the data
        ccm = CCM()
        motor_data_dictionary = ccm.import_ccm(file_path)
        self.__convert_ccm_to_DM2(motor_data_dictionary)
        del ccm

    # Converts all the CCM motor data to work with DM2
    def __convert_ccm_to_DM2(self, ccm_motor):
        #EL7411 data import
        self.Vendor = ccm_motor["Motor Manufacturer"]
        self.OrderCode = ccm_motor["Motor Model Number"]
        self.IsAc = ccm_motor["Motor IsAc"]
        self.Voltage = ccm_motor["Motor Voltage"]
        if self.IsAc == "true":
            self.DcBusVoltage = self.__DC_rectify(self.Voltage)
        else:
            self.DcBusVoltage = self.Voltage
        self.Inrms = round(ccm_motor["Motor Continuous Torque"]/self.__NmApk_to_NmArms(ccm_motor["Motor Torque Constant"]),2)
        self.Iprms = round(ccm_motor["Motor Peak Torque"]/self.__NmApk_to_NmArms(ccm_motor["Motor Torque Constant"]),2)
        self.Nmax = round((9.554140127 * (self.Inrms * self.DcBusVoltage))/(ccm_motor["Motor Continuous Torque"] * 0.00001))
        self.kT = round(self.__NmApk_to_NmArms(ccm_motor["Motor Torque Constant"]) * 0.00001, 4)
        self.kErms = round(ccm_motor["Motor Back Emf Constant"] *0.00001,4)
        self.PolePairs = ccm_motor["Motor Pole Pairs"]
        self.J = ccm_motor["Motor Inertia"] * 0.0000000001
        self.Mtc = 20   #Do not exists for most files
        self.Ti2t = 1   #Do not exists for most files
        self.ElecType = ccm_motor["Motor Manufacturer"]
        self.I0rms = round(ccm_motor["Motor Continuous Torque"]/self.__NmApk_to_NmArms(ccm_motor["Motor Torque Constant"]), 3)
        self.MnUnrms = (self.Voltage, round(ccm_motor["Motor Continuous Torque"] * 0.00001,3))
        self.NnUnrms = (self.Voltage, round(self.Nmax/2))
        self.R = ccm_motor["Motor Resistance"] * 0.01
        self.Lq = ccm_motor["Motor Inductance"] * 0.00001

    def __DC_rectify(self, AC_voltage):
        #Forward voltage drop of diode
        Vf = 0.705
        return AC_voltage / Vf

    #Convert Nm/Apk to Nm/Arms
    def __NmApk_to_NmArms(self, torque_constant_apk):
        return sqrt(2) * torque_constant_apk
    
    def export_EL7411_dmmotor(self, path):
        working_path = path
        root_folder = "EL7411"
        make = self.Vendor
        model = self.OrderCode[:3]

        save_name = ""
        #Check to make sure the name is safe to save with
        for char in self.OrderCode:
            if not (char.isalpha() or char.isdigit()):
                save_name += "-"
            else:
                save_name += char

        self.OrderCode = save_name + ".dmmotor"

        if not os.path.isdir(working_path + f"{root_folder}/"):
            os.mkdir(working_path + f"{root_folder}")
        working_path += f"{root_folder}/"

        if not os.path.isdir(working_path + f"{make}/"):
            os.mkdir(working_path + f"{make}")
        working_path += f"{make}/"

        if not os.path.isdir(working_path + f"{model}/"):
            os.mkdir(working_path + f"{model}")
        working_path += f"{model}/"

        output_file = open(working_path + self.OrderCode, "w")
        output_file.write(self.__XML_EL7411_Doc_Generator())
        output_file.close()



    def get_motor_data(self):
        print_string = f"Vendor:\t\t{self.Vendor}\n"
        print_string +=f"OrderCode:\t{self.OrderCode}\n"
        print_string +=f"Voltage DC:\t{self.DcBusVoltage}\n"
        print_string +=f"Inrms:\t\t{self.Inrms}\n"
        print_string +=f"Iprms:\t\t{self.Iprms}\n"
        print_string +=f"Nmax:\t\t{self.Nmax}\n"
        print_string +=f"kT:\t\t{self.kT}\n"
        print_string +=f"kErms:\t\t{self.kErms}\n"
        print_string +=f"PolePairs:\t{self.PolePairs}\n"
        print_string +=f"J:\t\t{self.J}\n"
        print_string +=f"Mtc:\t\t{self.Mtc}\n"
        print_string +=f"Ti2t:\t\t{self.Ti2t}\n"
        print_string +=f"MnUnrms:\t{self.MnUnrms}\n"
        print_string +=f"NnUnrms:\t{self.NnUnrms}\n"
        print_string +=f"R:\t\t{self.R}\n"
        print_string +=f"Lq:\t\t{self.Lq}\n"
        return print_string


    def __XML_EL7411_Doc_Generator(self):
        XML_document_text = f'''<?xml version="1.0" encoding="utf-8"?>
<Motor IsManualInput="true" IsManualMFiInput="false">
    <DatabaseType>
        <SchemaVersion />
        <DataVersion />
        <OrderCode>{self.OrderCode}</OrderCode>
        <GroupType />
        <ElectricMotorType>{self.OrderCode}</ElectricMotorType>
        <MotorfeedbackType />
        <MotorbrakeType />
        <AssemblyType />
        <VendorName>{self.Vendor}</VendorName>
        <IsAc>{self.IsAc}</IsAc>
        <ConstructType>{self.ConstrType}</ConstructType>
        <IsBeckhoffMotorShaftSpeicified>{self.IsBeckhoffMotorShaftSpeicified}</IsBeckhoffMotorShaftSpeicified>
    </DatabaseType>
    <DatabaseParameters>
        <Parameter>
            <Comment LcId="1033">Vendor</Comment>
            <Name>Vendor</Name>
            <Data type="visibleString">{self.Vendor}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Order code</Comment>
            <Name>OrderCode</Name>
            <Data type="visibleString">{self.OrderCode}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Nominal current</Comment>
            <Name>Inrms</Name>
            <Data type="real64" unitSiNumerator="4">{self.Inrms}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Peak current</Comment>
            <Name>Iprms</Name>
            <Data type="real64" unitSiNumerator="4">{self.Iprms}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Max. mechanical speed</Comment>
            <Name>Nmax</Name>
            <Data type="real64" unitSiNumerator="225">{self.Nmax}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Torque constant</Comment>
            <Name>kT</Name>
            <Data type="real64" unitSiNumerator="86" unitSiDenominator="4">{self.kT}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Voltage constant</Comment>
            <Name>kErms</Name>
            <Data type="real64" unitSiNumerator="38" unitSiDenominator="225">{self.kErms}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Pole pairs</Comment>
            <Name>PolePairs</Name>
            <Data type="real64">{self.PolePairs}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Motor inertia with brake and encoder</Comment>
            <Name>J</Name>
            <Data type="real64" unitSiNumerator="224">{self.J}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Motor thermal time constant</Comment>
            <Name>Mtc</Name>
            <Data type="real64" unitSiNumerator="71">{self.Mtc}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Time constant i²t</Comment>
            <Name>Ti2t</Name>
            <Data type="real64" unitSiNumerator="3">{self.Ti2t}</Data>
        </Parameter>
        <Parameter>
            <Name>ConstrType</Name>
            <Data type="real64">{self.ConstrType}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Electric motor type</Comment>
            <Name>ElecType</Name>
            <Data type="visibleString">{self.OrderCode}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Nominal current</Comment>
            <Name>I0rms</Name>
            <Data type="real64" unitSiNumerator="4">{self.Inrms}</Data>
        </Parameter>
        <Parameter>
            <Name>MnUnrms</Name>
            <DataTable type="real641" unitSiNumerator="38">
                <item>{self.MnUnrms[0]}</item>
            </DataTable>
            <DataTable type="real641" unitSiNumerator="86">
                <item>{self.MnUnrms[1]}</item>
            </DataTable>
        </Parameter>
        <Parameter>
            <Name>NnUnrms</Name>
            <DataTable type="real641" unitSiNumerator="38">
                <item>{self.NnUnrms[0]}</item>
            </DataTable>
            <DataTable type="real641" unitSiNumerator="225">
                <item>{self.NnUnrms[1]}</item>
            </DataTable>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Winding resistance R Ph-Ph 20°C</Comment>
            <Name>R</Name>
            <Data type="real64" unitSiNumerator="40">{self.R}</Data>
        </Parameter>
        <Parameter>
            <Comment LcId="1033">Winding inductance Lq Ph-Ph 20°C</Comment>
            <Name>Lq</Name>
            <Data type="real64" unitSiNumerator="44">{self.Lq}</Data>
        </Parameter>
    </DatabaseParameters>
</Motor>'''
        return XML_document_text