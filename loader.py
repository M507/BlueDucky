
"""
This function reads Config/NewPasswords file,
and based on that file, all the password will
be changed to the specified parameters accordingly.
"""
def readNewPassword():
    # Win:password123
    aList = []
    try:
        for line in open("Config/NewPasswords"):
            line = line.split(':')
            OS = line[0].strip('\n')
            password = line[1].strip('\n')
            aList.append([OS, password])
    except Exception as e:
        print("Error at readNewPassword()")
        print(e)

    return aList

"""
This function reads Config/NewPasswords which should have all 
The inputs for the new users.
"""
def readNewUsers():
    # Win:Admin123:MyPasswordIs123456:1
    aList = []
    try:
        for line in open("Config/NewUsers"):
            line = line.split(':')
            OS = line[0]
            username = line[1].strip('\n')
            password = line[2].strip('\n')
            admin = line[3].strip('\n')
            aList.append([OS, username, password, admin])
    except Exception as e:
        print("Error at readNewUsers()")
        print(e)
    return aList


def readCurrentUsers():
    # Win:admin:10.1.2.1:CCDCsucks123#
    aList = []
    try:
        for line in open("Config/startingAccounts"):
            line = line.split(':')
            OS = line[0].strip('\n')
            username = line[1].strip('\n')
            ip = line[2].strip('\n')
            password = line[3].strip('\n')
            aList.append([OS, username, ip, password])
    except Exception as e:
        print("Error at readCurrentUsers()")
        print(e)

    return aList

