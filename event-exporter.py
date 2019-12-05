#!/usr/bin/env python3

import kubernetes
from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
import datetime
import yaml
import os

import time

AVAILABLE_FIELDS = ["level", "namespace", "component", "ob", "name", "reason", "message"]
RULES_FILE = "eventRules.yaml"

class EventObject(object):

  def __init__(self, level, namespace, component, ob, name, reason, message):
    self.level = level
    self.namespace = namespace
    self.component = component
    self.ob = ob
    self.reason = reason
    self.message = message
    self.name = name

  def return_formated_event(self):
    f_event = "[%s] [%s] [%s] [%s] [%s] [%s] [%s] %s" % (timestamp(), self.level, self.namespace, self.component, self.ob,
                                                                                             self.name, self.reason, self.message)
    return f_event

def timestamp():
  return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S UTC")


def api():
  '''
  Initialize connection to Kubernetes
  '''
  try:
    config.load_incluster_config()
  except:
    config.load_kube_config()

  v1 = client.CoreV1Api()
  return v1

def parseyaml(event, attr):

  with open("eventRules.yaml", "r") as f:
      rules = yaml.safe_load(f)
  conditions = []
  events = set()
  for key, value in rules.items():
    if "include" not in rules.keys():
      events.add(event)
    if key == "include":
        for k, v in rules["include"].items():
                if k in AVAILABLE_FIELDS:
                    if isinstance(v, str):
                        if attr[k] != v:
                          conditions.append("False")
                    if isinstance(v, list):
                        for i in v:
                            if attr[k] != i:
                              conditions.append("False")
        if "False" not in conditions:
                events.add(event)

    if key == "exclude":
        for k, v in rules["exclude"].items():
            if k in AVAILABLE_FIELDS:
                if isinstance(v, str):
                    if attr[k] == v:
                      if event in events:
                        events.remove(event)
                if isinstance(v, list):
                    for i in v:
                        if attr[k] == i:
                          if event in events:
                            events.remove(event)
  for e in events:
    print(e)



def main():

  watcher = kubernetes.watch.Watch()
  stream = watcher.stream(api().list_event_for_all_namespaces)
  for event in stream:
    try:
      namespace = event['object'].involved_object.namespace
      ob = event['object'].involved_object.name
      message = event['object'].message
      name = event['object'].metadata.name
      reason = event['object'].reason
      level = event['object'].type
      component = event['object'].source.component
      event_obj = EventObject(level, namespace, component, ob, name, reason, message)
      event_obj_dict = event_obj.__dict__
      if os.path.exists("eventRules.yaml") and os.path.getsize("eventRules.yaml") > 0:
        parseyaml(event_obj.return_formated_event(), event_obj_dict)
      else:
        print(event_obj.return_formated_event())

    except ApiException as e:
      print ("Exception when calling CoreV1Api->create_namespaced_binding: %s\n" % e)


if __name__ == '__main__':
  main()
