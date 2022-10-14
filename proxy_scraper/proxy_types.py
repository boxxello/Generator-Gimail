from enum import Enum



class ProxyType(str, Enum):
    HTTP = "http"
    HTTPS= "https"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"
    ALL = "all"

    def __str__(self):
        return self.value
    def __add__(self, other):
        return ProxyType(self.value + other.value)
    @staticmethod
    def from_str(s):
        try:
            return ProxyType(s.lower())
        except ValueError:
            raise ValueError("Not a valid proxy type")
