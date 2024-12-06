#!/bin/env python3

from licomp.interface import ObligationTrigger
from licomp.main_base import LicompParser

from licomp_osadl.config import cli_name
from licomp_osadl.config import description
from licomp_osadl.config import epilog
from licomp_osadl.osadl import LicompOsadl

def main():
    lo = LicompOsadl()
    o_parser = LicompParser(lo,
                            name = cli_name,
                            description = description,
                            epilog = epilog,
                            default_trigger = ObligationTrigger.SNIPPET)
    o_parser.run()

if __name__ == '__main__':
    main()
