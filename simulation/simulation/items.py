from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Compose

from w3lib.html import remove_tags

from .helpers.common import parse_date, strip_value_str


class TakeIdentityOrNone(object):
    def __call__(self, values):
        """Override default Identity class."""
        if not values:
            return [None]
        return values


class ActiveForeignPrincipalItem(Item):
    country = Field()
    url = Field()
    foreign_principal = Field()
    address = Field()
    state = Field()
    registrant = Field()
    reg_num = Field()
    date = Field()
    exhibit_url = Field()


class ActiveForeignPrincipalLoader(ItemLoader):
    # Override to get None values
    default_input_processor = TakeIdentityOrNone()
    default_output_processor = Compose(TakeFirst(), strip_value_str)

    address_in = MapCompose(remove_tags)
    date_in = MapCompose(parse_date)

    def load_item(self):
        """Override to avoid ignoring None values. See
        https://github.com/scrapy/scrapy/commit/0632546"""
        item = self.item
        for field_name in self._values:
            item[field_name] = self.get_output_value(field_name)
        return item
