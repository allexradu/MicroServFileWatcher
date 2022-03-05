# MicroServ File Watcher

MicroServ File Watcher is a huge help when you have to copy a common code in development of Micro Services It
synchronizes the mirrors file changes to all your microservices.

Let's say you have the following folder structure...

+ Microservices/Auth/Common
+ Microservices/Products/Common
+ Microservices/Orders/Common

and you want when you make a change to either of the common folder to be reflected to all the other folders, that's
where MicroServ FileWatcher shines.

The command is: 

`python main.py arg1 arg2 arg3 arg4`

arg1: Name of the common folder (e.g. Common)

arg2: The file extensions to monitor 

arg3: The list of sub folders to monitor (e.g. Auth, Products, Orders) separated by
| as a string 

arg4: THe path of the main folder (e.g. /Users/user/python/Microservices/)

Example:

`python main.py Common "txt|js|ts" "Auth|Products|Orders" /Users/user/python/Microservices/`

Dev:

### Allex Radu
