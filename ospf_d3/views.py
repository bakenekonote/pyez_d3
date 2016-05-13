from jnpr.junos import Device
from lxml import etree
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
import os

junos_host = '172.27.170.60'
junos_user = 'lab'
junos_passwd = 'lab123'

def data(request):
        dev = Device(host=junos_host, user=junos_user, passwd=junos_passwd)
        dev.open()

	root = dev.rpc.get_ospf_database_information(extensive=True)
	
	linkset = set()
	nodeset = set()
	area = root.find('./ospf-area-header/ospf-area').text
	
	for r in root.findall("./ospf-database[lsa-type='Router']"):
	        adv_router_id = r.find('advertising-router').text
	        nodeset.add(adv_router_id)
	        for n in r.findall("./ospf-router-lsa/ospf-lsa-topology/ospf-lsa-topology-link"):
	                link_type = n.find("link-type-name").text
	                neighbor_id = n.find("ospf-lsa-topology-link-node-id").text
	                metric =  n.find("ospf-lsa-topology-link-metric").text
	                state =  n.find("ospf-lsa-topology-link-state").text
	                nodeset.add(neighbor_id)
	                if link_type == "Bidirectional":        
	                        if adv_router_id > neighbor_id:
	                                linkset.add((adv_router_id,neighbor_id,link_type, metric, state))
	                        else:
	                                linkset.add((neighbor_id,adv_router_id,link_type, metric, state))
	                else:
	                                linkset.add((adv_router_id,neighbor_id,link_type, metric, state))
	        
	
	#we need to transform set into link to fix the index for each node
	nodelist = list(nodeset)
	nodejson = []
	for n in nodelist:
	        nodejson.append(dict(name=n, group=1))
	linkjson = []
	for l in linkset:
	        linkjson.append(dict(source=nodelist.index(l[0]), target=nodelist.index(l[1]), value=1, linktype=l[2], status='up'))
	
	js = dict(area=area, nodes=nodejson, links=linkjson)
        return JsonResponse(js)

def index(request):
        resp = loader.get_template('ospf_d3/index.html').render()
        return HttpResponse(resp)
