from __future__ import print_function
from fabric.api import run, sudo, local, prompt, abort, env, roles, settings
import pexpect
import sys
import string
import time
import random
import getpass
import fabrichosts

# TODO 16-Mar-10: Change to a config file instead of importing as py module
fabrichosts.definehosts()

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

@roles('newslice')
def config_new_slice():
    """
    Configures a new Slicehost slice
    """
    # TODO 16-Mar-10: Refactor to make more modular
    root_password = getpass.getpass("Root's password given by SliceManager: ")
    admin_username = prompt("Enter a username for the admin user to create: ")
    admin_password = getpass.getpass("Enter a password for the admin user: ")
    env.user = 'root'
    env.password = root_password
    # Create the admin group and add it to the sudoers file
    admin_group = 'admin'
    run('addgroup --system {group}'.format(group=admin_group))
    run('echo "%{group} ALL=(ALL) ALL" >> /etc/sudoers'.format(
        group=admin_group)
    )
    # Create the new admin user (default group=username); add to admin group
    run('adduser {username} --disabled-password --gecos ""'.format(
        username=admin_username)
    )
    run('adduser {username} {group}'.format(
        username=admin_username,
        group=admin_group)
    )
    # Set the password for the new admin user
    run('echo "{username}:{password}" | chpasswd'.format(
        username=admin_username,
        password=admin_password)
    )
    # Disable logging in as root by locking root's password
    run('passwd --lock root')
    
    
    
    # TODO 16-Mar-10: Add code to create script to ssh into server. Better
    # yet, I should create a single script for SSHing into servers and
    # add a host_slug as a CLI argument

@roles('newslice')
def config_rebuilt_slice():
    """
    Configures a rebuilt Slicehost slice
    """
    # TODO 16-Mar-10: Need to also delete the entry in ~/.ssh/known_hosts
    with settings(disable_known_hosts=True):
        config_new_slice()

def remove_ip_from_known_hosts(ip_address):
    """
    Removes an IP address from ~/.ssh/known_hosts
    """
    # TODO 16-Mar-10: Develop remove_ip_from_known_hosts function
