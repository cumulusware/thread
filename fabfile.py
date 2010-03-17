from __future__ import print_function
from fabric.api import run, sudo, local, prompt, abort, env, roles, \
    settings, cd
import pexpect
import sys
import string
import time
import random
import getpass
import fabrichosts

# TODO 16-Mar-10: Refactor to add unit testing
# TODO 16-Mar-10: Add license information
# TODO 16-Mar-10: Fix Fabric err: stdin: is not a tty

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
    """
    Reboot the server
    """
    reboot()

@roles('newslice')
def config_new_slice():
    """
    Configures a new Slicehost slice
    """
    # TODO 16-Mar-10: Refactor to not throw errors if rerun on a slice that
    # has already been configured.
    # TODO 16-Mar-10: Refactor to make more modular
    root_password = getpass.getpass("Root's password given by SliceManager: ")
    admin_username = prompt("Enter a username for the admin user to create: ")
    admin_password = getpass.getpass("Enter a password for the admin user: ")
    new_ssh_port = prompt("Enter the port to use for SSH (Default=22): ")
    env.user = 'root'
    env.password = root_password
    # Create the admin and ssher groups and add admin to the sudoers file
    admin_group = 'admin'
    ssher_group = 'sshlogin'
    run('addgroup --system {group}'.format(group=admin_group))
    run('addgroup --system {group}'.format(group=ssher_group))
    run('echo "%{group} ALL=(ALL) ALL" >> /etc/sudoers'.format(
        group=admin_group)
    )
    # Set the default editor to vim.tiny
    run('update-alternatives --set editor /usr/bin/vim.tiny')
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
    # TODO 16-Mar-10: Add commands to configure the default editor
    # Interactively, the command I used was `update-alternatives --config
    # editor`
    
    # Change to using the new admin user
    env.user = admin_username
    env.password = admin_password
    # This will be the first time logging in under the admin_username
    # The next command confirms that we can ssh in as admin_username
    # and locks root's password for increased security.
    # From now on we must SSH into the slice using an admin or ssher.
    sudo('passwd --lock root')
    # Change the SSH port
    # TODO 16-Mar-10: Refactor to not use Perl
    sudo("{cmd} 's/{find}/\\1 {ssh_port}/g' {file}".format(
        cmd='perl -pi -e',
        find='(Port)\s+22$',
        ssh_port=new_ssh_port,
        file='/etc/ssh/sshd_config')
    )
    # Only allow SSH login for the groups admin and sshlogin
    sudo("{cmd} 's/{find}/\\1 no/g' {file}".format(
        cmd='perl -pi -e',
        find='(PermitRootLogin)\s+yes$',
        file='/etc/ssh/sshd_config')
    )
    replacement_string = 'AllowGroups {admins} {sshers}'.format(
        admins=admin_group,
        sshers=ssher_group
    )
    sudo("{cmd} 's/{find}/\\1\\n{replace}/g' {file}".format(
        cmd='perl -pi -e',
        find='(# Authentication:)$',
        replace=replacement_string,
        file='/etc/ssh/sshd_config')
    )
    # Reload ssh
    sudo('/etc/init.d/ssh reload')
    env.port = new_ssh_port
    # Install standard packages
    # TODO 16-Mar-10: Refactor to read config file of packages to install
    package_install_options = '--quiet --install-recommends --assume-yes'
    packages_to_install = (
        'git-core',
        'members',
        'apt-show-versions',
        'zip',
        'unzip',
    )
    for install_package in packages_to_install:
        sudo("apt-get install {options} {package}".format(
            options=package_install_options,
            package=install_package)
        )
    # Customize BASH using dot-files github project
    dest_dir = '~/src/dot-files.github.cumulusware'
    run('mkdir -p {dir}'.format(dir=dest_dir))
    run('git clone {repo} {install_to}'.format(
        repo='git://github.com/cumulusware/dot-files.git',
        install_to=dest_dir)
    )
    with cd('{dir}'.format(dir=dest_dir)):
        run('./deploy-dot-files.py')
    
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
