==============================================
List of Tools to be Installed
==============================================
1. For Editor - Visual Studio Code 
   https://code.visualstudio.com/

2. Get a GitHub 
   https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F&source=header-home

3. Get a Docker Hub Account 
   https://hub.docker.com/

4. For Java JDK
   https://www.oracle.com/java/technologies/downloads/#jdk17-windows

5. For Python
   https://www.python.org/

6. Jupyter Lab
   $ pip install jupyterlab
   $ pip install notebook

7. Docker Desktop for Windows
   https://www.docker.com/

8. Install Pandas
   $ pip install pandas

9. Install Sckit Learn
   $ pip install scikit-learn

10. Install Joblib
   $ pip install joblib

11. AWS CLI
    https://awscli.amazonaws.com/AWSCLIV2.msi

   Note: 
   - Using IAM , create 'mlapp' user and associate AWS S3FullAccess Policy to user(mlapp)
   - Create IAM credentials for same mlapp user (AccessKeyID,SecretAccessKeyID)
   - Permissions/Policy: AmazonEC2ContainerRegistryFullAccess,AmazonS3FullAccess

    $ aws --version   # Verify AWS CLI Installation
    $ aws configure   # Configure AWS CLI to Allow programatic access to AWS account
       - AccessKeyID
       - SecretAccessKeyID
       - region: us-east-2
       - output: json

13. Install Kubernetes 
    https://kind.sigs.k8s.io/
    https://kind.sigs.k8s.io/docs/user/quick-start#installation

    $ curl.exe -Lo kind-windows-amd64.exe https://kind.sigs.k8s.io/dl/v0.24.0/kind-windows-amd64
    $ Move-Item .\kind-windows-amd64.exe c:\some-dir-in-your-PATH\kind.exe

    Note: SET PATH =$PATH: C:\kind\kind.exe

    To Create Kubernetes Cluster 
    $ kind create cluster --name main-k8s-kind-cluster


14. Install Kubectl (CLI method and Clinet to connect with Kubernetes)
    URL: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
     $ curl.exe -LO "https://dl.k8s.io/release/v1.31.0/bin/windows/amd64/kubectl.exe"

    - Note: SET PATH =$PATH: C:\kubectl\kubectl.exe

   
###################################
List of Docker Commands
###################################

$ docker images
$ docker ps -a
$ docker build -t <name-of-the-docker-image>
$ docker images
$ docker login
$ docker rmi <<image-id>>
$ docker rm $(docker ps -a)
$ docker rmi $(docker images -a -q)
$ docker push <<image-id>>
$ docker push ssadcloud/mlapp:latest

###################################
Using Jenkins
###################################
Name of the S3 Bucket: mlapp-models-storage-artifacts
URI of the S3 Bucket:  s3://mlapp-models-storage-artifacts
AWS S3 CLI Command for File Upload:
      $ aws s3 cp <<artifact-object-name>> <<Name of the S3 Bucket/Name of the object>>

Job1: 01_mlapp_build_docker_image
      This Jenkins job is designated to pull the ML mode from GitHub , and build Source Code and generate (.joblib) and upload to AWS S3 buckets, and build Docker Images for MLApp
         $ cd mlops-predict-rental-price\
         $ aws s3 cp rental_price_model.joblib s3://mlapp-models-storage-artifacts/mlapp.joblib
         $ docker build . -t ssadcloud/mlapp
         $ docker push ssadcloud/mlapp

Job2: 02_mlapp_push_docker_image_registry
      This job to push image built from 01_mlapp_build_docker_image into Container Registry

        $ aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 932589472370.dkr.ecr.us-east-2.amazonaws.com
        $ docker build -t mlapp-ecr .
        $ docker tag mlapp-ecr:latest 932589472370.dkr.ecr.us-east-2.amazonaws.com/mlapp-ecr:latest
        $ docker push 932589472370.dkr.ecr.us-east-2.amazonaws.com/mlapp-ecr:latest


Job3: 03_mlapp_deploy_to_k8s
         #Task1
         $ cd mlops-predict-rental-price/k8s-config-files
         $ kubectl delete -f mlapp-service.yaml
         $ kubectl delete -f mlapp-deployment.yaml

         # Task2
         $ cd mlops-predict-rental-price/k8s-config-files
         $ kubectl apply -f mlapp-deployment.yaml
         $ kubectl apply -f mlapp-service.yaml

###################################
# Kuberenetes Commands
###################################
 - kubectl get nodes
 - kubectl get pods
 - kubectl apply -f mlapp-deployment.yaml
 - kubectl apply -f mlapp-service.yaml
 - kubectl delete -f mlapp-deployment
 - kubectl port-forward svc/rental-price-predictor-service 5000:5000
 - kubectl exec --stdin -tty podname --bin/bash