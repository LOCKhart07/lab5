## **Setup Instructions**

### Docker Desktop

* Download and install Docker Desktop from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

### Minikube

* Download Minikube from [https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download)
* Install Minikube

### Kubectl

* Download Kubectl from [https://dl.k8s.io/release/v1.32.0/bin/windows/amd64/kubectl.exe](https://dl.k8s.io/release/v1.32.0/bin/windows/amd64/kubectl.exe)
* Install Kubectl

### Kafka (Strimzi)

* Documentation: [https://strimzi.io/quickstarts/](https://strimzi.io/quickstarts/)
* Create a namespace for Kafka: `kubectl create namespace kafka`
* Install Strimzi: `kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka`
* Verify Strimzi installation: `kubectl get pod -n kafka --watch`
* Create a Kafka cluster: `kubectl apply -f https://strimzi.io/examples/latest/kafka/kraft/kafka-single-node.yaml -n kafka`
* Run a Kafka producer: `kubectl -n kafka run kafka-producer -ti --image=quay.io/strimzi/kafka:0.44.0-kafka-3.8.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic wine`
* Run a Kafka consumer: `kubectl -n kafka run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.44.0-kafka-3.8.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic wine --from-beginning`

### Postgres

* Apply the Postgres deployment: `kubectl apply -f postgres-deployment.yaml`
* Apply the Postgres service: `kubectl apply -f postgres-service.yaml`
* Run a Postgres shell: `kubectl exec -it deployment/postgres -- psql -d mydatabase`
* Create required table `CREATE TABLE wine_quality ( wine_name VARCHAR(255) NOT NULL, quality INTEGER NOT NULL );`

### Spark RBAC

* Documentation: [https://spark.apache.org/docs/3.5.3/running-on-kubernetes.html](https://spark.apache.org/docs/3.5.3/running-on-kubernetes.html)
* Create a Spark service account: `kubectl create serviceaccount spark`
* Create a Spark cluster role binding: `kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default`


### Docker image
* Build image: `docker build -t <dockerhub_account>/<image_name>:<version>`
* Push image to repo: `docker push <dockerhub_account>/<image_name>:<version>`

### Kubernetes deployment
* Run our streaming pipeline: `kubectl apply -f deployment.yaml`