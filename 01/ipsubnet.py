#!/usr/bin/env python3
import argparse
import warning

argparser = argparse.ArgumentParser(prog="ipsubnet", description="IP CIDT Subnet calculator/checker")
argparser.add_argument("-f", "--file", metavar='theFile', nargs=1, type=argparse.FileType('r'), help="Filename to parse. Contents in <ip> <cidr> format per line.")
argparser.add_argument("-c", "--cidr", nargs=1, type=str, help="CIDR to check")
argparser.add_argument("-i", "--ip", nargs=1, type=str, help="IP Address to check")

def readFile(inputfile):
    """
    Parameters:
    filename (str): Name of the file to read

    Returns:
    list_of_ip_cidr (dict): List of lists which are a pair of ip and cidr
    """

    ipcidr = []        
    currentLine = 1
    try:
        theFile = open(inputfile, "r")
        for line in theFile:
            splitLine = line.rstrip("\n").split()
                if len(splitLine) > 3:
                    if splitLine[2][0] == "#":
                        line.remove(splitLine[2])
                        ipcidr.append(splitLine)
                    else:
                       warnings.warn_explicit("Ignoring 3rd column. Comments start with #",
                                           SyntaxWarning, inputfile, currentLine)
                else if len(splitLine) == 2):
                    ipcidr.append(splitLine))
                else:
                    raise ValueError("Less than two columns found. Cannot copmare to nothing.")
    except ValueError as ve:
        print(ve)
        hadError = True
    except FileNotFoundError as fnf:
        print(fnf)
        hadError = True
    except PermissionError as perr:
        print(perr)
        hadError = True
    except Exception as e:
        print(e)
        hadError = True
    finally:
        theFile.close
        if hadError:
            print("Quitting due to error.")
            quit(-1)
        else:
            return list_of_ip_cidr

def convertToBinary(an_ip):
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
        print ve
        quit(-1)
    except TypeError as te:
        print(f"{octet} is not an integer in {an_ip}")
        quit(-1)

def checkCidr(ip_cidr_list):
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
    cidr_size = int(cidr_size) # Make it an int

    bin_cidr_address = convertToBinary(cidr_address)
    bin_ip_address = convertToBinary(ip_address)

    bin_ip_network = ip_address[0:32-(32-cidr_size)]
    bin_cidr_network = cidr_address[0:32-(32-cidr_size)]

    return bin_ip_network == bin_cidr_network

if __name__ == "__main__":
    args = argparser.parse_args()
    theFile = args.file
    theCidr = args.cidr
    theIp = args.ip
    try:
        if theFile and (theCidr or theIp):
            raise argparse.ArgumentError("Cannot have CIDR/IP and File")
        else if (theCidr == None and theIp) or (theCidr and theIp == None):
            raise argparse.ArgumentError("Must have both CIDR and IP")
        else if theFile and (theCidr == None and theIp == None):
            readFile(theFile)
        else:
            checkCidr([theIp, theCidr])
    except argparse.ArgumentError as ae:
        print(ae)
        quit(-1)
    except Exception as e:
        print(e)
    finally
