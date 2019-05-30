#!/usr/bin/env python3
import argparse
import warning

argparser = argparse.ArgumentParser(prog="ipsubnet", description="IP CIDT Subnet calculator/checker"))
argparser.add_argument("-f", "--file", nargs=1, type=str, help="Filename to parse. Contents in <ip> <cidr> format per line.")
argparser.add_argument("-c", "--cidr", nargs=1, type=str, help="CIDR to check")
argparser.add_argument("-i", "--ip", nargs=1, type=str, help="IP Address to check")
argparser.parse()

def readFile(inputfile):
    """
    Parameters:
    filename (str): Name of the file to read

    Returns:
    ipcidr (dict): List of lists which are a pair of ip and cidr
    """

    try:
        theFile = open(inputfile, "r")
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
        print("Quitting due to error.")
        quit(-1)

    ipcidr = []        
    currentLine = 1
    for line in theFile:
        splitLine = line.rstrip("\n").split()
        try:
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
            return ipcidr
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(e)

            return ipcidr
