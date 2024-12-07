#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  Author: wh0ami
# License: MIT License <https://opensource.org/license/MIT>
# Project: https://codeberg.org/wh0ami/tibber-pulse-sml-debugger

import argparse
import sys
import traceback
from time import sleep

import requests
from loguru import logger
from smllib.errors import CrcError

import tibber_pulse_sml_debugger
from tibber_pulse_sml_debugger.exceptions import AuthenticationError
from tibber_pulse_sml_debugger.helper import fetch_data, percentage


def main() -> None:
    # initialize cli argument parser
    parser = argparse.ArgumentParser(
        description="A tiny python based CLI application to see the data, that was recorded and send by your Tibber Pulse IR to your Tibber Pulse Bridge.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # read cli parameters
    parser.add_argument(
        "-a",
        "--address",
        metavar="<hostname or IP address>",
        type=str,
        required=True,
        help="The hostname or IP address of your Tibber Pulse Bridge. Please note, that the local webserver must be activated.",
    )
    parser.add_argument(
        "-u",
        "--username",
        metavar="<username>",
        type=str,
        default="admin",
        required=False,
        help="The username of your Tibber Pulse Bridge web server. Defaults to the factory default 'admin'.",
    )
    parser.add_argument(
        "-p",
        "--password",
        metavar="<password>",
        type=str,
        required=True,
        help="The password of your Tibber Pulse Bridge web server.",
    )
    parser.add_argument(
        "-n",
        "--node-id",
        metavar="<Pulse IR node ID>",
        type=int,
        default=1,
        required=False,
        help="The Node ID of your Tibber Pulse IR. Defaults to 1, which is not correct some times. You will find the Node ID in the web interface of your Tibber Pulse Bridge.",
    )
    parser.add_argument(
        "-i",
        "--interval",
        metavar="<amount of seconds>",
        type=int,
        default=1,
        required=False,
        help="The interval for polling the API of your Tibber Pulse Bridge. Defaults to one second.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Whether all meter data should be logged to stdout.",
    )

    # actually parse the arguments that were passed
    args = parser.parse_args(sys.argv[1:])

    # configure the logger
    logger.remove()
    logger.add(sys.stdout, level="DEBUG" if args.debug else "INFO")

    # initialize requests for authentication against the bridge
    session = requests.Session()
    session.auth = (args.username, args.password)

    # initialize all counters
    responses_total = 0
    responses_with_crc_errors = 0
    responses_with_empty_sml_frames = 0
    responses_with_other_errors = 0
    exit_code = 0

    # run the actual application logic
    try:
        while True:
            try:
                responses_total += 1
                response = fetch_data(
                    session=session,
                    node_id=args.node_id,
                    address=args.address,
                )
                logger.info("Valid SML data received!")
                logger.debug("+++ SML DATA +++")
                for result in response:
                    logger.debug(result)
            except AttributeError:
                responses_with_empty_sml_frames += 1
                logger.error("Bytes missing / SML frame is empty object!")
            except CrcError:
                responses_with_crc_errors += 1
                logger.error("Data invalid / CrcError while validating the SML frame!")
            except Exception as exception:
                responses_with_other_errors += 1
                raise exception
            finally:
                sleep(args.interval)
    except KeyboardInterrupt:
        pass
    except requests.exceptions.ConnectionError:
        logger.error(
            "Timeout while connecting to your Tibber Pulse Bridge. Have you activated the web server in your Tibber Pulse Bridge?"
        )
        exit_code = 1
    except AuthenticationError:
        logger.error("Passed username or password was rejected by your Tibber Pulse Bridge!")
        exit_code = 2
    except Exception:
        logger.error(traceback.format_exc())
        exit_code = 3
    finally:
        logger.info("+++ STATISTICS +++")
        responses_valid = (
            (responses_total - responses_with_empty_sml_frames) - responses_with_crc_errors
        ) - responses_with_other_errors
        logger.info(f"Total responses: {responses_total}")
        logger.info(f"Valid responses: {responses_valid} ({percentage(responses_total, responses_valid)})")
        logger.info(
            f"Empty responses: {responses_with_empty_sml_frames} ({percentage(responses_total, responses_with_empty_sml_frames)})"
        )
        logger.info(
            f"CrcError responses: {responses_with_crc_errors} ({percentage(responses_total, responses_with_crc_errors)})"
        )
        logger.info(
            f"Responses with other errors: {responses_with_other_errors} ({percentage(responses_total, responses_with_other_errors)})"
        )
        sys.exit(exit_code)


# run the main class
if __name__ == "__main__":
    main()
