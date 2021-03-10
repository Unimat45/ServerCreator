import os
import urllib.request as _urllib
from getpass import getuser

LstAwnsers = ["y", "n"]

while True:
    path = str(input("Enter new server's path : "))
    
    if path != "":
        if path.startswith("~"):
            path = path.replace("~", f"/home/{getuser()}")
            
        if path.startswith("/"):
            pathName = path.split("/")[-1]

        else:
            path = f"{os.getcwd()}/{path}"
            pathName = path.split("/")[-1]

        pathName = pathName.replace(" ", "")

        if not os.path.isdir(path):
            try:
                os.makedirs(path)
            except OSError:
                print("Error while creating folders. You may need to run this using sudo!")
                os._exit(1)
        try:
            os.chdir(path)
        except OSError:
            print("Error while changing directory")
            os._exit(1)
        else:
            break


urlStart = "https://raw.githubusercontent.com/Unimat45/ServerCreator/main/start.sh"
file = _urllib.urlopen(urlStart)
lines = ""
for line in file:
    lines += line.decode("utf-8")
lines = lines.replace("PATH", path)
lines = lines.replace("\"NAME\"", pathName)
with open("start.sh", "w") as f:
    f.write(lines)


urlRestart = "https://raw.githubusercontent.com/Unimat45/ServerCreator/main/restart.sh"
file = _urllib.urlopen(urlRestart)
lines = ""
for line in file:
    lines += line.decode("utf-8")
lines = lines.replace("PATH", path)
lines = lines.replace("\"NAME\"", pathName)
with open("restart.sh", "w") as f:
    f.write(lines)


urlStop = "https://raw.githubusercontent.com/Unimat45/ServerCreator/main/stop.sh"
file = _urllib.urlopen(urlStop)
lines = ""
for line in file:
    lines += line.decode("utf-8")
lines = lines.replace("PATH", path)
lines = lines.replace("\"NAME\"", pathName)
with open("stop.sh", "w") as f:
    f.write(lines)

os.system("chmod +x *")

'''
sources = os.popen("cat /etc/apt/sources.list").read().find("deb [trusted=yes] http://pfk.ddns.net/deb ./")

if sources == -1:
    try:
        os.system("echo \"deb [trusted=yes] http://pfk.ddns.net/deb ./\" | sudo tee -a /etc/apt/sources.list > /dev/null")
    except OSError:
        print("Could not add repo to sources file. Run this program with sudo to do so!")
    else:
        os.system("sudo apt-get update")
        os.system("sudo apt install paperupdater")
'''

while True:
    Backup = str(input("Create backups? (y/n): ")).lower()

    if Backup not in LstAwnsers:
        print("Please enter a valid awnser!")
    else:
        break

if Backup == "y":
    while True:
        backupPath = str(input("Enter path to backup : "))
    
        if backupPath != "":

            if backupPath.startswith("~"):
                backupPath = backupPath.replace("~", f"/home/{getuser()}")
                
            elif not backupPath.startswith("/"):
                backupPath = f"{os.getcwd()}/../{backupPath}"

            if not os.path.isdir(backupPath):
                
                print(f'Path "{backupPath.replace(f"{pathName}/../", "")}" doesn\'t exist!')

                while True:
                    createBackup = str(input("Create folder? (y/n): ")).lower()

                    if Backup not in LstAwnsers:
                        print("Please enter a valid awnser!")

                    elif createBackup == "y":
                        os.makedirs(backupPath)
                        break

                    else:
                        break

                if createBackup == "y":
                    break
            else:
                break

    with open("start.sh", "r") as f:
        start = f.read().splitlines()

    start.insert(28, 'echo "Backing up server"')
    start.insert(29, f'tar -pzcf {backupPath}/$(date +%Y.%m.%d.%H.%M.%S).tar.gz world world_nether world_the_end\n')
    wStart = ""

    for lines in start:
        wStart += lines + "\n"

    with open("start.sh", "w") as f:
        f.write(wStart)

    crontab = os.popen("crontab -l").read().find(f"0 2 * * * {path}/start.sh")

    if crontab == -1:
        os.system(f'(crontab -l 2>/dev/null; echo "0 2 * * * {path}/restart.sh") | crontab - 2>/dev/null')