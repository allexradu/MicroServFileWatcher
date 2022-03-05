# MicroServ File Watcher

MicroServ File Watcher is a huge help when you have to copy a common code in development of Micro Services It
synchronizes the file changes to all your microservices.

### [Download the Windows Distribution](https://github.com/allexradu/MicroServFileWatcher/tree/main/dist/windows)

### [Download the Mac OS X Distribution](https://github.com/allexradu/MicroServFileWatcher/tree/main/dist/mac)

Let's say you have the following folder structure...

+ Microservices/Auth/Common
+ Microservices/Products/Common
+ Microservices/Orders/Common

and you want when you make a change to either of the common folder to be reflected to all the other folders, that's
where MicroServ FileWatcher shines.

The command is:

`ms arg1 arg2 arg3 arg4`

arg1: Name of the common folder (e.g. Common)

arg2: The file extensions to monitor separated by | (e.g. txt|js|ts)

arg3: The list of sub folders to monitor (e.g. Auth, Products, Orders) separated by | as a string

arg4: THe path of the main folder (e.g. /Users/user/python/Microservices/)

Example:

`ms Common "txt|js|ts" "Auth|Products|Orders" /Users/user/python/Microservices/`

## Installation:

### Windows:

Copy the ms.exe on your C: folder and add the file to the [Path](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)

Use the ms command in the Command Prompt

### Mac OSX:

Copy the ms file to:

`/usr/local/bin`

Use the md command in the terminal

### Dev: Allex Radu
