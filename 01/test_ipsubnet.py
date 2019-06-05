import ipsubnet
from ip_cidr import Ip, Cidr
import pytest
import ipaddress

class TestClass(object):
    def test_ipcidr(self):
        assert Ip("1.1.1.1").binip == "00000001000000010000000100000001"
        assert Ip("1.0.0.1").binip != "00000001000000010000000100000001"
        assert Ip("208.67.222.222").binip == "11010000010000111101111011011110"
        assert Ip("00000001000000010000000100000001").ip_addr == "1.1.1.1"
        ip = Ip("103.237.104.0")
        assert ip.ip_addr == "103.237.104.0"
        assert ip.binip == "01100111111011010110100000000000"
        cidr = Cidr("103.237.104.0", 22)
        assert cidr.network == "103.237.104.0"
        assert cidr.prefix == 22
        assert cidr.ip_start == "103.237.104.0"
        assert cidr.ip_stop == "103.237.107.255"
        assert type(ip.ip_addr) == str
        with pytest.raises(SystemExit, match="2"):
            Ip("256.1.1.1")
        with pytest.raises(SystemExit, match="2"):
            Ip("a.1.1.1")

    def test_check_cidr(self):
        ip = Ip("103.237.105.3")
        cidr = Cidr("103.237.104.0", 22)
        assert ip in cidr
        ip2 = Ip("103.237.108.0")
        assert ip2 not in cidr
        assert (ip in cidr) == (ipaddress.ip_address("103.237.105.3") in ipaddress.ip_network("103.237.104.0/22"))
