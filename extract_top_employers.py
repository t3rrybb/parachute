#!/usr/bin/python -tt

import urllib2, csv, codecs, json
from collections import OrderedDict
from bs4 import BeautifulSoup

def extract_attributes(name, url):
    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    company = OrderedDict()
    company['NAME'] = name
    tabletag = soup.find('table')#.find_next('tr')
    
    # get rid of all content in French
    for tag in tabletag.find_all():
        if tag.has_attr('class') and 'fr-content' in tag['class']:
            tag.decompose()

    is_header = True
    attr = None
    for tdtag in tabletag.find_all('td'):
        if is_header:
            attr = tdtag.get_text().strip().upper()
            is_header = False
            continue
        company[attr] = tdtag.get_text().strip()
        is_header = True
    return company

def get_company_list(url):
    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    companies = OrderedDict()
    for heading in soup.find_all('', {'class': 'alpha-heading rating-row'}):
        for link in heading.parent.parent.find_all('a'):
            companies[link.string] = link['href']
    return companies

def process(url):
    the_list = get_company_list(url)
    companies = list()
    for name in the_list:
        print('Processing %s (%s)' % (name, the_list[name]))
        company = extract_attributes(name, the_list[name])
        companies.append(company)
    return companies

def save2jsonfile(filepath, data):
    with open(filepath, 'w') as jsonfile:
        jsonfile.write(json.dumps(data, indent=4))

def main():
    # Top employers in Canada nation wide
    companies = process('http://www.canadastop100.com/national/')
    save2jsonfile('top-employers-canada.json', companies)

    # Top employers in GTA
    companies = process('http://www.canadastop100.com/toronto/')
    save2jsonfile('top-employers-gta.json', companies)

    # Canada's Best Diversity Employers
    companies = process('http://canadastop100.com/diversity/')
    save2jsonfile('canadas-best-diversity-employers.json', companies)

if __name__ == '__main__':
    main()