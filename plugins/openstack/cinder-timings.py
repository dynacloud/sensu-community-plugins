#!/usr/bin/env python
import re
import os
import time
import sys
import socket
from cinderclient.v1 import client
import optparse


STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

STATS_PREFIX = "openstack.cinder"

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

def cinderConnect():
  return client.Client(USER, PASS, TENANT_NAME, OS_AUTH_URL, service_type="volume")

def collect_metric(name, value, timestamp):
  print "%s %s %d" % (STATS_PREFIX + name, value, timestamp)

def now():
  return time.time()


#main
cinder = cinderConnect()

# volumes timings/counts
try:

  start = now()
  volumes = cinder.volumes.list()
  end = now()
  if volumes:
    volumestime = round(end - start, 4)
    collect_metric("timings.volumes.list", volumestime, now())
    collect_metric("counts.volumes.list", len(volumes), now())
except:
  print "volumes.list failed"

# exit cleanly
sys.stdout.flush()
sys.stderr.flush()
sys.exit(0)