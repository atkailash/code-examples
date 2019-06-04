import ipsubnet
import pytest


class TestClass(object):
    def test_convert_to_binary(self):
        assert ipsubnet.convert_to_binary("1.1.1.1") == "00000001000000010000000100000001"
        assert ipsubnet.convert_to_binary("1.0.0.1") != "00000001000000010000000100000001"
        assert ipsubnet.convert_to_binary("208.67.222.222") == "11010000010000111101111011011110"
        assert type(ipsubnet.convert_to_binary("1.1.1.1")) == str
        with pytest.raises(SystemExit, match="2"):
            ipsubnet.convert_to_binary("256.1.1.1")
        with pytest.raises(SystemExit, match="2"):
            ipsubnet.convert_to_binary("a.1.1.1")

    def test_check_cidr(self):
        assert ipsubnet.check_cidr(["1.1.1.1", "1.0.0.0/15"]) == True
        assert ipsubnet.check_cidr(["1.0.0.1", "1.0.0.0/15"]) == True
        assert ipsubnet.check_cidr(["10.1.0.16", "10.1.0.0/28"]) == False
