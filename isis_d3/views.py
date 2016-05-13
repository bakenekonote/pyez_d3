from jnpr.junos import Device
from lxml import etree
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
import os

junos_host = 'kdc-dc-mx480-2.kdc.jnpr.net'
junos_user = 'coeadmin'
junos_passwd = 'coeadmin'

def data(request):
        dev = Device(host=junos_host, user=junos_user, passwd=junos_passwd)
        dev.open()

        root = dev.rpc.get_isis_database_information(extensive=True)

	dev.close()

        linkset = set()
        nodeset = set()

        for a in root.findall('./isis-database/isis-database-entry/isis-neighbor/is-neighbor-id'):
                b = a.find('../../lsp-id')
		
                if 'extensive' in request.GET:
                    s1 = a.text
                    s2 = b.text[:-3]
                else:
                    s1 = a.text[:-3]
                    s2 = b.text[:-6]
                if s1 > s2:
                        linkset.add((s1,s2))
                else:
                        linkset.add((s2,s1))
                nodeset.add(s1)
                nodeset.add(s2)

        #we need to transform set into link to fix the index for each node
        nodelist = list(nodeset)
        nodejson = []
        for n in nodelist:
                nodejson.append(dict(name=n, group=1))
        linkjson = []
        for l in linkset:
                linkjson.append(dict(source=nodelist.index(l[0]), target=nodelist.index(l[1]), value=1, status='up'))

        js = dict(nodes=nodejson, links=linkjson)
        return JsonResponse(js)

def index(request):
        resp = loader.get_template('isis_d3/index.html').render()
        return HttpResponse(resp)
