Things needed to be done:
- Docker desktop
    - https://www.docker.com/products/docker-desktop/
- Minikube
    - https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download
    - Kubectl
        - curl.exe -LO "https://dl.k8s.io/release/v1.32.0/bin/windows/amd64/kubectl.exe"
- Kafka(Strimzi)
    - https://strimzi.io/quickstarts/
    - kubectl create namespace kafka
    - kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
    - kubectl get pod -n kafka --watch
    = kubectl apply -f https://strimzi.io/examples/latest/kafka/kraft/kafka-single-node.yaml -n kafka 
    - kubectl -n kafka run kafka-producer -ti --image=quay.io/strimzi/kafka:0.44.0-kafka-3.8.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic
    - kubectl -n kafka run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.44.0-kafka-3.8.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-beginning
- Postgres
 - kubectl apply -f postgres-deployment.yaml
 - kubectl apply -f postgres-service.yaml
 - kubectl exec -it deployment/postgres -- bash
    - psql -d mydatabase
    - CREATE TABLE wine_quality ( wine_name VARCHAR(255) NOT NULL, quality INTEGER NOT NULL );
- Spark RBAC
    - https://spark.apache.org/docs/3.5.3/running-on-kubernetes.html
    - kubectl create serviceaccount spark
    - kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default

