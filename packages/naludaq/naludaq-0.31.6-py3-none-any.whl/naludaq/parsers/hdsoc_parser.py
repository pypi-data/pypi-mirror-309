"""ASoCv3Parser

Use parser to parse the data from the Hardware.
The boards sends a raw bitstream and it needs to be parsed into events.
The parser class is a tool to parse the raw bitstream of 8-bit chunks
into 16 bit words then extracting the 12-bit data, the header info,
channels and window number data.

This data is then returned in a dictionary.
The raw data is preserved.

This module was previously located under the naludaq.daq.workers
subpackage, and was relocated to improve the organization of the
naludaq package.
"""

import logging
from collections import defaultdict
from typing import List

import numpy as np

from naludaq.helpers.exceptions import BadDataError
from naludaq.parsers.parser import Parser

LOGGER = logging.getLogger("naludaq.hdsoc_parser")


class HDSoCParser(Parser):
    def __init__(self, params):
        super().__init__(params)
        self._stop_word = params.get("stop_word", b"\xfa\x5a")
        if isinstance(self._stop_word, str):
            self._stop_word = bytes.fromhex(self._stop_word)
        self._chan_mask = params.get("chanmask", 0x3F)
        self._chan_shift = params.get("chanshift", 0)
        self._abs_wind_mask = params.get("abs_wind_mask", 0x3F)
        self._evt_wind_mask = params.get("evt_wind_mask", 0x3F)
        self._evt_wind_shift = params.get("evt_wind_shift", 6)
        self._headers = params.get("headers", 4)
        self._timing_mask = params.get("timing_mask", 0xFFF)
        self._timing_shift = params.get("timing_mask", 12)
        self._packet_size = params.get("packet_size", 72)

    def _validate_input_package(self, in_data):
        """HDSoC: Splits the input package into a list of packets,
        and validates each packet based on a fixed size. Returns
        a list of only valid packets.

        Args:
            in_data (dict): Raw event structure from packager

        Raises:
            BadDataError: If all packets are bad

        Returns:
            split_in_data (list): List of validated packets
        """
        split_in_data = self._split_rawdata_into_packets(in_data["rawdata"])
        for packet in split_in_data:
            if len(packet) != self._packet_size:
                split_in_data.remove(packet)
        if split_in_data == []:
            raise BadDataError("Input package has no valid packets")
        return split_in_data

    def parse_digital_data_old(self, in_data) -> dict:
        """Parse the raw data from the board.

        Since the data packets are constant length, we can extract the data
        in place with matrix operations, speeding up the parsing.

        Args:
            in_data (bytearray): Raw data from the board

        Returns:
            Parsed event as a dict.

        Raises:
            BadDataException if no data is found or if the data contains errors.
        """
        try:
            input_packets = self._validate_input_package(in_data)
        except:
            raise

        num_packets = len(input_packets)
        raw_data = np.frombuffer(np.array(input_packets).flatten(), dtype=">H")
        raw_data = np.reshape(
            np.array(raw_data, dtype="uint16"), (num_packets, self._packet_size // 2)
        )

        abs_wind_mask = self._abs_wind_mask
        evt_wind_mask = self._evt_wind_mask
        evt_wind_shift = self._evt_wind_shift
        chan_shift = self._chan_shift
        chan_mask = self._chan_mask
        timing_mask = self._timing_mask
        timing_shift = self._timing_shift
        headers = self._headers

        curr_event = {
            "window_labels": [[] for _ in range(self.params["channels"])],
            "evt_window_labels": [[] for _ in range(self.params["channels"])],
            "data": [[] for _ in range(self.params["channels"])],
            "timing": [[] for _ in range(self.params["channels"])],
            "time": [[] for _ in range(self.params["channels"])],
        }

        current_time_dict = defaultdict(int)
        for packet in raw_data:
            # If all data bytes are zero the window comes from a disabled channel.
            if np.all(packet[headers:] == 0):
                continue

            channel = (packet[0] >> chan_shift) & chan_mask
            abs_window = packet[3] & abs_wind_mask
            evt_window = (packet[3] >> evt_wind_shift) & evt_wind_mask
            timing = (int(packet[1] & timing_mask) << timing_shift) | int(
                packet[2] & timing_mask
            )

            time_multiplier = current_time_dict[channel]
            current_time_dict[channel] = time_multiplier + 1
            time = np.arange(
                time_multiplier * self.samples, (time_multiplier + 1) * self.samples
            )

            curr_event["window_labels"][channel].append(abs_window)
            curr_event["evt_window_labels"][channel].append(evt_window)
            curr_event["timing"][channel].append(timing)
            curr_event["data"][channel].extend(packet[headers : headers + self.samples])
            curr_event["time"][channel].extend(time)
        curr_event["data"] = [np.array(x) for x in curr_event["data"]]
        return curr_event

    def _split_rawdata_into_packets(self, rawdata: bytearray) -> List[bytearray]:
        """Splits raw event data into packets.

        Args:
            rawdata (bytearray): the raw data to split

        Returns:
            A list of raw packets.
        """
        return rawdata.split(self._stop_word)

    def _fix_missing_data(self, event):
        samples = self.params["samples"]
        channels = self.channels

        maxlen = max([len(x) for x in event["data"]])

        time_axis = np.full(shape=(channels, maxlen), fill_value=np.nan)
        data_axis = np.full(shape=(channels, maxlen), fill_value=np.nan)
        for chan, (data, label) in enumerate(
            zip(event["data"], event["window_labels"])
        ):
            if len(data) == 0:
                continue
            if len(data) == maxlen:
                data_axis[chan] = data
                time_axis[chan] = np.arange(0, maxlen)
                continue
            # Replace the below with correct algorithm
            label = np.array(label)
            mwin = self.missing_window(label)
            if mwin != 0 or mwin != len(label):
                data_axis[chan, : mwin * samples] = data[: mwin * samples]
                data_axis[chan, (mwin + 1) * samples :] = data[mwin * samples :]
            elif mwin == 0:
                data_axis[chan] = data[samples:]
            elif mwin == len(label):
                data_axis[chan] = data[:samples]

            time_axis[chan, : mwin * samples] = np.arange(0, mwin * samples)
            time_axis[chan, (mwin + 1) * samples :] = np.arange(
                (mwin + 1) * samples, maxlen
            )

        return time_axis, data_axis

    def _fix_missing_windows(self, event: dict) -> int:
        """Find the index of the missing windows in the labels.

        Args:
            labels: input labels in an array without the correct ordering
            max_windows: the maximum windows before rolling over
            group_size: channel group of channels operating in the same clock domain
        """
        labels = event["window_labels"]
        max_windows = self.params["windows"]
        # group_size = self.params.get(
        #     "group_size", 16
        # )  # Should be used to align all channels in the same group

        channels = len(labels)
        maxlabels = max([len(x) for x in labels])
        output = np.full(shape=(channels, maxlabels), fill_value=np.nan)
        for i, row in enumerate(labels):
            prev = row[0]
            output[i][0] = row[0]
            dist = 0
            j_prev = 0
            for j, y in enumerate(row[1:]):
                # check if rolling over
                # check distance from previous
                if prev == (max_windows - 1):
                    if y == 0:
                        dist = 1
                    else:
                        dist = y
                    prev = y
                elif np.isnan(y):
                    prev = np.nan
                    dist = 0
                    j_prev = j
                    continue
                else:
                    dist = y - prev
                    prev = y

                index = int(j_prev + dist)
                output[i][index] = y
                j_prev = index

        return output

    def _add_xaxis_to_event(self, event):
        """Adds an x-axis to the data.

        Based on the amount of channels and samples it will add a timeaxis
        per channel to the event dict.

        During certain readout modes the window labels are not aligning,
        This function accounts for that and moves the time axis accordingly.

        It uses the window labels to determine the time axis by finding the lowest
        window number and offsetting the time axis by that amount.
        The 0-time will be the first samples in the lowest window.

        Args:
            event (dict): The event to add the x-axis to.

        Returns:
            numpy array with sample numbers for each channel.
        """
        channels = self.channels
        maxlen = max([len(x) for x in event["data"]])
        xax = np.tile(np.arange(0, maxlen), channels).reshape(channels, maxlen)

        # Fill in data with np.nan if the window labels are not in order.
        # This operation is channel by channel since the first window label
        # is not necessarily the same for all channels.

        return xax

    def parse(self, raw_data) -> dict:
        """Parses raw_data into a dict.

        Parses the data from the raw event and strips the timestamp/id.
        An dict is created from the parsed data with the id preserved.

        Args:
            raw_data (bytes): Raw data packaged with a header and a stopword.
        Returns:
            dict.
        """
        event = {}
        try:
            event = self.parse_digital_data(raw_data)
        except (TypeError, Exception) as e_msg:
            LOGGER.exception("parse_digital_data failed: %s", e_msg)
            event = raw_data
        else:
            # Add the X-Axis.
            # event = self.datafiller(event)
            x, y = self._fix_missing_data(event)
            lbl = self._fix_missing_windows(event)
            event["time"] = x
            event["data"] = y
            event["window_labels"] = lbl
            event["created_at"] = raw_data.get("created_at", 0)
            event["pkg_num"] = raw_data.get("pkg_num", 0)
            event["event_num"] = raw_data.get("pkg_num", 0)

        event["name"] = None

        return event
