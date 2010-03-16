from __future__ import print_function
from fabric.api import run, sudo, local, prompt, abort, env, roles, settings
import pexpect
import sys
import string
import time
import random
import getpass
import fabrichosts

fabrichosts.definehosts()

def hostsfile(group):
    """Loads a group of hosts from a config file.
    group: name of the group file, one host per line
    """
    base_dir = '~/.dsh/group/'
    
    from os.path import join, abspath, expanduser
    
    filename = abspath(expanduser(join(base_dir, group)))
    try:
        fhosts = open(filename)
    except IOError:
        abort('file not found: %s' % filename)
    
    def has_data(line):
        """'line' is not commented out and not just whitespace."""
        return line.strip() and not line.startswith('#')
    
    config.fab_hosts = [ line.strip() for line in fhosts
                        if has_data(line)]
    

def _host_type():
    run('uname -s')

def site_package():
    """
    Determine the site package
    """
    command = "python -c 'from distutils.sysconfig import get_python_lib; print get_python_lib()'"
    x = local(command)
    print(x)

def new_user(username, admin=False):
    """
    Command to add a user with a home directory on Linux system using adduser
    
    Run this command with fab host new_user:<username>
    
    """
    run('adduser {username} --disabled-password --gecos ""'.format(
        username=username)
    )

def reboot():
    reboot()

# Steps that are taken the first time you log into a slice
# 0. ssh root@<sliceip>
# 1. Asked to add the RSA key fingerprint (yes/no)
# 2. Enter the root password given by Slicehost
# 3. Create the admin/sshers groups: `addgroup admin` and `addgroup sshers`
# 4. Add the admin group to the sudoers file with:
#   `EDITOR=vi visudo`
#   %admin ALL=(ALL) ALL
# 5. Create a new admin user with `adduser <username>` and answer questions
#   Can Fabric handle the questions that are asked when creating a new user?
#   Fabric cannot handle answering questions the way that pyExpect does.
#   Therefore, I should use useradd which isn't interactive. The adduser
#   command is an Ubuntu only command, so instead I should use the more
#   generic Linux/UNIX useradd command. The adduser command does:
#   1. Adds user <username> given
#   2. Adds a new group <username>
#   3. Adds user <username> to the group <username>
#   4. Creates the home directory /home/<username>
#   5. Copies files from /etc/skel to the home directory
#   The other option is to use adduser in a non-interactive mode
#       adduser <username> --disabled-password --gecos ""
# 6. Add the admin user to the admin group with `adduser <username> admin`
# 7. Remove the password from the root user with `passwd --lock root`

@roles('newslice')
def config_new_slice():
    """
    Configures a new Slicehost slice
    """
    root_password = getpass.getpass("Root's password given by SliceManager: ")
    admin_username = prompt("Enter a username for the admin user to create: ")
    admin_password = getpass.getpass("Enter a password for the admin user: ")
    env.user = 'root'
    env.password = root_password
    admin_group = 'admin'
    new_user(admin_username, True)
    run('addgroup {group}'.format(group=admin_group))
    run('adduser {username} {group}'.format(
        username=admin_username,
        group=admin_group)
    )
    run('echo "{username}:{password}" | chpasswd'.format(
        username=admin_username,
        password=admin_password)
    )
    run('echo "%{group} ALL=(ALL) ALL" >> /etc/sudoers'.format(
        group=admin_group)
    )
    run('passwd --lock root')

@roles('newslice')
def config_rebuilt_slice():
    """
    Configures a rebuilt Slicehost slice
    """
    with settings(disable_known_hosts=True):
        config_new_slice()

def remove_ip_from_known_hosts(ip_address):
    """
    Removes an IP address from ~/.ssh/known_hosts
    """
    
