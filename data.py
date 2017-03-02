
# coding: utf-8

# In[1]:

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

OSMFILE = "kolkata.osm"  #Downloaded osm file
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Lane", "Road","Sarani", "Park", "Bagan", "Place"] 
            
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
# Creating regular expression objects
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
double_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

# Cleaning the names using the mapping dictioanry listed above
def update_name(name, mapping):
    if '(' in name:
        name = name.split('(')[0]
    name = name.strip()
    
    m = street_type_re.search(name)
    if m:
        if m.group() in mapping.keys():
            name = re.sub(m.group(), mapping[m.group()], name)
            

    return name

def clean_postal_code(postcode):
    return postcode.replace(" ","")

# Giving elements a dictionary shape with organised key:value pair
def shape_element(element):
    POS = ['lat','lon']
    node = {}
    create={}
    node_refs=[]
    pos = [None,None]
    
    if element.tag == "node" or element.tag == "way" :
        node['type']=element.tag
        for key, value in element.attrib.iteritems():
            if key in CREATED:
                create[key] = value
            elif key == 'lat':
                pos[0] = float(value)
            elif key == 'lon':
                pos[1] = float(value)
            else:
                node[key] = value
        
        node['create'] = create  #Adding the 'create' dictionary into node
        if pos:
            node['pos'] = pos
        
        for child in element:
            #Checking if children are of type nd
            if child.tag == 'nd':
                node.setdefault('node_refs',[]).append(child.attrib['ref'])
                
            #Checking if children are of type tag                
            elif child.tag == 'tag':
                k = child.attrib['k']
                v = child.attrib['v']
                  
                
                if problemchars.search(k) or double_colon.search(k):
                    pass   #ignoring unusual types
                elif k.startswith('addr:'):
                    v = update_name(v, mapping)
                elif k == "addr:postcode":
                    v = clean_postal_code(v) # cleaning extra spaced postal codes
                    #Creating a dictionary with cleaned key:value pairs
                    node.setdefault('address',{})[ k.split(":")[1] ] = v
                else:
                    node[k] = v
               
            
    if node:
        return node
    else:
        pass

# Processing all the nodes into dictionary so as to store in json file
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

    
       

if __name__ == "__main__":
    data = process_map(OSMFILE, True)
    pprint.pprint(data[0])
    


# In[ ]:



