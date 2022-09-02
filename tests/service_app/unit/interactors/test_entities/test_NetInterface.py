from ipaddress import IPv4Interface
from socket import AddressFamily

import pytest
from psutil._common import snicaddr

from src.service_app.interactors.net_scanner.entities import NetInterface


class TestNetInterface:
    @pytest.mark.parametrize(
        "name,snicaddrs, result",
        [
            pytest.param(
                "test",
                [
                    snicaddr(
                        family=AddressFamily.AF_INET,
                        address="127.0.0.1",
                        netmask="255.0.0.0",
                        broadcast=None,
                        ptp=None,
                    ),
                    snicaddr(
                        family=AddressFamily.AF_PACKET,
                        address="00:00:00:00:00:00",
                        netmask=None,
                        broadcast=None,
                        ptp=None,
                    ),
                ],
                NetInterface(
                    name="test",
                    ip_interfaces=[IPv4Interface("127.0.0.1/8")],
                    mac="00:00:00:00:00:00",
                ),
                id="All fields are filled",
            ),
            pytest.param(
                "test_2",
                [
                    snicaddr(
                        family=AddressFamily.AF_INET,
                        address="127.0.0.1",
                        netmask="255.255.0.0",
                        broadcast=None,
                        ptp=None,
                    ),
                ],
                NetInterface(
                    name="test_2",
                    ip_interfaces=[IPv4Interface("127.0.0.1/16")],
                    mac=None,
                ),
                id="No mac address",
            ),
            pytest.param(
                "test",
                [
                    snicaddr(
                        family=AddressFamily.AF_INET6,
                        address="::1",
                        netmask="ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
                        broadcast=None,
                        ptp=None,
                    ),
                    snicaddr(
                        family=AddressFamily.AF_PACKET,
                        address="00:00:00:00:00:00",
                        netmask=None,
                        broadcast=None,
                        ptp=None,
                    ),
                ],
                NetInterface(
                    name="test",
                    ip_interfaces=[],
                    mac="00:00:00:00:00:00",
                ),
                id="No ipv4 address, ipv6 address is skipped, mac exists",
            ),
        ],
    )
    def test_constructor(self, name, snicaddrs, result):
        assert NetInterface.from_psutil_snicaddr(name, snicaddrs) == result

    @pytest.mark.parametrize(
        "obj, is_usable",
        [
            pytest.param(
                NetInterface(name="test", ip_interfaces=[], mac=None),
                False,
                id="All requirements are violated",
            ),
            pytest.param(
                NetInterface(
                    name="test", ip_interfaces=[IPv4Interface("127.0.0.1/16")], mac=None
                ),
                False,
                id="No mac provided",
            ),
            pytest.param(
                NetInterface(
                    name="test",
                    ip_interfaces=[IPv4Interface("127.0.0.1/16")],
                    mac="00:00:00:00:00:00",
                ),
                False,
                id="Dummy mac provided",
            ),
            pytest.param(
                NetInterface(
                    name="test",
                    ip_interfaces=[IPv4Interface("127.0.0.1/16")],
                    mac="de:ad:be:ef:12:34",
                ),
                True,
                id="All requirements are satisfied",
            ),
        ],
    )
    def test_scan_usable(self, obj, is_usable):
        assert obj.scan_usable() is is_usable
