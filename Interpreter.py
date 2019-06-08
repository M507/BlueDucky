

def writeOpenPowershell():
    string = "GUI r\n" \
             "DELAY 50\n" \
             "STRING powershell\n" \
             "ENTER\n" \
             "DELAY 300"
    return string

def writeOpenCMD():
    string = "GUI r\n" \
             "DELAY 50\n" \
             "STRING cmd\n" \
             "ENTER\n" \
             "DELAY 300"
    return string

def writeLogin(username,ip,password):
    string = "STRING ssh "+username+"@"+ip+"\n" \
             "ENTER\n" \
             "DELAY 500\n" \
             "STRING "+password+"\n" \
             "ENTER\n" \
             "DELAY 500"

    return string

def writeCommands(script):
    string = "STRING "+script+"\n"\
             "ENTER\n"\
             "DELAY 300"
    return string

def changePasswordHelper(OS,user, password):
    string = ""
    if OS == "Win":
        string = "STRING net user "+user+" "+ password +"\n" \
                 "ENTER\n"\
                 "DELAY 300"
    elif OS == "Linux":
        string = "STRING passwd\n" \
                 "ENTER\n" \
                 "DELAY 300\n"\
                 "STRING " + password + "\n" \
                 "ENTER\n" \
                 "DELAY 300\n" \
                 "STRING " + password +" \n" \
                 "ENTER\n" \
                 "DELAY 300"
    else:
        print("Unknown OS - changePasswordHelper(OS,user, password)")
        exit(-1)
    return string