'''Script para monitorización de temperatura mediante el chip DS18S20 utilizando un servidor EmonCMS.

  Es necesario sustituir KEY por la APIKEY del servidor.
  
  Para más información visita la siguiente dirección:
  http://litox.entramado.net/2013/12/26/monitorizar-la-temperatura-desde-raspberry-pi/
  
  Autor: Carlos Sanmartín Bustos
  
'''

import os
import glob
import time
import urllib2, httplib

os.system('sudo modprobe wire')
os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

APIKEY="KEY"
period=10

base_dir = '/sys/bus/w1/devices'
f = open(base_dir + '/w1_bus_master1/w1_master_slave_count', 'r');
sensorCount = f.readlines()
sensorCount = [int(l[0]) for l in sensorCount]
f.close()
f = open(base_dir + '/w1_bus_master1/w1_master_slaves', 'r');
devices = f.readlines()
f.close()
def read_temp_raw(sensor):
  device_file = base_dir + '/' + devices[sensor][:-1] + '/w1_slave'
  f = open(device_file, 'r')
  lines = f.readlines()
  f.close()
  return lines
  
def read_temp(sensor):
  lines = read_temp_raw(sensor)
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw(sensor)
  
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    return temp_string[0:4]
    
while True:
  url = "http://localhost/emoncms/input/post?json={"
  for x in range(0, sensorCount[0]):
    url = url + devices[x][:-1] + ":" + read_temp(x) + ","
  url = url[:-1]+"}&apikey="+ APIKEY
  print(url)
  urllib2.urlopen(url)
  time.sleep(period)