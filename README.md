RPM Controller
==============

RPM Controller is a utillity that take control of all RPM's installed, erased and updated in the machine, this information goes to a central MongoDB Node

Version
-------

1.0

Tech
----

RPM Controller use this technologies:

* [Python] - Awesome developing languaje, supported from 2.4.3 
* [CentOS/RHEL] - Supported from Rhel 5.5, and CentOS 5.5
* [rpm_api] - Own Library that take information about rpm's of the node
* [Pymongo] - Great module that talks with MongoDB
* [Argparse] - Argument parser Module

Installation
--------------
How to install [rpmController][1]:
```sh
git clone git@pdihub.hi.inet:troitino/rpmControler.git
```
or:
```sh
yum install rpmController
```

This module needs the rpm module of CentOS/RedHat/Fedora, then you need to use the native python version of your SO, 
* [RHEL 5.X/CentOS 5.X] - python 2.4.3 with rpms pymongo, python-argparse and python-bson
* [RHEL 6.X/CentOS 6.X] - python 2.6.6 with the same name of rpms but not the same content
* Both of them with all dependencies in artifacts </others/rpmcontroller/{5.X|6.X}/x86_64>

##### Configure file:

* conf/rpmController.ini

```sh
[mongo]
 ip = 127.0.0.1    --> IP of MongoDB Node
 port = 27017      --> Port of MongoDB Node
 database = rpmdb  --> Database Name
```

Execution
--------------
By default RPM Controller search RPMs in the system and registry in a MongoDB
* rpmcontroller --> Search rpms and take it to MongoDB
* rpmcontroller -f <pattern> --> Search RPMs in MongoDB
* debug mode --> log all actions in /var/log/rpmcontroller.log (Default deactivated)

Help:
```sh
Optional arguments:
  -h, --help            show this help message and exit
  -f pattern, --find pattern
                        Pattern to search in MongoDB
  -c, --check           Check if there are new rpms in node
  -d, --debug           Debug Mode
  --version             show program's version number and exit
```

Authors:
----
* Juan Manuel Parrilla: [Profile][JP_PDI] [Twitter][@kerbeross]
* Francisco García Troitiño: [Profile][FGT_PDI]


License
----

MIT

*Free Software, Hell Yeah!*

  [JP_PDI]: https://github.com/padajuan
  [@kerbeross]: http://twitter.com/@kerbeross
  [FGT_PDI]: https://github.com/ftroitino
  [1]: https://github.com/padajuan/rpmController
  [Pymongo]: https://github.com/mongodb/mongo-python-driver
  [Argparse]: https://code.google.com/p/argparse
  [Python]: http://www.python.org/
  [CentOS/RHEL]: http://www.centos.org/
