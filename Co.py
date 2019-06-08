import subprocess
import os.path


"""
Stylish input()
"""
def s_input(string):
    return input(string+">").strip("\n")


"""
Execute command locally
"""
def execute_command(command):
    if len(command) > 0:
        print(command)
        proc = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
        return proc

"""
Get all subdirectories of a directory.
"""
def getSubs(dirname):
    print("getSubs")
    dirs = [d for d in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, d))]
    # subdirectories = [dirname + "/" + subDirName for subDirName in subdirectories]
    subdirectories = []
    for dir in dirs:
        subdirectories.append(dirname + '/' + dir)
    return subdirectories

"""
Get all files of a directory.
"""
def getFiles(dirname):
    return [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]


"""
Rocket science
"""
def answer(string):
    a = input(string)
    if a == "Y" or a == 'y' or a == 'Yes' or a == 'yes':
        return True
    else:
        return False

"""
Rocket science
"""
def answerExit(string):
    if string == "exit" or string == "Exit" or string == "q" or string == "Q":
        return True
    else:
        return False

