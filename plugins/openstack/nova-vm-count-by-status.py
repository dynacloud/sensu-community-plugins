#!/usr/bin/env python
import re
import os
import time
import optparse
import sys
import socket
import novaclient.v1_1

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

def now():
    return int(time.time())

def total_time(timings):
    total = 0
    for url, start, end in timings:
        total += round(end - start,2)
    return total


#main
nova = novaConnect()
status_count = {}

# servers timings/counts
try:
    servers = nova.servers.list(True, {'all_tenants': '1'})
    for server in servers:
        status = server.status
        if status not in status_count:
            status_count[status] = 1
        else:
            status_count[status] += 1

except Exception as e:
    print "servers.list failed %s" % e

for status in status_count:
    print "%s %s %d" % (STATS_PREFIX + "counts.servers.stats." + status, status_count[status], now())



# exit cleanly
sys.stdout.flush()
sys.stderr.flush()
sys.exit(0)
