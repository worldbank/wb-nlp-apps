import requests
import re


def download_with_retry(url, params=None, max_retries=10):
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = requests.get(url, params=params)
            break
        except:
            retry_count += 1

    if retry_count >= max_retries:
        return

    return response


# s = set(['Publications & Research', 'Publications'])
# s = set(["Country Focus", "Country Focus"])
# s = set("Publications,Publications & Research,Publications,Publications & Research".split(','))

def normalize_set(s):
    # s = set(['Publications & Research', 'Publications'])

    l = sorted(s)
    remove_index = set()

    for i in range(len(l) - 1):
        for j in range(1, len(l)):
            if l[i] in l[j]:
                remove_index.add(i)

    for k in sorted(remove_index, reverse=True):
        l.pop(k)

    return l


def make_unique_entry(series):
    # This will remove duplicate entries in fields: `majdocty` (`majdoctype` : normalized) and `admreg`
    series = series.fillna('')
    series = series.str.split(',').map(set).map(lambda vals: ', '.join(normalize_set(vals)))
    return series.replace('', None)


def collapse_array(data, connector=None):
    # Assume that array is of type list
    value = []

    if isinstance(data, list):
        for d in data:
            if isinstance(d, dict):
                value.append(collapse_nested_dict(d, connector=connector))
            else:
                value.extend(collapse_array(d))
    # elif isinstance(data, dict):
    #     data = collapse_nested_dict(data, connector=connector)
    #     value.append(data)
    else:
        value.append(data)

    try:
        if connector:
            # `connector` is only used in the root function call so it is safe
            # to assume that in cases where the original value is not an array or nested array,
            # we can just retrieve and return the original value
            if len(value) > 1:
                # This means that the data is an array and possibly nested
                value = connector.join(value)
            else:
                value = value[0]
    except Exception as e:
        print(data)
        print(value)
        raise(e)

    return value


# line_break_pattern = re.compile('\r?\n|\r')
whitespace_pattern = re.compile(r'\s+')
hanging_dash_pattern = re.compile(r'\S+- ')


def normalize_hanging_dash(t):
    for p in hanging_dash_pattern.findall(t):
        t = t.replace(p, p.replace('- ', ' - '))

    return t


def normalize_str_col(ser):
    return ser.map(lambda x: normalize_hanging_dash(whitespace_pattern.sub(' ', x)) if isinstance(x, str) else x)


def normalize_geo_regions(x, connector='|'):
    # geo_regions has this assumed format: {'0': {'geo_region': 'Europe'}, '1': {'geo_region': 'Europe'}}
    if isinstance(x, dict):
        x = connector.join(set(i['geo_region'] for i in x.values()))

    return x


def collapse_nested_dict(x, connector=None):
    value = []

    if isinstance(x, dict):
        for val in x.values():
            value.extend(collapse_nested_dict(val))
    elif isinstance(x, list):
        x = collapse_array(x, connector=connector)
        value.append(x)
    else:
        value.append(x)

    if connector:
        if len(value) > 1:
            value = connector.join(value)
        else:
            value = value[0]

    return value
