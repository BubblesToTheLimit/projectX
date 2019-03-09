import json

class TagConfig:
    tags = []
    f_loc = ""
    def __init__(self, config_fname):
        with open(config_fname, 'r') as f:
            d = json.load(f)
            print(d)
        self.tags = d['tags']
        self.tags = list(map(lambda x: CategoryConfig.from_dict(x), self.tags))
        self.f_loc = config_fname
        
    def save(self, loc=None):
        l = ""
        if loc == None:
            l = self.f_loc
        else:
            l = loc
        l = l+'.out_test'

        with open(l, 'w') as f:
            s = json.dumps({'tags': self.tags}, cls=TagEncoder)
            print('save')
            print(s)

class CategoryConfig:
    c_id = ""
    color = ""
    b_configs = []

    def __init__(self, c_id, color, b_configs):
        self.c_id = c_id
        self.color = color
        self.b_configs = b_configs
        self.b_configs = list(map(lambda x: BookingConfig.from_dict(x), self.b_configs))

    @classmethod
    def from_dict(cls, d):
        c_id = d['id']
        color = d['color']
        b_configs = d['abbuchungen']
        return cls(c_id, color, b_configs)

    def reprJSON(self):
        return dict(id=self.c_id, color=self.color, abbuchungen=self.b_configs)

class BookingConfig:
    b_id = ""
    identifier = []

    def __init__(self, b_id, identifier):
        self.b_id = b_id
        self.identifier = identifier
        self.identifier = list(map(lambda x: RegexIdentifier.from_dict(x), self.identifier))

    @classmethod
    def from_dict(cls, d):
        b_id = d['id']
        identifier = d['identifier']
        return cls(b_id, identifier)

    def reprJSON(self):
        return dict(id=self.b_id, identifier=self.identifier)

class RegexIdentifier:
    t = ""
    v = ""

    def __init__(self, t, v):
        self.t = t
        self.v = v

    @classmethod
    def from_dict(cls, d):
        t = d['type']
        v = d['value']
        return cls(t, v)

    def reprJSON(self):
        return dict(type=self.t, value=self.v)

class TagEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
