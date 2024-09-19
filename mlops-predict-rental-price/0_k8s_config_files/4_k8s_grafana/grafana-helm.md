# Install using Helm

## Add helm repo
helm repo add grafana https://grafana.github.io/helm-charts

## Update helm repo
helm repo update

## Install helm 
helm install my-release grafana/grafana

## Expose Grafana Service
export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=my-release" -o jsonpath="{.items[0].metadata.name}")
kubectl --namespace default port-forward $POD_NAME 3000

Note:
kubectl get pods
kubectl exec -it <<grafana-pod>> -- sh
grafana-cli admin reset-admin-password NEWPASSWORD


1. Get your 'admin' user password by running:

   kubectl get secret --namespace default my-release-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo


2. The Grafana server can be accessed via port 80 on the following DNS name from within your cluster:

   my-release-grafana.default.svc.cluster.local

   Get the Grafana URL to visit by running these commands in the same shell:
     export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=my-release" -o jsonpath="{.items[0].metadata.name}")
     kubectl --namespace default port-forward $POD_NAME 3000

3. Login with the password from step 1 and the username: admin