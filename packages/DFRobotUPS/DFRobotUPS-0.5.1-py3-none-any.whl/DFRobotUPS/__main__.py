# DFRobotUPS.__main__



import argparse
import functools
import logging
import logging.handlers
import os
import sys
from time import sleep

import daemon

from . import (__version__, DFRobotUPS, DEFAULT_ADDR, DEFAULT_BUS, DETECT_OK,
               DETECT_NODEVICE, DETECT_INVALIDPID)



# --- constants ---



# default and ranges of values for command line parameters

DEFAULT_PERCENT = 7
DEFAULT_INTERVAL = 60
DEFAULT_RETRY = 10
DEFAULT_CMD = "/sbin/halt"

MIN_PERCENT = 5
MAX_PERCENT = 95

MIN_INTERVAL = 1
MAX_INTERVAL = 600


# percentage at which to log 'charged' message

CHARGED_PERCENT = 95



# --- functions ---



def sgn(n):
    """Return the sign of a number: 0 if it is 0, -1 if it is negative,
    or +1 if it is positive.
    """

    return 0 if n == 0 else -1 if n < 0 else 1



def int_range(min=0, max=100):
    """Factory function for range-checked integer.  This is useful for
    the 'type' argument for ArgumentParser.add_argument() to validate
    the input.
    """

    def int_range_check(s):
        v = int(s)
        if min <= v <= max:
            return v
        else:
            raise argparse.ArgumentTypeError(f"value not in range {min}-{max}")

    return int_range_check



def create_logger(shutdown, foreground, debug):
    """Create a return the logger for events.

    The logger will include stderr, if the program is running in the
    foreground (not in shutdown monitor mode, or running the monitor but
    not as a background daemon).  Logging to syslog will be included if
    running in shutdown monitor mode.
    """


    # create logger object and set the overall debugging level (we'll
    # override this in each handler, below, but this level stops
    # anything being logged that is less severe, in any handler)

    logger = logging.getLogger("DFRobotUPS")
    logger.setLevel(logging.DEBUG)


    # we log to stderr if we're not running in shutdown mode or we are,
    # but running in the foreground

    if (not shutdown) or foreground:
        # create logging handler with formatter for stderr - the level
        # here depends on the command line options specified

        stderr_loghandler = logging.StreamHandler(stream=sys.stderr)
        stderr_logformatter = logging.Formatter("%(levelname)s: %(message)s")
        stderr_loghandler.setFormatter(stderr_logformatter)
        stderr_loghandler.setLevel(logging.DEBUG if debug >= 2
                                    else logging.INFO if debug >= 1
                                    else logging.WARNING)


        # add the stderr handler as a logger destination

        logger.addHandler(stderr_loghandler)


    # create a syslog handler, if we're running in shutdown mode

    if shutdown:
        # create logging handler with formatter for syslog - we always log
        # at INFO level here

        syslog_loghandler = logging.handlers.SysLogHandler(address="/dev/log")
        syslog_logformatter = logging.Formatter(
                                "%(name)s[%(process)d]: %(message)s")
        syslog_loghandler.setFormatter(syslog_logformatter)
        syslog_loghandler.setLevel(logging.DEBUG if debug >= 2
                                    else logging.INFO)


        # add the syslog handler as a logger destination

        logger.addHandler(syslog_loghandler)


    return logger



def detect_ups(bus, addr, retry, logger):
    """Try to detect the UPS on the specified bus and I2C address,
    retrying if required.  A DFRobotUPS() object is returned, or None,
    if a UPS could not be found.
    """


    logger.info(f"searching for UPS HAT on bus {bus} at I2C address"
                f" 0x{addr:02x}")


    # loop, trying to detect the UPS

    tries = 0
    while True:
        tries += 1
        ups = DFRobotUPS(addr=addr, bus=bus)

        if ups.detect == DETECT_OK:
            break

        logger.warning(
            f"connection failed error code {ups.detect}"
            f" ({ups.detectstr()}), try {tries} of {retry}")

        # if we've run out of tries, stop
        if tries == retry:
            break

        sleep(1)


    # if the UPS could not be found, log the type of error encountered
    # and return None (for 'not found')

    if ups.detect != DETECT_OK:
        if ups.detect == DETECT_NODEVICE:
            logger.error("no device found at I2C address")

        elif ups.detect == DETECT_INVALIDPID:
            logger.error("device PID invalid for UPS HAT")

        else:
            logger.error(f"detection failed - unknown reason: {ups.detect}")

        return None


    # log some information about the UPS

    logger.info(f"UPS HAT found with product ID 0x{ups.pid:02x}, firmware"
                + (" version %d.%d" % ups.fwver))


    return ups



def setup(shutdown, foreground, debug):
    """Set up the logger and detect the UPS."""

    # create a logger appropriate to the mode we're running in
    logger = create_logger(shutdown=shutdown, foreground=foreground,
                        debug=debug)

    logger.info(f"startup: DFRobotUPS v{__version__}")

    # try to detect the UPS
    ups = detect_ups(bus=args.bus, addr=args.addr, retry=args.retry,
                     logger=logger)

    # abort if we couldn't find the UPS (detect_ups() will log an error)
    if ups is None:
        sys.exit(1)

    return ups, logger



def ups_monitor(ups, percent, interval, cmd, logger):
    """This function implements the main loop which polls the State of
    Charge (SoC) of the UPS battery and triggers the shutdown command,
    when it falls below the specified percentage.
    """

    logger.info(
        f"initial SoC {ups.soc:.2f}%, polling for shutdown at"
        f" {percent}% every {interval}s, shutdown command:"
        f" { ' '.join(cmd) }")

    # initialise current SoC and set the charge direction to 0 (= no
    # direction yet)
    last_soc = ups.soc
    soc_direction = 0

    while True:
        soc = ups.soc

        # if the SoC is lower than the shutdown percentage, break out of
        # the monitoring loop and execute the command
        if soc <= percent:
            break

        # work out if we're charging (+1), discharging (-1) or the
        # unchanged (0)
        new_soc_direction = sgn(soc - last_soc)
        if (new_soc_direction != 0) and (new_soc_direction != soc_direction):
            # there has been a change in SoC AND the direction the SoC
            # is changing has itself changed - log that
            if new_soc_direction < 0:
                logger.info("discharging: SoC falling from high of"
                            f" {last_soc:.2f}%")
            elif new_soc_direction > 0:
                logger.info("charging: SoC rising from low of"
                            f" {last_soc:.2f}%")

            # store the new direction as the current
            soc_direction = new_soc_direction

        # if we've just charged to 95% or more, consider us charged and
        # log a message
        if (last_soc < CHARGED_PERCENT) and (soc >= CHARGED_PERCENT):
            logger.info(f"charged: SoC is at {soc:.2f}%")

        # update the most recent SoC
        last_soc = soc

        # debug message (only logged if debugging enabled)
        logger.debug(f"current SoC {soc:.2f}% above shutdown threshold"
                     f" at {percent}% - sleeping for {interval}s")

        sleep(interval)

    logger.critical(
        f"shutdown: current SoC {soc:.2f}% has reached trigger at"
        f" {percent}% - executing:" f" { ' '.join(cmd) }")

    # execute the shutdown command, which will replace this process
    os.execv(cmd[0], cmd)

    # we'll never get here



def run(shutdown, foreground, percent, interval, cmd, debug):
    """Setup and monitor the UPS, triggering shutdown."""

    # set up the logger and detect the UPS
    ups, logger = setup(shutdown, foreground, debug)

    # run the main monitoring and shutdown loop
    ups_monitor(ups, percent, interval, cmd, logger)

    # we'll never get here




# --- parse arguments ---



parser = argparse.ArgumentParser(
    # override the program name as running this as a __main__ inside a
    # module # directory will use '__main__' by default - this name
    # isn't necessarily correct, but it looks better than that
    prog="DFRobotUPS",

    # text to display after the command line arguments help
    epilog="By default, the current charge status and battery voltage"
           " will be displayed and the program will terminate.  Using"
           " the -s option will cause the program to daemonise and"
           " poll the charge level and run a shutdown command, when it"
           " drops below a specified level."
    )

parser.add_argument(
    "-s", "--shutdown",
    action="store_true",
    help="run as a daemon and poll the battery SoC and initiate system "
         " shutdown when level drops below the defined level")

parser.add_argument(
    "-f", "--foreground",
    action="store_true",
    help="when running with the -s option, stay running in the"
         " foreground - don't run in the background as a daemon")

parser.add_argument(
    "-p", "--percent",
    type=int_range(MIN_PERCENT, MAX_PERCENT),
    default=DEFAULT_PERCENT,
    help="State of Charge (SoC) percentage at which to trigger shutdown"
         f" shutdown (min: {MIN_PERCENT}, max: {MAX_PERCENT}, default: "
         f" {DEFAULT_PERCENT})")

parser.add_argument(
    "-i", "--interval",
    type=int_range(MIN_INTERVAL, MAX_INTERVAL),
    default=DEFAULT_INTERVAL,
    help="number of seconds between polls of the battery SoC (min:"
         f" {MIN_INTERVAL}, max: {MAX_INTERVAL}, default:"
         f" {DEFAULT_INTERVAL})")

parser.add_argument(
    "-c", "--cmd",
    nargs="+",
    default=(DEFAULT_CMD, ),
    metavar=("CMD", "ARG"),
    help=f"command to run to trigger shutdown (default: {DEFAULT_CMD})")

parser.add_argument(
    "-a", "--addr",
    type=functools.partial(int, base=0),
    default=DEFAULT_ADDR,
    help="I2C address for UPS HAT; can be specified in hex as 0xNN"
         f" (default: 0x{DEFAULT_ADDR:02x})")

parser.add_argument(
    "-b", "--bus",
    type=int,
    default=DEFAULT_BUS,
    help=f"I2C SMBus number for UPS HAT (default: {DEFAULT_BUS})")

parser.add_argument(
    "-r", "--retry",
    type=int,
    default=DEFAULT_RETRY,
    help="number of times to try connecting to the UPS HAT (default:"
         f" {DEFAULT_RETRY})")

parser.add_argument(
    "-d", "--debug",
    action="count",
    default=0,
    help="increase debugging level (max: 2, default: 0)")

parser.add_argument(
    "-v", "--version",
    action="version",
    version=__version__)

args = parser.parse_args()



# --- main ---



# check if we're running in monitoring and shutdown mode

if args.shutdown:
    # warn if we're not root as we're unlikely to be able to shut the
    # system down

    if os.getuid() != 0:
        # create a temporary logger for this, with the foreground option
        # forced, to log to the terminal

        logger = create_logger(shutdown=args.shutdown, foreground=True,
                               debug=args.debug)

        logger.warning("not running as root - unlikely to be able to"
                       " execute shutdown command")


    # execute in either the foreground or as a daemon in the background

    if args.foreground:
        # we're running in the foreground - don't become a daemon
        run(shutdown=args.shutdown, foreground=args.foreground,
            percent=args.percent, interval=args.interval, cmd=args.cmd,
            debug=args.debug)

    else:
        # we're running as a daemon
        with daemon.DaemonContext():
            run(shutdown=args.shutdown, foreground=args.foreground,
                percent=args.percent, interval=args.interval, cmd=args.cmd,
                debug=args.debug)


# we're just in information mode, so just print that

ups, logger = setup(shutdown=args.shutdown, foreground=args.foreground,
                    debug=args.debug)

print(f"State of Charge (SoC) {ups.soc:.2f}%, battery voltage {ups.vcell}mV")
