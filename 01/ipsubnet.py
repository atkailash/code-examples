#!/usr/bin/env python3
import argparse

argparser = argparse.ArgumentParser(prog="ipsubnet", description="IP CIDT Subnet calculator/checker")
argparser.add_argument("-f", "--file", nargs=1, type=str, help="Filename to parse. Contents in <ip> <cidr> format per line.")
argparser.add_argument("-c", "--cidr", nargs=1, type=str, help="CIDR to check")
argparser.add_argument("-i", "--ip", nargs=1, type=str, help="IP Address to check")


def read_file(input_file):
    """
    Parameters:
    filename (str): Name of the file to read

    Returns:
    list_of_ip_cidr (dict): List of lists which are a pair of ip and cidr
    """

    list_of_ip_cidr = []
    had_error = False
    try:
        a_file = open(input_file, "r")
        for line in a_file:
            split_line = line.rstrip("\n").split("#") # Remove comment first
            if len(split_line) <= 2: # IP/CDR is [0] and comment is [1], will also work if it's just IP/CDR
                split_line = split_line[0].split() # Remove the comment
                list_of_ip_cidr.append(split_line)
            else:
                raise ValueError("Less than two columns found. Cannot compare to nothing.")
    except ValueError as ve:
        print(ve)
        had_error = True
    except FileNotFoundError as fnf:
        print(fnf)
        had_error = True
    except PermissionError as perr:
        print(perr)
        had_error = True
    except Exception as e:
        print(e)
        had_error = True
    finally:
        a_file.close()
        if had_error:
            print("Quitting due to error.")
            quit(4)
        else:
            return list_of_ip_cidr


def convert_to_binary(an_ip):
    """
    Takes IP address and converts it to binary

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

def check_cidr(ip_cidr_list):
    """
    Calculate the cidr of given list that contains IP in 0 and
    the CIDR in 1. This is being done manually instead of using the
    ipaddress module.

    Parameters:
    ip_cidr_list (list): [ip, cidr]

    Returns:
    ip_in_cidr (bool): True if it is, False if not.
    """

    ip_address = ip_cidr_list[0]
    [cidr_address, cidr_size] = ip_cidr_list[1].split("/")
    cidr_size = int(cidr_size)  # Make it an int

    bin_cidr_address = convert_to_binary(cidr_address)
    bin_ip_address = convert_to_binary(ip_address)

    bin_ip_network = bin_ip_address[0:cidr_size]
    bin_cidr_network = bin_cidr_address[0:cidr_size]

    return bin_ip_network == bin_cidr_network


if __name__ == "__main__":
    args = argparser.parse_args()
    the_file = args.file
    the_cidr = args.cidr
    the_ip = args.ip
    try:
        if the_file is not None: # -f is used
            if the_cidr is not None or the_ip is not None:  # -c or -i is used
                raise argparse.ArgumentError(the_file, "Cannot have CIDR/IP and File")
            elif the_cidr is None or the_ip is None:        # no -c or -i
                list_ip_cidr_list = read_file(the_file[0])
                for ip_and_cidr in list_ip_cidr_list:
                    result = check_cidr(ip_and_cidr)
                    print(f"IP: {ip_and_cidr[0]} in {ip_and_cidr[1]} = {result}")
            else:
                raise argparse.ArgumentError()
        elif the_ip is not None and the_cidr is None:       # -i not -c
            raise argparse.ArgumentError(the_cidr, "Must have both CIDR and IP")
        elif the_cidr is not None and the_ip is None:       # -c not -i
            raise argparse.ArgumentError(the_ip, "Must have both CIDR and IP")
        elif the_cidr is not None and the_ip is not None:                                               # -c -i not -f
            the_ip = the_ip[0]
            the_cidr = the_cidr[0]
            result = check_cidr([the_ip, the_cidr])
            print(f"IP: {the_ip} in {the_cidr} = {result}")
        else:
            argparser.print_help()
            raise argparse.ArgumentError(the_file, "No valid arguments provided")
    except argparse.ArgumentError as ae:
        print(f"ArgumentError: {ae}")
        print("Args" + str(vars(args)))
        quit(1)
    except Exception as e:
        print(f"Unknown exception: {e}")
        quit(-1)
