import Sparkassenparser
import sys

example_path = '../data/example.csv'
if len(sys.argv) > 1:
    print('Using example location', sys.argv[1])
    example_path = sys.argv[1]

def main():
    bookings = Sparkassenparser.parse_from_filename(example_path)
    for booking in bookings:
        print(booking)

if __name__=='__main__':
    main()