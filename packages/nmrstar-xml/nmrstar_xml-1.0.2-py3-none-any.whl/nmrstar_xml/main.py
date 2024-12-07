#!/usr/bin/env python3
import argparse
import logging
from nmrstar_xml import nmrstar_xml_logger


def main():
    logging.basicConfig()
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--loglevel', default='WARN', help="Python logging level")

    args = parser.parse_args()
    nmrstar_xml_logger.setLevel(getattr(logging,args.loglevel))


if __name__ == "__main__":
    main()

