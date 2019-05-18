import sys
import os
import argparse

import Sparkassenparser
from TagConfig import *

parser = argparse.ArgumentParser("main script")
parser.add_argument('-c', '--csv')
parser.add_argument('-tc', '--tagconfig')

args = parser.parse_args()

def main(args):
    tagconfig = TagConfig(args.tagconfig)

    bookings = Sparkassenparser.parse_from_filename(args.csv)

    findings = 0
    for booking in bookings:
        category = tagconfig.infer_category(booking)
        if category != "":
            findings += 1
        booking.category = category
    print(f"Found {findings} categories!")

if __name__=='__main__':
    main(args)
