#!/usr/bin/python
 # -*- coding: utf-8 -*-

import re
import sys
import string

import json
import codecs

from unidecode import unidecode

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


# el "?n=3.html" hace que el menú de navegación esté expandido.
vademecum_home = "http://www.dit.upm.es/~pepe/libros/vademecum/index.html?n=3.html"
vademecum_topics = "http://www.dit.upm.es/~pepe/libros/vademecum/topics/"


# Regex patterns for the data
# title, topic
pattern_head = re.compile('>(\w+)\s[?[\w\s]*\]?\s?\(([\w\s]*)\)<\/span>', re.UNICODE)

#links_to
pattern_links = re.compile("<a\shref=.(\d+.html)#mywiki", re.UNICODE)

# JSON template
json_template = 'vademecum_template.json'

# Unitext dictionary
template = 'dictionary_template'
concepts = []

def get_topics(driver):
    
    
    #navigation iframe
    driver.switch_to.frame("content")
    
    
    enlaces = driver.find_elements_by_tag_name("a")
    
    validos = [e.get_attribute("href") for e in enlaces if e.get_attribute("href")]
    
    return validos
  
def get_data_from_link(driver, resource):
    """
    Do some dirty magic to parse the vademecum
    and get the data in a semi-definitve format.
    """
    info = {}
    try:
        driver.get(resource)
        driver.switch_to.frame("content")
    
        text = driver.page_source
        
        # The header
        cabecera = pattern_head.search(text)
        result = cabecera.groups()
        info['label'] = result[0]
        info['topic'] = result[1]
        
        # Append the concepts for the unitext dict
        if info['label'] not in concepts:
            concepts.append(info['label'])
        
        # The actual explanation
        content = ""

        textos = driver.find_elements_by_xpath("//div[@class='WordSection1']/p[@class='MsoNormal']")
        for contenido in textos:
            content = content+contenido.text
        
        # Get examples
        examples = driver.find_elements_by_xpath("//td/p[@class='PreformattedTextCxSpMiddle']")
        example = ""
        for line in examples:
            example = example+line.text
        
        # This is cheating, but, If I don't have examples, I add a fake one
        # saying I don't have an example
        if example == "":
            example = "Lo siento, no tengo ningún ejemplo sobre eso"
        
        info['example'] = example
        
        # Replace some weird syntax    
        if u"\xb7" in content:
            content = string.replace(content, u"\xb7         ", " ")
        
        # Search for inverted commas, and remove them
        if u"\u201c" in content:
            content = string.replace(content, u"\u201c", "")
        if u"\u201d" in content:
            content = string.replace(content, u"\u201d", "")
        
        # Remove line jumps
        if u"\n" in content:
            content = string.replace(content, u"\n", "")
        
        info['content'] = content
        
        # The related info
        related = pattern_links.findall(text)
        if related:
            info['links_to'] = []
            for link in related:
                info['links_to'].append(vademecum_topics+link)
            
            
        # Add the resource
        info['resource'] = resource
        
        print "Valido: " + resource
    except Exception as e:
        print e.message
        print "No valido: "+resource
        
    return info
    
def replace_links_with_labels(data):
    """
    Replaces the links in the scrapped data with the actual labels
    Returns a list with all the data, no a dictionary!
    """
    result = []
    for resource, values in data.iteritems():
        
        if 'links_to' in values:
            # Get the labels
            newlinks = []
            for link in values['links_to']:
                if link in data:
                    newlinks.append({'label': data[link]['label']})
            values['links_to'] = newlinks
        else:
            # If there is no "links to", since its a mandatory field (curses!), generic filler
            values['links_to'] = {'label': 'otros conceptos'}
        
        result.append(values)
    
    return result
    
def write_to_json(data, filename):
    """
    Copys the template, and replaces the data with the new scrapped one.
    """
    
    template = json.load(open(json_template))
    template['items'] = data
    
    # Write the data
    with open(filename, 'w') as outfile:
        json.dump(template, outfile, encoding="utf-8", indent=2)

def write_unitex_dict():
    """
    Writes the unitext dict.
    """
    
    # Generate the string
    dictionary = u""
    for concept in concepts:
        dictionary += concept.lower() + ',' + concept.lower() + '.JAVACONCEPT\n'
    
    dict_file = codecs.open('dictionary.txt', 'w', 'utf-8')
    dict_file.write(unidecode(dictionary))
    dict_file.close()
def main():
    # Get the main page
    driver = webdriver.Firefox()
    driver.get(vademecum_home)
    
    enlaces = get_topics(driver)
    
    #Debug
    #print get_data_from_link(driver, "http://www.dit.upm.es/~pepe/libros/vademecum/topics/95.html")
    #print concepts
    #return 
    
    vademecum_data = {}
    for enlace in enlaces:    
        data = get_data_from_link(driver, enlace)
        if data:
            vademecum_data[enlace] = data        
                
    driver.close()
    
    # Replace the "links to" sections with labels instead of uris
    data = replace_links_with_labels(vademecum_data)
    
    # Save all the data!
    write_to_json(data, 'vademecum.json')
    write_unitex_dict()
    print "done!"
if __name__ == "__main__":
    main()

