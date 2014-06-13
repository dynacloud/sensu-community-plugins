#!/usr/bin/env python
import os
import time
import sys
import socket
from keystoneclient.v2_0 import client
import optparse

STATS_PREFIX = "openstack.keystone.timings"

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


def keystoneConnect():
    return client.Client(username=USER,
                 password=PASS,
                 tenant_name=TENANT_NAME,
                 auth_url=OS_AUTH_URL,
                 timeout=10)
def collect_metric(name, value, timestamp):
    try:
        print "%s %s %d\n" % (name, value, timestamp)
    except:
        print "Put to graphite failed"

def now():
    return int(time.time())


t0 = time.time()
try:
    keystone = keystoneConnect()
except:
    print "Keystone connection failed"
    sys.exit()

t1 = time.time()
total = round(t1-t0,2)

KMETRIC = STATS_PREFIX + ".token_get." + USER
collect_metric(KMETRIC, total, now())