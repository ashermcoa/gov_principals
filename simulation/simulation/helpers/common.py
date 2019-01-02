import datetime
import pytz
import re


def strip_value_str(value):
    result = value.replace('\xa0', ' ')\
        .replace('\\u00a0', '')\
        .strip()
    if result == '':
        return None

    # Replace 2 or more spaces that might exist
    # in the string with a single space.
    return re.sub('\s{2,}', ' ', result)


def parse_date(date_str):
    if date_str is not None:
        pst = pytz.timezone('US/Eastern')
        d = datetime.datetime.strptime(date_str, '%m/%d/%Y')
        d = pst.localize(d)
        return d.isoformat()
    return None
