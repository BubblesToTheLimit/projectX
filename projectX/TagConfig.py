import json
import re
import pprint

from Booking import Booking

class TagConfig:
    """
    Methods:
    - infer_category(Booking)
    - add_category(name)
    - add_booking(c_name, b_name, identifier)
    - add_identifier(c_name, b_name, ...)
    - remove____
    """
    categories = {}
    f_loc = ""
    def __init__(self, filename="", categories = {}):
        self.f_loc = filename
        self.categories = categories

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as f:
            d = json.load(f)
            print(d)
        if 'tags' in d:
            categories = d['tags']
            cats = {}
            for k, c in categories.items():
                cat = Category.from_dict(c)
                if cat.c_id not in cats:
                    cats[cat.c_id] = cat
                else:
                    print("Error: Duplicate category id!")
        else:
            cats = {}
        return cls(filename, cats)

    def save(self, loc=None):
        l = ""

        if loc == None and self.f_loc == None:
            return -1
        elif loc == None:
            l = self.f_loc
        else:
            l = loc

        with open(l, 'w') as f:
            s = json.dumps({'tags': self.categories}, cls=TagEncoder)
            json.dump({'tags': self.categories}, f, cls=TagEncoder)
        return 1
            


    def infer_category(self, booking):
        r = []
        for name, cat in self.categories.items():
            for b in cat.b_configs:
                if b.matches(booking):
                    r.append((cat, b))
        if len(r) > 1:
            return {
                'success': False,
                'm': 'More than one BookingType for booking',
                'r': r
            }
        elif len(r) == 0:
            return {
                'success': False,
                'm': 'No BookingType found for booking', 
                'r': r
            }
        else:
            return {
                'success': True,
                'r': r[0]
            }

    def add_category(self, name, color="000000", b_config=[]):
        if name in self.categories.keys():
            print('Error: category named:"', name, '" exists already')
            return -1
        c = Category(name, color, b_config)
        self.categories[name] = c
        return 1

    def add_booking_type(self, c_name, b_name, i=[]):
        if c_name not in self.categories.keys():
            print('Error: booking cannot be added to category because category "', c_name, '" does not exist')
            return -1
        b = BookingType(b_name, i)
        self.categories[c_name].b_configs.append(b)
        return 1


    def add_identifier(self, c_name, b_name, i):
        if c_name not in self.categories.keys():
            print('Error: itentifier cannot be added to booking type because category "', c_name, '" does not exist')
        try: 
            b_index = [b.b_id for b in self.categories[c_name].b_configs].index(b_name)
            self.categories[c_name].b_configs[b_index].identifiers.append(i)
        except ValueError as e:
            b_ids = [b.b_id for b in self.categories[c_name].b_configs]
            pprint.pprint(e)
            print('Error: identifier cannot be added to booking type because booking "', b_name, '" does not exist for category ', c_name, ' - ', b_ids)

class Category:
    c_id = ""
    color = ""
    b_configs = []

    def __init__(self, c_id, color, b_configs):
        self.c_id = c_id
        self.color = color
        self.b_configs = b_configs
        self.b_configs = list(map(lambda x: BookingType.from_dict(x), self.b_configs))

    @classmethod
    def from_dict(cls, d):
        if not 'id' in d or not 'color' in d or \
           not 'abbuchungen' in d:
            raise ValueError('Invalid json/dict: ' + str(d))
        c_id = d['id']
        color = d['color']
        b_configs = d['abbuchungen']
        return cls(c_id, color, b_configs)

    def reprJSON(self):
        return dict(id=self.c_id, color=self.color, abbuchungen=self.b_configs)

class BookingType:
    b_id = ""
    identifiers = []

    def __init__(self, b_id, identifier):
        self.b_id = b_id
        self.identifiers = identifier
        self.identifiers = list(map(lambda x: RegexIdentifier.from_dict(x), self.identifiers))

    @classmethod
    def from_dict(cls, d):
        if not 'id' in d or not 'identifier' in d:
            raise ValueError('Invalid json/dict: ' + str(d))
        b_id = d['id']
        identifiers = d['identifier']
        return cls(b_id, identifiers)

    def reprJSON(self):
        return dict(id=self.b_id, identifier=self.identifiers)

    def matches(self, booking):
        for i in self.identifiers:
            if i.matches(booking):
                return True
        return False

class RegexIdentifier:
    t = ""
    pattern = None

    def __init__(self, t, v):
        self.t = t
        self.pattern = re.compile(v)

    @classmethod
    def from_dict(cls, d):
        if not 'type' in d or not 'value' in d:
            raise ValueError('Invalid json/dict: ' + str(d))
        t = d['type']
        v = d['value']
        return cls(t, v)

    def reprJSON(self):
        return dict(type=self.t, value=self.pattern.pattern)

    def set_value(self, v):
        self.pattern = re.compile(v)

    def matches(self, booking):
        if self.t == "comment":
            return self.pattern.match(booking.comment)
        elif self.t == "from_to":
            return self.pattern.match(booking.from_to)
        elif self.t == "iban":
            return self.pattern.match(booking.iban)
        elif self.t == "value":
            return self.pattern.match(booking.value)
        elif self.t == "booking_type":
            return self.pattern.match(booking.booking_type)
        else:
            raise ValueError('Invalid RegexType')

class TagEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
