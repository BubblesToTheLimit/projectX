import json
from Booking import Booking

class Tagger:
    searches = None

    def __init__(self, filename):
        try:
            with open(filename, 'r') as f:
                self.searches = {}
                
                d=json.load(f)
                for tag, search_strings in d.items():
                    if tag == "tag_colors":
                        continue
                    self.searches[tag] = search_strings

        except FileNotFoundError as e:
            print(f"Couldn't find file {filename}")
            return

    def tag_bookings(self, bookings: [Booking]):
        print(self.searches)
        for booking in bookings:
            for tag, search_strings in self.searches.items():
                for string in search_strings:
                    if string.lower() in str(booking).lower():
                        booking.tag = tag
                        print(f"Tagged booking of value {booking.value}\t with {tag}")
                    