import sys
import os
import argparse

import Sparkassenparser
from TagConfig import TagConfig
from Tagger import Tagger


parser = argparse.ArgumentParser("main script")
parser.add_argument('-c', '--csv', required=True)
parser.add_argument('-tc', '--tagconfig', required=True)

args = parser.parse_args()

csv_path = args.csv
tagconfig_path = args.tagconfig

def main():
    bookings = Sparkassenparser.parse_from_filename(csv_path)
    tc = TagConfig(tagconfig_path)
    tc.save(tagconfig_path)

if __name__=='__main__':
    main()
