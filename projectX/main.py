import sys
import os
import argparse

import Sparkassenparser
from TagConfig import TagConfig, Identifier
from Tagger import Tagger

from test import tag_config_test

parser = argparse.ArgumentParser("main script")
parser.add_argument('-c', '--csv')
parser.add_argument('-tc', '--tagconfig')

args = parser.parse_args()

def main(csv_p, tc_p):
    tag_config_test(csv_p, tc_p)

if __name__=='__main__':
    main(args.csv, args.tagconfig)
