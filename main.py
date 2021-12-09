#Directory where CCM files exist
IMPORT_PATH = "./motor-parameter-files/"
#Directory where to export the DM2 files
EXPORT_PATH = ""
#Path for DM2 XML Templates
XML_TEMPLATES = "./XML_Templates/"

import os
from DM2 import MotorUtility
import traceback
import logging

#Walk the OS path to for any files in the director or sub-directories
def ccm_folder_walk(IMPORT_PATH):
    filelist = []
    for root, dirs, files in os.walk(IMPORT_PATH):
        for file in files:
            if file[-4:] == ".ccm":
                #Append the file name to the list
                filelist.append(os.path.join(root,file))
    return filelist

def main():
    #Create and EL7411 Object
    dm2motor = MotorUtility()

    #Mass Import Routine
    filelist = ccm_folder_walk(IMPORT_PATH)
    print(f"Now Importing {len(filelist)} Motor Files...")
    dc_motor_count = 0
    ac_motor_count = 0
    for file in filelist:
        try:
            dm2motor.import_ccm_motordata(file)
            #You can print the motor data for each file like this
            #print(el7411.get_motor_data())
            if dm2motor.IsAc == "false":
                dm2motor.export_EL7411_dmmotor(EXPORT_PATH)
                dc_motor_count += 1
        except Exception as e:
            print("On File:", file)
            logging.error(traceback.format_exc())
            # Logs the error appropriately.

    print(f"Number of DC Motors Exported: {dc_motor_count}")
    print(f"Number of AC Motors Exported: {ac_motor_count}")

if __name__ == '__main__':
    main()