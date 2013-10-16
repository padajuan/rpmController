#!/usr/bin/python

import platform
import datetime
import time
import os
from pymongo import Connection
import datetime
import time
import hashlib
import codecs
import ConfigParser


# Para leer donde esta instalado el mongodb
config = ConfigParser.RawConfigParser()
config.read('/opt/pdi/rpmControler/rpmControler.ini')

ip_mongo = config.get('mongo', 'ip')
port_mongo = config.getint('mongo','port')

#Para sacar la hora de cada ejecucion
horaRaw = time.time()
hora = time.ctime(horaRaw)


#trato de sacar un codigo unico md5 que me identifique la maquina
#strip_digits(name) + strip_digits(ips) + strip_digits(system) + strip_digits(release) + strip_digits(version) + strip_digits(distribution)
def codigo(cadena):  
  return hashlib.md5(cadena).hexdigest()

def nombre_maquina():
   nombre=os.popen('uname -n')
   respuesta= ""
   for i in nombre.readlines():
            respuesta = respuesta + i
   return respuesta.splitlines()

def Ip_Maquina():
    ips=os.popen('/sbin/ifconfig  | grep "inet addr" | grep -v "127.0.0.1"| cut -d":" -f2 | cut -d" " -f1')
    respuesta= ""
    for i in ips.readlines():
            respuesta = respuesta + i
    return respuesta.splitlines()

#devuelve un diccionario con todos los rpms de la maquina
def info_paquetes():

    paquetes=os.popen('rpm -qa | sort -n')
    respuesta= ""
    for i in paquetes.readlines():
            respuesta = respuesta + i
    return respuesta.splitlines()
#para pasar de cadane a lista
def strip_digits(string):
    result = ''
    for c in string:
        result = result + c
    return result
#saca la fecha en la que se instalo el rpm. cuidado puede haber problemas con el idioma.
def install_date(string):
    #print 'rpm -qi '+string+' | grep -i "Install date"'
    result = os.popen('rpm -qi '+string+' | grep -i "Install date"| cut -d" " -f4,5,6,7,8')
    respuesta= ""
    for i in result.readlines():
            respuesta = respuesta + i
    return respuesta
  
def run():
  name = nombre_maquina()
  ips = Ip_Maquina()
  paquetes = info_paquetes()
  date = datetime.datetime.utcnow()
  system = platform.system()
  release = platform.release()
  version = platform.version()
  distribution = platform.dist()
  aux2 = strip_digits(name) + strip_digits(ips) + strip_digits(system) + strip_digits(release) + strip_digits(version) + strip_digits(distribution)
  id_= codigo(cadena = aux2)

  #connect to mongodb

  connection = Connection(ip_mongo, port_mongo)

  # get database

  db = connection.rpms_database

  #get one collection

  collection = db.rpms_collection


  info_host = {}
  info_host ["id_"] = id_
  info_host ["name"] = name
  info_host ["ips"] = ips
  info_host ["date"] = date
  info_host ["system"] = system
  info_host ["release"] = release
  info_host ["version"] = version
  info_host ["distribution"] = distribution



  info_pcs = db.info_hosts

  if (info_pcs.find({"id_": id_}).count() == 0):
    info_pcs.insert(info_host)
  #else:
  #  print "Ya existia el host..."

  dict_rpms= {}

  rpms = db.rpms

  for record in rpms.find({"id_": id_}):
    if (record["rpm"].find(" (deleted)") == -1):
      dict_rpms[record["rpm"]] = False
    #else:
      #print "excluyo:"
      #print record["rpm"]

  
  for i in paquetes:
    date_installed = install_date(i)
    info_rpms = {}
    info_rpms ["id_"] = id_
    info_rpms ["rpm"] = i
    info_rpms ["date_process"] = date
    info_rpms ["date_installed"] = date_installed
    if (rpms.find({"id_": id_, "rpm": i, "date_installed": date_installed}).count() == 0):
      #print "print inserto:" + i
      rpms.insert(info_rpms)
    #else:
      #print "find del find"

    dict_rpms[i] = True

  for item in dict_rpms:
    #print item
    #print dict_rpms[item]
    if (dict_rpms[item] == False):
      if (rpms.find({"id_": id_, "rpm": item + " (deleted)"}).count() == 0):
        date_installed = install_date(i)
        info_rpms = {}
        info_rpms ["id_"] = id_
        info_rpms ["rpm"] = item + " (deleted)"
        info_rpms ["date_process"] = date
        info_rpms ["date_installed"] = ""
        rpms.insert(info_rpms)



def main():
  run()

main()