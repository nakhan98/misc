#!/usr/bin/python
# Recompile and reload Intel igb network drivers after kernel upgrade
# New kernel will only be loaded after reboot so have this run at startup 

from os.path import isfile
import subprocess as sub
from shlex import split as sh_split
import os
import sys

cmd = sh_split("uname -a")
cmd2 = '''
rmmod -v igb; 
rm -rfv igb-*/;
tar -xvzf igb*.tar.gz && 
cd igb-*/src/ &&
make install &&
modprobe -v igb &&
/etc/init.d/networking restart;
cd ../../;
rm -rfv igb-*/;
'''
kernel_version_file = "./kernel_version.txt"
cur_dir = os.path.dirname(os.path.abspath(__file__))

def recompile_drivers():
    ret_value = sub.call(cmd2, shell=True)


def update_kernel_version_file():
    p = sub.Popen(cmd, stdout=sub.PIPE)
    output = p.communicate()
    open(kernel_version_file, "wt").write(output[0])


def kernel_change():
    p = sub.Popen(cmd, stdout=sub.PIPE)
    curr_ver = p.communicate()[0]
    version_in_file = open(kernel_version_file, "rt").read()
    if curr_ver == version_in_file:
        return False
    else:
        return True
    

def main():
    os.chdir(cur_dir)

    # Exit if not root
    if os.getuid() != 0:
        print("Root permissions required!")
        sys.exit(1)

    if not isfile(kernel_version_file):
        print("Kernel version file does not exist... will create now")
        #open(kernel_version_file, "wt").write("")
        update_kernel_version_file()
    else:
        if kernel_change():
            print("Detected kernel upgrade... recompiling network drivers\n\n")
            # run recompile function
            recompile_drivers()
            update_kernel_version_file()
        else:
            print("Kernel update has not occurred")


if __name__ == "__main__":
    main()
