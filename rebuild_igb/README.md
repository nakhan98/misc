# Automatic IGB Drivers Rebuild Script

This script was used to automatically rebuild the Intel igb network drivers after kernel upgrades on a recent Intel Server model running Ubuntu 10.04. We got DKMS working so it has since been retired. The script detects if there has been a kernel version change and then recompiles/reloads the Intel igb driver if necessary

# Installation #
- Create a directory in /home/user/ and copy this script and the intel igb tarball into it
- Run: sudo rebuild_igb.py
- To run automatically at startup, place following line in /etc/rc.local above 'exit 0' line:
(sleep 1m && python /home/user/directory_name/rebuild_igb.py) &

