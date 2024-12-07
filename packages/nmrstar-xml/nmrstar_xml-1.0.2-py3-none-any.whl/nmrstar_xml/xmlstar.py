#!/usr/bin/env python3
import argparse

from nmrstar_xml import Translator


def main( ):
    parser = argparse.ArgumentParser(description="Translate XML file to NMR-STAR" )
    parser.add_argument('-i','--input',help="XML input file (default stdin)")
    parser.add_argument('-o','--output',help="NMR-STAR output file (default stdout)")
    parser.add_argument('--xmlstar',action='store_true',help=argparse.SUPPRESS) #only used for test call
    args = parser.parse_args()
    with Translator(args.input,args.output) as tr:
        tr.xml_translate()


if __name__ == "__main__":
    main()
