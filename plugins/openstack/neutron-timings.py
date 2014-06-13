#!/usr/bin/env python
import re
import os
import time
import sys
import socket
from quantumclient.v2_0 import client as neutronclient
import optparse


STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

STATS_PREFIX = "openstack.neutron"

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

def neutronConnect():
  return neutronclient.Client(username=USER, password=PASS, tenant_name=TENANT_NAME, auth_url=OS_AUTH_URL)

def collect_metric(name, value, timestamp):
  print "%s %s %d" % (STATS_PREFIX + name, value, timestamp)


def now():
  return time.time()


#main
neutron = neutronConnect()

# network timings/counts
try:

  start = now()
  networks = neutron.list_networks()
  end = now()
  if networks:
    networkstime = round(end - start, 4)
    collect_metric("timings.networks.list", networkstime, now())
except:
  print "networks.list failed"

# exit cleanly
sys.stdout.flush()
sys.stderr.flush()
sys.exit(0)