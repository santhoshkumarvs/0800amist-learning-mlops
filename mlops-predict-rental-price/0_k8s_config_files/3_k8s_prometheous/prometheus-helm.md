
Key Page: 
https://artifacthub.io/packages/helm/prometheus-community/prometheus


# Install using Helm:

## Add helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

## Update helm repo
helm repo update

## Install helm 
helm install my-prometheus prometheus-community/prometheus

## Expose Prometheus Service

# The Prometheus server can be accessed via port 80 on the following DNS name from within your cluster:
my-prometheus-server.default.svc.cluster.local

Get the Prometheus server URL by running these commands in the same shell:

$ export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=my-prometheus" -o jsonpath="{.items[0].metadata.name}")
$ kubectl --namespace default port-forward $POD_NAME 9090


# The Prometheus alertmanager can be accessed via port 9093 on the following DNS name from within your cluster:
my-prometheus-alertmanager.default.svc.cluster.local


Get the Alertmanager URL by running these commands in the same shell:
$ export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=alertmanager,app.kubernetes.io/instance=my-prometheus" -o jsonpath="{.items[0].metadata.name}")
$ kubectl --namespace default port-forward $POD_NAME 9093


# The Prometheus PushGateway can be accessed via port 9091 on the following DNS name from within your cluster:
my-prometheus-prometheus-pushgateway.default.svc.cluster.local

Get the PushGateway URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/instance=my-prometheus,app.kubernetes.io/name=prometheus-pushgateway" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace default port-forward $POD_NAME 9091

 