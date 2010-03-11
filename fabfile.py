from fabric.api import run, sudo, local, prompt, abort

def questvcs():
    env.hosts = ['209.20.74.154']
    env.port = 9106

def host_type():
    run('uname -s')

def site_package():
    """
    Determine the site package
    """
    command = "python -c 'from distutils.sysconfig import get_python_lib; print get_python_lib()'"
    x = local(command)
    print x

def initial_slice_login():
    """
    Commands to execute on first login this is the only root login
    """
    pass

def reboot():
    reboot()