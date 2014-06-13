#!/usr/bin/env python
import re
import os
import time
import sys
import socket
import novaclient.v1_1
import optparse

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

STATS_PREFIX = "openstack.nova"

if not re.match(".$", STATS_PREFIX):
    STATS_PREFIX += "."

p = optparse.OptionParser(conflict_handler="resolve", description= "This Nagios plugin checks the health of mongodb.")

p.add_option('-a', '--auth-url', action='store', type='string', dest='auth_url', default='http://127.0.0.1:5000/v2.0', help='Auht Url you want to connect to')
p.add_option('-t', '--tenant', action='store', type='string', dest='tenant', default=27017, help='The port mongodb is runnung on')
p.add_option('-u', '--user', action='store', type='string', dest='user', default=None, help='The username you want to login as')
p.add_option('-p', '--pass', action='store', type='string', dest='passwd', default=None, help='The password you want to use for that user')

options, arguments = p.parse_args()

USER = options.user
PASS = options.passwd
TENANT_NAME = options.tenant
OS_AUTH_URL = options.auth_url

def novaConnect():
    return novaclient.v1_1.Client(USER, PASS, TENANT_NAME, OS_AUTH_URL, timeout="600", service_type="compute", no_cache=True)

def collect_metric(name, value, timestamp):
#     sock = socket.socket()
#     sock.settimeout(5)
#     sock.connect( (GRAPHITE_HOST, 2003) )
    print "%s %s %d" % (STATS_PREFIX + name, value, timestamp)
#     sock.send("%s %s %d\n" % (STATS_PREFIX + name, value, timestamp))
#     sock.close()

def now():
    return int(time.time())

def total_time(timings):
    total = 0
    for url, start, end in timings:
        total += round(end - start,2)
    return total


#main
nova = novaConnect()

# flavor timings/counts
try:

    flavors = nova.flavors.list()
    if flavors:
        flavortime = total_time(nova.get_timings())
        nova.reset_timings()
        collect_metric("timings.flavors.list", flavortime, now())
        collect_metric("counts.flavors.list", len(flavors), now())
except:
    print "flavors.list failed"

# net timings/counts
try:
    networks = nova.networks.list()
    if networks:
        networkstime = total_time(nova.get_timings())
        nova.reset_timings()
        collect_metric("timings.networks.list", networkstime, now())
        collect_metric("counts.networks.list", len(networks), now())
except:
    print "networks.list failed"

# servers timings/counts
try:
    servers = nova.servers.list(True, {'all_tenants': '1', 'status': "ACTIVE"})

except:
    print "servers.list failed"

serverstime = total_time(nova.get_timings())
collect_metric("counts.servers.list", len(servers), now())
collect_metric("timings.servers.list", serverstime, now())
nova.reset_timings()


# exit cleanly
sys.stdout.flush()
sys.stderr.flush()
sys.exit(0)