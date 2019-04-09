import Sparkassenparser
from Tagger import Tagger
import Plotter
import sys
import os

dirname = os.path.dirname(__file__)
csv_path = os.path.join(dirname, '../data/example.csv')
tagconfig_path = os.path.join(dirname, '../data/tagconfig.json')

if len(sys.argv) > 1:
    print('Using csv location', sys.argv[1])
    csv_path = sys.argv[1]

def main():
    bookings = Sparkassenparser.parse_from_filename(csv_path)
    
    tagger = Tagger(tagconfig_path)
    tagger.tag_bookings(bookings)

    for booking in bookings:
        print(booking)

    Plotter.plot_timeframe(bookings, "20.02.19", "31.03.19")

if __name__=='__main__':
    main()