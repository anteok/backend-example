from __future__ import annotations
from ipaddress import IPv4Address, IPv4Interface
from socket import AddressFamily
from typing import Optional

from psutil._common import snicaddr
from pydantic import BaseModel


class NetInterface(BaseModel):
    """Server net interface."""

    name: str
    ip_interfaces: list[IPv4Interface]  # TODO: work on IPv6
    mac: Optional[str]

    @classmethod
    def from_psutil_snicaddr(cls, name: str, addr_data: list[snicaddr]) -> NetInterface:
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
