

def parseyaml(file):
        with open(RULES_FILE, "r") as f:
            rules = yaml.safe_load(f)
        return rules

class EventIncludeParser(EventObject):
    events = set()
    rules = parseyaml(RULES_FILE)

    def __init__(self, EventObject):
        super(EventIncludeParser, self).__init__(EventObject)
        self.event_obj_attr = EventObject.__dict__

    def match_value(v):
          if isinstance(v, str):
              if event_obj_dict[k] == v:
                  return True
    def includeHandler(self):

        for key, value in rules.items():
          if "include" not in rules.keys():
            events.add(event)
          if key == "include":
              for k, v in rules["include"].items():
                  if k in AVAILABLE_FIELDS:


                      if isinstance(v, list):
                          for i in v:
                              if event_obj_dict[k] == i:
                                  events.add(event)
