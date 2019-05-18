import csv
from datetime import datetime
from Booking import Booking

def parse_from_filename(fn, delimiter=';'):
    try:
        with open(fn, 'r') as f:
            r = csv.reader(f, delimiter=delimiter)
            first_line = True
            result = []
            for line in r:
                if first_line:
                    first_line = False
                    continue
                o = parse_line(line)
                result.append(o)
            return result
    except FileNotFoundError as e:
        print(f"Couldn't find file {fn}")
        return

def parse_line(line):
    date=datetime.strptime(line[1], "%d.%m.%y")
    booking_type = line[3]
    comment = line[4]
    from_to = line[11]
    iban = line[12]
    value = float(line[14].replace(",",".")) #BUG may fail

    return Booking(date, comment, from_to, iban, value, booking_type)
