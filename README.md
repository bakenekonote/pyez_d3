# pyez_d3

Juniper Router Visualization Tools using PYEZ and D3

isis/ospf visualization
_____
1. enable netconf over ssh on JUNOS device
2. install pyez python library and its prereqs.
3. apt-get install python-django
4. modify pyez_d3/isis_d3/views.py and update the junos_host, junos_user and junos_passwd
5. update pyez_d3/settings ALLOW_HOSTS with your server ip addresses. e.g. 
'''
ALLOWED_HOSTS = [ '172.27.171.81' ]
'''
6. 	python manage.py runserver 0.0.0.0:8080

on your web browser visit 
http://ip:8080/isis_d3/
http://ip:8080/ospf_d3/
