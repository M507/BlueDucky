# BlueDucky
![logo](https://github.com/M507/BlueDucky/raw/master/p.png)
BlueDucky is a blue-team tool. It generates a list of USB-Rubber-Ducky instructions. 


The idea behind this tool is to create different payloads for each member as fast as possible.  Each member of the team will have a USB-Rubber-Ducky. Each member will be responsible of setting up different boxes. Here where the tool comes handy, the team can make a customized USB-Rubber-Ducky payload for each member. Payloads that run PowerShell and SSH into each box and execute a list of instructions for each box and making payloads will not take more than a minute before the competition.


The goal is to design the fastest incident response plan, which should include:
- Changing every user's password in every box.

- Executing customized scripts for:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Setting up firewall rules
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Setting up new users
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	You know the drill ...

### Setup
```sh
$ git clone https://github.com/M507/BlueDucky.git
$ cd BlueDucky
$ python3 BlueDucky.py
$ # Follow the instructions
..
..
Saving ..
Enter filename > output.txt
$ java -jar duckencode.jar -i output.txt -o inject.bin
$ cp inject.bin /<usb path>/
```

### Configuration
- All scrpits/plans must be is Config/
- Windows scrpits/plans must have .ps1 extension
- Linux scrpits/plans must have .sh extension
- BlueDucky/Config/startingAccounts file is where the default credentials should be.
```
Win:admin:10.1.2.1:CCDCsucks123#
Win:admin:10.1.2.5:CCDCsucks123#
Win:admin:10.1.2.10:CCDCsucks123#
Win:dnsUser:10.1.2.202:CCDCsucks123#
Linux:root:10.2.2.2:Admin123#
Linux:dnsadmin:10.2.2.202:Admin123#
```
- BlueDucky/Config/NewPasswords file must have two inputs, one for Windows users, and the other one for Linux:
```
Win:THISisTHEnewPASSWORD
Linux:UPDATEDpassword
```
- BlueDucky configers all users according to Config/NewPasswords file.

- BlueDucky/Config/NewUsers file is where the backup users shoud be, they will be created after chaning the password for the default users.
```
Win:Admin123:MyPasswordIs123456:1
Win:user1:123456:0
Linux:Admin:Password123456:1
Linux:user1:123456:0
```
- BlueDucky/Plans directory is where the firewall/anyscrpit scrpts should be.

### Support

- python3
- java
