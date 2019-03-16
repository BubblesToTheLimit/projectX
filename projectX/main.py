import sys
import os
import argparse

import Sparkassenparser
from TagConfig import TagConfig, RegexIdentifier
from Tagger import Tagger


parser = argparse.ArgumentParser("main script")
parser.add_argument('-c', '--csv')
parser.add_argument('-tc', '--tagconfig')

args = parser.parse_args()

csv_path = args.csv
tagconfig_path = args.tagconfig

def main(csv_p, tc_p):
    tc = TagConfig()
    tc.add_category('Grundausgaben')
    tc.add_booking_type('Grundausgaben', 'Miete')
    tc.add_booking_type('Grundausgaben', 'Strom')
    i0 = RegexIdentifier('comment', 'MIETE')
    i1 = RegexIdentifier('from_to', 'Vattenfall')
    tc.add_identifier('Grundausgaben', 'Miete', i0)
    tc.add_identifier('Grundausgaben', 'Strom', i1)
    tc.save(tc_p)

    if not csv_p or not tc_p:
        return
    tc = TagConfig.from_file(tc_p)
    bookings = Sparkassenparser.parse_from_filename(csv_path)
    for b in bookings:
        r = tc.infer_category(b)
        if r['success']:
            print('Found category+booking:', r['r'],'for:', b)
        else:
            print(r['m'], b)

if __name__=='__main__':
    main(csv_path, tagconfig_path)
