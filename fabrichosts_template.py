from __future__ import print_function
from fabric.api import env, roles

# Template showing format used for the fabrichosts.py file
def definehosts():
    env.roledefs = {
        'newslice': ['xxx.xx.xx.xxx'],
        'slices': ['xxx.xx.xx.xxx', 'xxx.xx.xx.xxx']
    }
