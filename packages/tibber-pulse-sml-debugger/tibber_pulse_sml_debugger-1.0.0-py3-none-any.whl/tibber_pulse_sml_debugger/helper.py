#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  Author: wh0ami
# License: MIT License <https://opensource.org/license/MIT>
# Project: https://codeberg.org/wh0ami/tibber-pulse-sml-debugger

import requests
import smllib.sml.response_get_list
from smllib import SmlStreamReader, const

from tibber_pulse_sml_debugger.exceptions import AuthenticationError


def percentage(total: int, part: int) -> str:
    """
    Calculate and format the percentage of two integers.

    :param total: The total amount for the percentage calculation.
    :param part: The part amount for the percentage calculation.
    :return: The percentage of the part value from the total value as a string, followed by the % symbol.
    """
    percentage_value = round((part / (total / 100)), 2)
    return f"{percentage_value}%"


def fetch_data(session: requests.Session, address: str, node_id: int) -> list[str]:
    """
    Fetch and process the SML data from a Tibber Pulse Bridge web server.

    :param session: The requests session with the auth data.
    :param address: The hostname or IP address of the Tibber Pulse Bridge web server.
    :param node_id: The node ID of the Tibber Pulse IR.
    """
    raw_sml_data = session.get(f"http://{address}/data.json?node_id={node_id}", timeout=10)
    if raw_sml_data.status_code == 401:
        raise AuthenticationError()

    sml_stream = SmlStreamReader()
    sml_stream.add(raw_sml_data.content)

    sml_frame = sml_stream.get_frame()

    results = []

    parsed_sml_messages = sml_frame.parse_frame()
    for message in parsed_sml_messages:
        if isinstance(message.message_body, smllib.sml.response_get_list.SmlGetListResponse):
            for list_entry in message.message_body.val_list:
                if list_entry.obis in const.OBIS_NAMES:
                    obis_name = const.OBIS_NAMES[list_entry.obis]
                else:
                    continue
                if list_entry.unit and list_entry.unit in const.UNITS:
                    obis_unit = const.UNITS[list_entry.unit]
                else:
                    obis_unit = ""
                results.append(f"{obis_name} -> {list_entry.get_value()} {obis_unit}")
    return results
