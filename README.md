# README #

Project: Thread
Purpose: Fabric based management of Mac OS X local client and Ubuntu servers
Author: Matthew Rankin

## Purpose ##

The goal is to create a quick, repeatable, automated process to manage both my local Mac OS X client used for development and various Ubuntu servers. The Ubuntu servers that need to be managed are both running on [Slicehost][slicehost] and local hardware. Thread uses the [Fabric][fabric] Python "library and command-line tool designed to streamline deploying applications or performing system administration tasks via SSH."

## Dependencies ##

The following were used in the development of Thread:

* Python
* Fabric 1.0 dev (cloned from github)
    * Paramiko=1.7.4
    * PyCrypto>=1.9
* Virtualenv
* Pip
* Nose

[slicehost]: http://www.slicehost.com/

[fabric]: http://www.fabfile.org/