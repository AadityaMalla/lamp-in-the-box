# LAMP in the Box — CSCI 312 Project 1

A modified LAMP stack packaged into containers and orchestrated with Kubernetes.

| Layer | Technology | Container |
|---|---|---|
| L — Linux | AlmaLinux 9 (AWS EC2) | host |
| A — Web server | NGINX | `lamp-nginx` |
| M — Data | Apache Spark SQL (PySpark) | `lamp-spark` |
| P — Back end | Rust (Rocket) | `lamp-rocket` |

## Architecture
```
Browser → NGINX Ingress Controller → lamp-service → 3 pods (Deployment, replicas: 3)
          each pod: nginx:80 → rocket:8000 → spark:9000 (shared localhost)
```

## Repository layout
- `nginx/` — NGINX image: landing page + reverse proxy to Rocket
- `rocket/` — Rust/Rocket API; `/students` queries the Spark container
- `spark/` — Spark SQL service exposing query results as JSON (Spark UI on 4040)
- `k8s/` — `deployment.yaml`, `service.yaml`, `ingress.yaml`

## Build
```bash
docker build -t lamp-spark:1.0 spark/
docker build -t lamp-rocket:1.0 rocket/
docker build -t lamp-nginx:1.0 nginx/
```

## Container networking demo (user-defined bridge)
```bash
docker network create lampnet
docker run -d --name spark  --network lampnet lamp-spark:1.0
docker run -d --name rocket --network lampnet -e SPARK_URL=http://spark:9000 lamp-rocket:1.0
docker run -d --name nginx  --network lampnet -e ROCKET_HOST=rocket -p 8080:80 lamp-nginx:1.0
docker run --rm --network lampnet busybox wget -qO- http://nginx/api/students
```

## Deploy to Kubernetes (k3s + ingress-nginx)
```bash
docker save lamp-nginx:1.0 lamp-rocket:1.0 lamp-spark:1.0 | k3s ctr images import -
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl create -f k8s/ingress.yaml
kubectl get pods
```

## Endpoints
- `/` — landing page (NGINX)
- `/api/` — Rocket hello, shows which pod served the request
- `/api/students` — NGINX → Rocket → Spark SQL query result

## Team
Malla, Aaditya  ·  Mayu, Natoli   · Osman, Khadija    

```
