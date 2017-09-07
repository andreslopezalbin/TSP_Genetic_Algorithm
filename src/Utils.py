from math import radians, cos, sin, asin, sqrt
import os
import webbrowser

import django
from django.conf import settings

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.getcwd()],
    }
]
settings.configure(TEMPLATES=TEMPLATES)
django.setup()

from django.template.loader import get_template
from django.template import Context


def haversine(gen1, gen2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1 = float(gen1.longitude)
    lat1 = float(gen1.latitude)
    lon2 = float(gen2.longitude)
    lat2 = float(gen2.latitude)
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def print_map(best_chr):
    string = ""
    for city in best_chr:
        string += '{lat: ' + city.latitude + ', lng: ' + city.longitude + '},'

    template = get_template('template.html')
    map = template.render(Context({'path': string}))

    path = os.path.abspath('map.html')
    url = 'file://' + path

    with open(path, 'w') as f:
        f.write(map)
    webbrowser.open(url)


    # {lat: 38.91200402, lng: -6.337997512},
    # {lat: 37.25037355, lng: -6.929949383},
    # {lat: 36.53499086, lng: -6.225005332},
    # {lat: 38.91200402, lng: -6.337997512}
