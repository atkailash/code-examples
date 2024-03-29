#!/usr/bin/env python3
import argparse
from ip_cidr import Ip, Cidr
import csv

argparser = argparse.ArgumentParser(prog="ipsubnet", description="IP CIDT Subnet calculator/checker")
argparser.add_argument("-f", "--file", nargs=1, type=str,
                       help="Filename to parse. Contents in <ip> <cidr> format per line.")
argparser.add_argument("-c", "--cidr", nargs=1, type=str, help="CIDR to check")
argparser.add_argument("-i", "--ip", nargs=1, type=str, help="IP Address to check")
argparser.add_argument("-o", "--out", nargs=1, type=str, help="Output file (CSV)")


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
            split_line = line.rstrip("\n").split("#")  # Remove comment first
            if len(split_line) <= 2:  # IP/CDR is [0] and comment is [1], will also work if it's just IP/CDR
                split_line = split_line[0].split()  # Remove the comment
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
            quit(4)  # 4 to differentiate from other quits
        else:
            return list_of_ip_cidr


def write_csv(out_file, result_dict):
    with open(out_file, 'w') as csv_out:
        writer = csv.writer(csv_out, delimiter=",")
        writer.writerow(["IP", "IS IN", "NETWORK", "PREFIX"])
        for ip in result_dict:
            cidr_net = result_dict[ip]['cidr'].network.ip_addr
            cidr_prefix = result_dict[ip]['cidr'].prefix
            isin = result_dict[ip]['isin']
            writer.writerow([ip.ip_addr, isin, cidr_net, cidr_prefix])


def process_ipcidr(ip, cidr):
    ip = Ip(ip)
    cidr_net, prefix = cidr.split("/")
    return_cidr = Cidr(cidr_net, int(prefix))
    return (ip, {"cidr": return_cidr, "isin": ip in return_cidr})


if __name__ == "__main__":
    args = argparser.parse_args()
    the_file = args.file
    the_cidr = args.cidr
    the_ip = args.ip
    out_file = args.out
    result = {}
    try:
        if the_file is not None:  # -f is used
            the_file = the_file[0]
            if the_cidr is not None or the_ip is not None:  # -c or -i is used
                raise argparse.ArgumentError(the_file, "Cannot have CIDR/IP and File")
            elif the_cidr is None or the_ip is None:  # no -c or -i
                list_ip_cidr_list = read_file(the_file)
                for ip_and_cidr in list_ip_cidr_list:
                    an_ip, processed_dict = process_ipcidr(ip_and_cidr[0], ip_and_cidr[1])
                    result[an_ip] = processed_dict
                    print(f"IP: {an_ip} in {processed_dict['cidr']} = {processed_dict['isin']}")
            else:
                raise argparse.ArgumentError()
        elif the_ip is not None and the_cidr is None:  # -i not -c
            raise argparse.ArgumentError(the_cidr, "Must have both CIDR and IP (IP Provided)")
        elif the_cidr is not None and the_ip is None:  # -c not -i
            raise argparse.ArgumentError(the_ip, "Must have both CIDR and IP (CIDR Provided)")
        elif the_cidr is not None and the_ip is not None:  # -c -i not -f
            the_ip = the_ip[0]
            the_cidr = the_cidr[0]
            an_ip, processed_dict = process_ipcidr(the_ip, the_cidr)
            result[an_ip] = processed_dict
            print(f"IP: {an_ip} in {processed_dict['cidr']} = {processed_dict['isin']}")
        else:
            argparser.print_help()
            raise argparse.ArgumentError(the_file, "No valid arguments provided")
        if out_file:
            write_csv(out_file[0], result)
    except argparse.ArgumentError as ae:
        print(f"ArgumentError: {ae}")
        print("Args" + str(vars(args)))
        quit(1)
    except Exception as e:
        print(f"Unknown exception: {e}")
        quit(-1)
