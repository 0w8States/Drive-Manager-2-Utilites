class HDMotorUtils:
    def __init__(self):
        self.OrderCode = ""

    def check_voltage(self, motor_ordercode):

        if "FHA" in motor_ordercode:
            return self.FHA_voltage(motor_ordercode)

        elif "RSF" in motor_ordercode:
            return self.RSF_voltage(motor_ordercode)

        elif "LPA" in motor_ordercode:
            return self.LPA_voltage(motor_ordercode)

        elif "LBC" in motor_ordercode:
            return self.LBC_voltage(motor_ordercode)

        elif "SHA" in motor_ordercode:
            return self.SHA_voltage(motor_ordercode)

        else:
            print("Motor Code Not Found")


    def FHA_voltage(self, motor_ordercode):
        order_parse = motor_ordercode.strip().split("-")
        #Motor Check FHA
        if not order_parse[0] == "FHA":
            return "Incorrect Motor"   
        #FHA 8C, 11C, 14C check
        if order_parse[1] == "8C" or order_parse[1] == "11C" or order_parse[1] == "14C":
            #Absolute Encoder
            if "12S17b" in order_parse[3] or "SB14bSB14b" in order_parse[3]:
                if "A" in order_parse[3]:
                    return ("AC", 100)
                elif "G" in order_parse[3]:
                    return ("AC", 200)
                elif "E" in order_parse[3]:
                    return ("DC", 24)
            #Incremental Encoder
            else:
                if len(order_parse) >= 5:
                    if order_parse[4] == "E":
                        return ("DC", 24)
                    else:
                        return ("AC", 100)
                else:
                    return ("AC", 100)

        #FHA 17C, 25C, 32C, 40C check
        if order_parse[1] == "17C" or order_parse[1] == "25C" or order_parse[1] == "32C" or order_parse[1] == "40C":
            if len(order_parse) >= 5:
                if order_parse[4] == "A":
                    return ("AC", 100)
                elif order_parse[4] == "E" and order_parse[1] == "17C":
                    return ("DC", 24)
                elif order_parse[3] == "H":
                    return ("AC", 480)
                else:
                    return ("AC", 200)
            else:
                return ("AC", 200)

    def RSF_voltage(self, motor_ordercode):
        order_parse = motor_ordercode.strip().split("-")

        #Motor Check RSF
        if order_parse[1] == "17A" or order_parse[1] == "20A" or order_parse[1] == "25A" or order_parse[1] == "32A":
            return ("AC", 200)
        else:
            return ("DC", 24)
        
    def LPA_voltage(self, motor_ordercode):
        return ("DC", 24)

    def LBC_voltage(self, motor_ordercode):
        return ("AC", 200)

    def SHA_voltage(self, motor_ordercode):
        order_parse = motor_ordercode.strip().split("-")
        #print(order_parse)
        if "100" in order_parse[1]:
            return ("AC", 100)
        elif "200" in order_parse[1]:
            return ("AC", 200)
        else:
            return ("DC", 24)
