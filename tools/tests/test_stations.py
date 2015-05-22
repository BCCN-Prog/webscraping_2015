import os
from ..stations import *
import pprint

d = station_file2dict(os.path.join('tools',
                                   'TU_Stundenwerte_Beschreibung_Stationen.txt'))
#json = stations.get_pretty_json(d)
#stations.dump_dict2json(d, 'webscraping/stations.json')
d2 = load_int_key_json2dict(os.path.join('tools', 'stations.json'))

pprint.pprint(d2[4377])

# Has any of the entries changed?
print(set(o for o in set(d2).intersection(set(d)) if d[o] !=
          d2[o]))
