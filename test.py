import yaml
import os


__available_fields = ["level", "namespace", "component", "ob", "name", "reason", "message"]

def parseyaml():
    if os.path.exists("eventRules.yaml") and os.path.getsize("eventRules.yaml") > 0:
        with open("eventRules.yaml", "r") as f:
            rules = yaml.safe_load(f)
            print(rules)
            for key, value in rules.items():
                if key == "include":
                    for k, v in rules["include"].items():
                        if k in __available_fields:
                            if isinstance(v, str):
                                if event[k] == v:
                                    print(event)
                            if isinstance(v, list):
                                for i in v:
                                    if event[k] == i:
                                        print(event)




parseyaml()
