import sys
import yaml
from typing import Generic, List

class Identifier:
    """
    A helper class: Given a booking's target field and a pattern this class determines a match
    """
    pattern: str
    target: str

    def __init__(self, identifiers_config):
        try:
            self.pattern = identifiers_config["pattern"]
            self.target = identifiers_config["target"]
        except:
            print(f"Error loading identifier from identifierconfig: {identifiers_config}")
            sys.exit()

    def __str__(self):
        return ",".join([self.pattern, self.target])

    def matches(self, booking):
        try:
            value = booking.__dict__[self.target]
        except:
            print(f"Couldn't find {self.target} in booking class. Has to be one of {booking.__dict__.keys()}")
            sys.exit()

        if self.pattern in value:
            return True
        else:
            return False

class Item:
    """
    A helper class: An item groups multiple identifiers under a common name.
    """
    name: str
    identifiers: List[Identifier]

    def __init__(self, item_config):
        try:
            self.name = item_config["name"]
            self.identifiers = []
            for identifier_config in item_config["identifiers"]:
                self.identifiers.append(Identifier(identifier_config))
        except:
            print(f"Error loading item from itemconfig: {item_config}")
            sys.exit()

    def __str__(self):
        identifierstring = ""
        for identifier in self.identifiers:
            identifierstring = identifierstring + str(identifier)
        return ",".join([self.name, identifierstring])

class Category:
    """
    A helper class. A category groups multiple items under common name and a color.
    """
    name: str
    color: str
    item: List[Item]

    def __init__(self, category_config, defaultcolor=""):
        try:
            self.name = category_config["name"]

            if defaultcolor:
                self.color = category_config.get("color", defaultcolor)
            else:
                self.color = category_config["color"]

            bong = []
            for item_config in category_config.get("items"):
                bong.append(Item(item_config))
            self.item = bong
        except:
            print("Error loading category from configuration!")
            sys.exit()

    def __str__(self):
        itemstring = ""
        for item in self.item:
            itemstring = itemstring + str(item)
        return ",".join([self.name, self.color, itemstring])

class TagConfig:
    """
    The main class. Loads the configuration from a yaml file.
    Infers booking meta-information using its subclasses.
    """
    categories = List[Category]
    default_color = "#FFFFFF"

    def __init__(self, filename):
        try:
            f = open(filename)
        except FileNotFoundError:
            print(f"Couldn't open file {filename}")
            sys.exit()

        config = yaml.load(f, Loader=yaml.FullLoader)

        default_color = config.get("defaults",{}).get("color", self.default_color)
        self.default_color = default_color
        self.categories = []
        try:
            for category_config in config["categories"]:
                self.categories.append(Category(category_config, defaultcolor=default_color))
        except:
            print("Error found in configuration, check docs.")
            sys.exit()

    def __str__(self):
        output = []
        for category in self.categories:
            output.append(str(category))
        output = "|".join(output)
        return "default_color: " + self.default_color+ "\n" + \
               "categories: " + output

    def infer_category(self, booking):
        for category in self.categories:
            for item in category.item:
                for identifier in item.identifiers:
                    if identifier.matches(booking):
                        return category.name
        return ""
