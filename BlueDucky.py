from Co import *
from loader import *
from Interpreter import *


"""
Foe every "user" in starting accounts:
Change the "user"'s password according to the OS type. 
"""
def changeAllPasswords(stringsList,readCurrentUsersList,readNewPasswordList):
    accounts = []
    for user in readCurrentUsersList:
        readCurrentUsersList_OS = user[0]
        username = user[1]
        ip = user[2]
        oldPassword = user[3]
        for line in readNewPasswordList:
            readNewPasswordList_OS = line[0]
            newPassword = line[1]
            if readCurrentUsersList_OS == readNewPasswordList_OS:
                # login
                l = writeLogin(username,ip,oldPassword)
                stringsList.append(l)
                l = changePasswordHelper(readNewPasswordList_OS,username, newPassword)
                stringsList.append(l)
                l = writeCommands("exit")
                stringsList.append(l)
                accounts.append([username,ip,newPassword,readNewPasswordList_OS])
    return stringsList, accounts

"""
For each account in "accounts" list:
-> Login into ssh
-> Execute commands
-> Exit
"""
def forEachAccount(mainList,accounts,commands):
    # [username,ip,newPassword,os]
    for account in accounts:
        username = account[0]
        ip = account[1]
        newPassword = account[2]
        l = writeLogin(username, ip, newPassword)
        mainList.append(l)
        l = writeCommands(commands)
        mainList.append(l)
        l = writeCommands("exit")
        mainList.append(l)
    return mainList


"""
Create backup users
"""
def addUsers(mainList, accounts):
    # [OS, username, password, admin]
    # Win:Admin123:MyPasswordIs123456:1
    readNewUsersList = readNewUsers()

    # [username,ip,newPassword,os]
    for account in accounts:
        # [OS, username, password, admin]
        for newUser in readNewUsersList:
            OS1 = newUser[0]
            newUserUsername = newUser[1]
            password = newUser[2]
            admin = newUser[3]

            username = account[0]
            ip = account[1]
            currentPassword = account[2]
            OS2 = account[3]

            # If the OS is Windows
            print(OS1,OS2)
            if OS1 == "Win" and OS2 == "Win":

                # Login first
                l = writeLogin(username, ip, currentPassword)
                mainList.append(l)

                # Create the new user
                command = "net user /add " + newUserUsername + " " + password
                l = writeCommands(command)
                mainList.append(l)

                # If admin - add it to the admins group
                if admin:
                    command = "new localgroup administrators "+newUserUsername+" /add"
                    l = writeCommands(command)
                    mainList.append(l)

                # Logout
                l = writeCommands("exit")
                mainList.append(l)

            elif OS1 == "Linux" and OS2 == "Linux":

                # Login first
                l = writeLogin(username, ip, currentPassword)
                mainList.append(l)

                # Create the new user
                command = "adduser " + newUserUsername
                l = writeCommands(command)
                """
                Enter new UNIX password:
                Retype new UNIX password:
                passwd: password updated successfully
                """
                mainList.append(l)
                command = password
                l = writeCommands(command)
                mainList.append(l)
                command = password
                l = writeCommands(command)
                mainList.append(l)

                # If admin - add it to the admins group
                if admin:
                    command = "usermod -aG sudo " + newUserUsername + " /add"
                    l = writeCommands(command)
                    mainList.append(l)
                    command = currentPassword
                    l = writeCommands(command)
                    mainList.append(l)

                # Logout
                l = writeCommands("exit")
                mainList.append(l)
            else:
                pass

    return mainList

def setupPlans():
    plans = []
    print("List all plans:")
    for dir in getFiles("Plans"):
        print("  "+dir)
    while 1:
        inputs = s_input("Which script would you like to run? or q to exit")
        if answerExit(inputs):
            break
        if os.path.isfile("Plans/"+inputs):
            plans.append("Plans/"+inputs)

        print("List of the scripts that will compile:")
        for script in plans:
            print("  " + script)

    print("The final list:")
    for script in plans:
        print("  " + script)
    return plans

def executePlans(mainList, plans, accounts):
    for plan in plans:
        with open(plan, 'r') as f:
            output = f.read()
            # replace every \n by ;
            # since the compiler can not interpret newlines
            output = output.replace('\n', ';')

        # For each account in the "accounts" list
        for account in accounts:
            # [username,ip,newPassword,readNewPasswordList_OS]
            username = account[0]
            ip = account[1]
            currentPassword = account[2]
            OS = account[3]

            # If this account is Win, and the plan for windows (.ps1), then true
            if OS == "Win" and plan[-2:] == "s1":
                # Login first
                l = writeLogin(username, ip, currentPassword)
                mainList.append(l)

                # Add the plan
                command = output
                l = writeCommands(command)
                mainList.append(l)

            elif OS == "Linux" and plan[-2:] == "sh":
                # Login first
                l = writeLogin(username, ip, currentPassword)
                mainList.append(l)

                # Add the plan
                command = output
                l = writeCommands(command)
                mainList.append(l)
            else:
                pass
    return mainList

def printList(mainList):
    for command in mainList:
        print(command)



def setup():
    s_input("Press any key to start..")
    print("Loading config files ..")
    # [OS, password]
    # Win:password123
    readNewPasswordList = readNewPassword()
    # [OS, username, ip, password]
    # Win:admin:10.1.2.1:CCDCsucks123#
    readCurrentUsersList = readCurrentUsers()


    # Start making the main list
    # Update the passwords
    # And make a list of the active accounts (accounts=[])
    mainList = []
    accounts = []
    if answer("Do you want to change all the users' passwords?"):

        print("writing all the new passwords.. ", end='')
        # Open Powershell, change all passwords
        mainList.append(writeOpenPowershell())
        mainList, accounts = changeAllPasswords(mainList, readCurrentUsersList, readNewPasswordList)
        print("Done")


    # Start making the plans list
    # Execute the plans accoring to the type of each account
    plans = []
    if answer("Do you want to use the 'plans' scripts?"):
        plans = setupPlans()
        mainList = executePlans(mainList, plans, accounts)


    if answer("Do you want to create new users from Config/NewUsers?"):
        mainList = addUsers(mainList, accounts)

    return mainList, plans

def saveList(mainList):
    print("Saving ..")
    filename = s_input("Enter filename")
    f = open(filename, 'w')
    for command in mainList:
        f.write(command)

def start():
    # Setup
    mainList, plans = setup()
    printList(mainList)
    saveList(mainList)


def main():
    start()
    pass

if __name__ == '__main__':
    main()

