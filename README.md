# README #

* **Project:** Thread
* **Goal:** Manage and deploy Ubuntu servers

## Purpose ##

The goal is to create a quick, repeatable, automated process to manage Ubuntu servers running on either local hardware or [Slicehost][] VPS slices. Thread uses the [Fabric][] Python "library and command-line tool designed to streamline deploying applications or performing system administration tasks via SSH."

## Installation ##

These are *rough* instructions for installing Fabric and Thread in a virtualenv.

1. Install virtualenv, virtualenvwrapper, and pip (Jesse Noller provides good instructions in his article [SO YOU WANT TO USE PYTHON ON THE MAC?][noller-python])
2. `mkvirtualenv thread`
3. `git clone git://github.com/cumulusware/thread.git` to whatever directory you want to use to store Thread
4. `fab -l` to list the available commands
5. Copy `fabrichosts_templates.py` to `fabrichosts.py` and customize for your hosts and roles
5. To configure a fresh slice, add the slice's IP to the `newslice` role in `fabrichosts.py` and then execute the `fab config_new_slice` command.


[slicehost]: http://www.slicehost.com/

[fabric]: http://www.fabfile.org/

[noller-python]: http://jessenoller.com/2009/03/16/so-you-want-to-use-python-on-the-mac/