import json  

class Author:
    def __init__(self, author):
        # input: json data
        self.name = self.process_name(author)
        self.affiliation = self.process_affiliation(author['affiliation'])
        self.email = author['email']
    
    def process_affiliation(self, affiliation):
        if len(affiliation) == 0: return {'name': None, 'location': {}}
        affi_name = ''
        if (affiliation['laboratory'] and affiliation['institution']): 
            affi_name = affiliation['laboratory'] + ' in ' + affiliation['institution']
        affi = {'name': affi_name, 'location': affiliation['location']}
        return affi

    def process_name(self, author):
        # input json author, output name string
        name = ''
        if author['first']: name += author['first']
        if len(author['middle']) != 0: name += " ".join(author['middle'])
        if author['last']: name += author['last'] 
        if author['suffix']: name += author['suffix']
        return name

def list_author(authors, num=5):
    """return author name under each paper"""
    names = []
    count = 0
    for author in authors:
        count += 1
        name = ""
        if len(author['first'])!=0: name = author['first'][0] 
        if len(author['middle']) != 0: name += author['middle'][0][0] 
        if len(author['last'])!=0: name = name + ' ' + author['last'] 
        if len(name)!= 0: names.append({'name':name, 'show':count<=num}) 
    return names
