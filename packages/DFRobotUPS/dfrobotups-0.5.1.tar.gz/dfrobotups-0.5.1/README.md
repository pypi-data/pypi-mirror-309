DFROBOTUPS MODULE
=================

It supports the DFRobotUPS HAT for the Raspberry Pi Zero (the more
sophisticated version for other Pis has not be checked nor tested) and
can retrieve information about the HAT itself, as well as dynamic data
for the current SoC (State of Charge) and cell voltage.

In addition, it can be run in a mode to poll the SoC and trigger a
shutdown command when it falls below a specified level.

This module contains can be used as a standalone utility or imported for
use in other scripts.

The module was developed and used under Python 3.9 on Raspberry PiOS
11.9 to support PiSCSI.

The information to write the module was taken from the DFRobotUPS wiki
at: https://wiki.dfrobot.com/UPS%20HAT%20for%20Raspberry%20Pi%20%20Zero%20%20SKU%3A%20DFR0528

Command line options
--------------------

The command line options listed with `--help` are shown below:

```
usage: DFRobotUPS [-h] [-s] [-f] [-p PERCENT] [-i INTERVAL] [-c CMD [ARG ...]]
                  [-a ADDR] [-b BUS] [-r RETRY] [-d] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -s, --shutdown        run as a daemon and poll the battery SoC and initiate
                        system shutdown when level drops below the defined
                        level
  -f, --foreground      when running with the -s option, stay running in the
                        foreground - don't run in the background as a daemon
  -p PERCENT, --percent PERCENT
                        State of Charge (SoC) percentage at which to trigger
                        shutdown shutdown (min: 5, max: 95, default: 7)
  -i INTERVAL, --interval INTERVAL
                        number of seconds between polls of the battery SoC
                        (min: 1, max: 600, default: 60)
  -c CMD [ARG ...], --cmd CMD [ARG ...]
                        command to run to trigger shutdown (default:
                        /sbin/halt)
  -a ADDR, --addr ADDR  I2C address for UPS HAT; can be specified in hex as
                        0xNN (default: 0x10)
  -b BUS, --bus BUS     I2C SMBus number for UPS HAT (default: 1)
  -r RETRY, --retry RETRY
                        number of times to try connecting to the UPS HAT
                        (default: 10)
  -d, --debug           increase debugging level (max: 2, default: 0)
  -v, --version         show program's version number and exit

By default, the current charge status and battery voltage will be displayed
and the program will terminate. Using the -s option will cause the program to
daemonise and poll the charge level and run a shutdown command, when it drops
below a specified level.
```

Author
------

Robert Franklin <rcf@mince.net>, UK
