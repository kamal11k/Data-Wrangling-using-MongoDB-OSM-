
# coding: utf-8

# In[1]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "kolkata.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) #regular expression


expected = ["Street", "Avenue", "Lane", "Road", 
            "Sarani", "Park", "Bagan", "Place"]


mapping = { "St": "Street",
            "St.": "Street",
            "Ave" : "Avenue",
            "Ave." : "Avenue",
            "Rd" : "Road",
            "Rd." : "Road",
            "Raod" : "Road",
            "road" : "Road",
            "raod" : "Road",
            "ROAD" : "Road",
            "Ln" : "Lane",
            "Ln." : "Lane"
            }


def audit_street_type(street_types, street_name):
    
    street_type = street_name.split(" ")[-1]
    street_types[street_type].add(street_name)
        

        # Updating names using mapping dictionary listed above
def update_name(name, mapping):
    if '(' in name:
        name = name.split('(')[0]
    name = name.strip()
    
    m = street_type_re.search(name)
    if m:
        if m.group() in mapping.keys():
            name = re.sub(m.group(), mapping[m.group()], name)
            

    return name


# Checking if its a street name
def is_street_name(child):
    return (child.attrib['k'] == "addr:street")


# Auditing the nodes to create a dictioanry having street type key:value pairs
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # Checking only node and way tags.
        if elem.tag == "node" or elem.tag == "way":
            for child in elem.iter("tag"): # Iterating through 'tag' types
                if is_street_name(child):
                    # updating street names during auditing
                    street_name = update_name(child.attrib['v'], mapping)
                    audit_street_type(street_types, street_name)
    osm_file.close()
    return street_types






    
if __name__ == '__main__':
    
    st_types = audit(OSMFILE)
    
    pprint.pprint(dict(st_types))
    


# In[ ]:



