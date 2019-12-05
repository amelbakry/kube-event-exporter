# Kubernetes Event Exporter:

Kubernetes events are stored in the apiserver on master. To avoid filling up master’s disk, a retention policy is enforced: events are removed one hour after the last occurrence.
This Application will listen to live events from the api server and publish them to standard output, with logging agent installed, these events can be exported to central logging system like Scalyr in this case.

## How to use it:

 - In Scalyr select the cluster and then  $application == "event-exporter"
 - event-exporter parser is installed, so you can filter by the below attributes
   - Namespace
   - Level
   - Component
   - Object
   - Resource name
   - Reason
   - Message

## Applying Filters:
 - You can filter (include/exclude) the events to be shipped to the Central Logging System (Scalyr in this case)
 - To apply filter create a yaml file with the name "eventRules.yaml" and apply your rules
   In the value field, you can use string or a list
  - Examples:
    - Include means include only
```
      include:
             level: "Warning"
             namespace: ["kube-system"]
             component: "kube-schedule-scaler"
             reason: "Unhealthy"
```

    - Exclude
      ```
         exclude:
             namespace: ["acquire", "bhennessy"]
             reason: ["Started", "Created", "Scheduled", "Pulling", "BackOff", "Pulled"]
             component: ["kube-dns", "kubelet"]
```
