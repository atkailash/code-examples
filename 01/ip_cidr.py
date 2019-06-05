class Ip(object):
    def __init__(self, ip_addr):
        if not isinstance(ip_addr, str):
            raise TypeError("IP must be string")
        if len(ip_addr.split('.')) == 4:
            self.ip_addr = ip_addr
            self.binip = self._ip_to_bin(self.ip_addr)
        elif len(ip_addr) == 32:
            self.ip_addr = self._bin_to_ip(ip_addr)
            self.binip = ip_addr
        else:
            self.ip_addr = self._bin_to_ip(ip_addr)
            self.binip = ip_addr.join('0' * (32 - len(self.binip)))

    def __str__(self):
        return self.ip_addr

    def __repr__(self):
        return f"Ip({self.ip_addr})"

    def __eq__(self, other):
        if isinstance(other, Ip):
            return self.ip_addr == other.ip_addr
        else:
            return self.ip_addr == other

    def __hash__(self):
        return hash((self.ip_addr, self.binip))

    def _ip_to_bin(self, an_ip):
        """
        Takes IP address and converts it to binary
        Internal method.

        Parameter:
        an_ip (str): IP Address to convert

        Returns:
        bin_ip (str): IP Address in binary
        """
        octets = an_ip.split(".")
        bin_octet_list = []
        try:
            for octet in octets:
                if len(octet) <= 3 and int(octet) <= 255:
                    bin_octet_list.append(format(int(octet), '08b'))
                else:
                    raise ValueError(f"Octet {octet} in {an_ip} invalid.")
            bin_ip = "".join(bin_octet_list)
            return bin_ip
        except ValueError as ve:
            print(ve)
            print("Quitting: please fix the error")
            quit(2)
        except Exception as e:
            print(e)
            print("Quitting: please resolve the error")
            quit(3)

    def _bin_to_ip(selfself, an_ip):
        """
        Takes a binary IP and converts it to dot notation
        Internal Method.

        Parameter:
        an_ip (str): Binary string, no dots

        Returns:
        dot_ip (str): String of dot notation IP
        """
        dot_ip = ''
        if len(an_ip) < 32:
            an_ip.join("0" * (32 - len(an_ip)))
        elif len(an_ip) == 32:
            for x in range(0, len(an_ip), 8):
                if x < 24:
                    dot_ip += str(int(an_ip[0 + x:8 + x], 2)) + "."
                else:
                    dot_ip += str(int(an_ip[0 + x:8 + x], 2))
        elif "." in an_ip:
            raise ValueError("Can only convert binary IP without dots")
        return dot_ip


class Cidr(object):
    def __init__(self, network: str, prefix: int):
        self.network = Ip(network)
        self.prefix = prefix
        self.ip_start = Ip(self._pad(self.network.binip[0:self.prefix], '0'))
        self.ip_stop = Ip(self._pad(self.network.binip[0:self.prefix], '1'))


    def __repr__(self):
        return f"Cidr(network={self.network}, prefix={self.prefix})"

    def __str__(self):
        return f"{self.network}/{self.prefix}"

    def _pad(self, bin_ip, padding):
        """
        Pads a binary string IP to make it 32

        Parameters:
        bin_ip (str): binary string
        padding (str): Character to use for padding

        Returns:
        string: padded binary IP string
        """
        return bin_ip + (padding * (32 - len(bin_ip)))

    def __contains__(self, an_ip):
        try:
            if not isinstance(an_ip, Ip):
                new_ip = Ip(an_ip)
                return self.ip_start.binip < new_ip.binip < self.ip_stop.binip
            elif isinstance(an_ip, Ip):
                return self.ip_start.binip < an_ip.binip < self.ip_stop.binip
            else:
                raise TypeError("Can only check string or Ip")
        except TypeError as te:
            print(te)
