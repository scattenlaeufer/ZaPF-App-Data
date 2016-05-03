#!/usr/bin/python

import mwclient
import re
import yaml
import random
import argparse
from pprint import pprint

#parser = argparse.ArgumentParser('Get AK data from ZaPF wiki')
#parser.add_argument('ak_section',type=int,default=1,help='AK section')
#parser.add_argument('ws_section',type=int,default=2,help='WS section')
#args = parser.parse_args()

#print(args)

site = mwclient.Site('zapf.wiki','/')
page = site.pages['SoSe16_Arbeitskreise']

def parse_tables(section,regex):
	page_source = page.text(section)
	tables = re.findall(regex,page_source)

	wiki_link = re.compile('\[\[(.*?)\|(.*?)\]\]')
	ak_list = []

	for line in tables:
		ak = {}
		if line[0].strip() == '':
			ak['slotid'] = random.choice(['AK1','AK2','AK3','AK4','AK5','AK6','AK7','BAK1','BAK2'])
		else:
			ak['slotid'] = line[0]
		ak['room'] = line[1]
		names = wiki_link.findall(line[2])
		if len(names) == 1:
			ak['name'] = names[0][1]
			ak['url'] = 'https://zapf.wiki/'+names[0][0]
		elif len(names) == 2:
			ak['name'] = names[1][1]
			ak['url'] = 'https://zapf.wiki/'+names[1][0]
		responsible_raw_list = line[3].split(',')
		responsible_list = []
		for responsible in responsible_raw_list:
			responsible_split = wiki_link.findall(responsible)
			if len(responsible_split) > 0:
				responsible_list.append(responsible_split[0][1])
			else:
				responsible_list.append(responsible.strip())
		ak['responsible'] = ', '.join(responsible_list)
		ak_list.append(ak)

	return ak_list

ak_list = parse_tables(2,'\|(.*?)\|\|(.*?)\|\|(.*?)\|\|(.*?)\|\|.*?')
ak_list += parse_tables(4,'\|(.*?)\|\|(.*?)\|\|(.*?)\|\|(.*)')

ak_yaml = yaml.dump(ak_list,default_flow_style=False)
with open('ak_sose16.yml','w') as yaml_file:
	yaml_file.write(ak_yaml)
