
import random
from enum import Enum

from mac_generator.Exceptions import FormatErrorUnknown
from utils.logging import get_logger

logger = get_logger()


class Format(Enum):


    HYPHEN = 1
    COLON = 2
    PERIOD = 3
    CISCO = 4
    NONE = 5
    UNKNOWN = 6


class GeneratorMac:
    """type of MAC address formats"""


    def __init__(self, mac_type=None, format_type: Format = None, generate_partial=None, lowercase=False):
        """
        Supported MAC address formats:
            MM:MM:MM:SS:SS:SS
            MM-MM-MM-SS-SS-SS
            MMMM.MMSS.SSSS
            MMMMMMSSSSSS
        :param mac_type: the type of mac address
        :param format_type: the format of the mac address
        :param generate_partial: generate a partial mac address
        :param lowercase: lowercase the mac address
        """
        if not mac_type and not format_type:
            raise ValueError("No MAC address type or format type specified")
        elif mac_type and not format_type:
            self.format_type = self.get_format(mac_type)
        elif not mac_type and format_type:
            self.format_type = self._get_mac_format(mac_type)
        else:
            raise ValueError("Format type and MAC address type specified, cannot chose both")
        if generate_partial:
            not_formatted = self._build_random_nic()
        else:
            not_formatted = self._build_random_twelve_digit()
        try:
            self.lowercase = bool(lowercase)
        except ValueError:
            logger.error("lowercase must be a boolean, defaulting to false")
            self.lowercase = False
        self.mac = self._build_mac_with_separator(
            self._set_lettercase(not_formatted), self.format_type
        )
        trimmed = self._trim_separator(self.mac)
        if len(trimmed) != 12:
            raise ValueError(f"MAC must be 12 digits but found {len(trimmed)}")
        self.HEXADECIMAL = "0123456789ABCDEF"



    @staticmethod
    def _trim_separator(mac: str) -> str:
        """removes separator from MAC address
        :param mac: the mac address
        :return: the mac address without separator
        """
        return mac.translate(str.maketrans("", "", ":-."))


    def _set_lettercase(self, string: str) -> str:
        """determines lettercase for MAC address
        :param string: the mac address
        :return: the mac address with the lettercase
        """
        return string.upper() if not self.lowercase else string.lower()


    @staticmethod
    def _ins(source: str, insert: str, position: int) -> str:
        """inserts value at a certain position in the source
        :param source: the source string
        :param insert: the value to insert
        :param position: the position to insert the value
        :return: the source string with the value inserted
        """
        return source[:position] + insert + source[position:]


    def _build_mac_with_separator(self, mac: str, _format: Format) -> str:
        """
        builds the type of separator used
        :param mac: the mac address
        :param _format: the format of the mac address
        :return: the mac address with the separator
        """
        if _format == Format.HYPHEN:
            return self._ins(
                self._ins(
                    self._ins(self._ins(self._ins(mac, "-", 2), "-", 5), "-", 8),
                    "-",
                    11,
                ),
                "-",
                14,
            )
        if _format == Format.COLON:
            return self._ins(
                self._ins(
                    self._ins(self._ins(self._ins(mac, ":", 2), ":", 5), ":", 8),
                    ":",
                    11,
                ),
                ":",
                14,
            )
        if _format == Format.PERIOD:
            return self._ins(
                self._ins(
                    self._ins(self._ins(self._ins(mac, ".", 2), ".", 5), ".", 8),
                    ".",
                    11,
                ),
                ".",
                14,
            )
        if _format == Format.CISCO:
            return self._ins(self._ins(mac, ".", 4), ".", 9)
        if _format == Format.NONE:
            return mac
        if _format == Format.UNKNOWN:
            raise FormatErrorUnknown("Unknown MAC format")


    def _get_mac_format(self, mac: str) -> Format:
        """set the mac format style
        :param mac: the mac address
        :return: the format of the mac address
        """
        if mac.count("-") == 5 and "." not in mac and ":" not in mac:
            return Format.HYPHEN
        if mac.count(":") == 5 and "." not in mac and "-" not in mac:
            return Format.COLON
        if mac.count(".") == 5 and ":" not in mac and "-" not in mac:
            return Format.PERIOD
        if mac.count(".") == 2 and ":" not in mac and "-" not in mac:
            return Format.CISCO
        if len(mac) == 12:
            return Format.NONE
        if "." not in mac and ":" not in mac and "-" not in mac:
            return Format.UNKNOWN
        else:
            return Format.NONE


    def _build_random_nic(self) -> str:
        """randomize 6-digit NIC portion of a mac addr
        :return: the mac address with the random NIC portion
        """
        random_nic = ""
        for c in range(0, 6):
            random_nic += random.choice(self.HEXADECIMAL)
        return random_nic


    def _build_random_twelve_digit(self) -> str:
        """randomize 12-digit mac
        :return: the mac address with the random 12-digit mac
        """
        mac = self._build_random_nic()
        for number in range(0, 6):
            mac += random.choice(self.HEXADECIMAL)
        return mac


    @staticmethod
    def get_format(mac_type)->Format:
        """get format of MAC address
        :param mac_type: the type of mac address
        :return: the format of the mac address
        """
        if mac_type.find(":") != -1:
            return Format.COLON
        elif mac_type.find("-") != -1:
            return Format.HYPHEN
        elif mac_type.find(".") != -1:
            return Format.PERIOD
        elif mac_type.find("") != -1:
            return Format.CISCO
        elif mac_type.find("") != -1:
            return Format.NONE
        else:
            return Format.UNKNOWN
