from __future__ import annotations
from ipaddress import IPv4Interface
from socket import AddressFamily
from typing import Optional

from psutil._common import snicaddr
from pydantic import BaseModel


class NetInterface(BaseModel):
    """Server net interface."""

    name: str
    ip_interfaces: list[IPv4Interface]  # TODO: work on IPv6
    mac: Optional[str]

    _dummy_mac = "00:00:00:00:00:00"

    @classmethod
    def from_psutil_snicaddr(cls, name: str, addr_data: list[snicaddr]) -> NetInterface:
        """Makes a NetInterface object from psutil.net_if_addrs() element."""
        if_args = {
            "name": name,
            "ip_interfaces": [
                IPv4Interface(f"{addr.address}/{addr.netmask}")
                for addr in addr_data
                if addr.family is AddressFamily.AF_INET and addr.netmask
            ],
        }
        if macs := [
            addr.address for addr in addr_data if addr.family is AddressFamily.AF_PACKET
        ]:
            if_args["mac"] = macs[0]
        return cls(**if_args)

    def scan_usable(self) -> bool:
        """Checks if interface fits for scanning."""
        return (
            bool(self.mac) and bool(self.ip_interfaces) and self.mac != self._dummy_mac
        )
