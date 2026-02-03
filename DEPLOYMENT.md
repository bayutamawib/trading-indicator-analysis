# Deployment Guide

This guide covers deploying the Trading Indicator Analysis system using Docker and Kubernetes.

## Docker Deployment

### Build Docker Image

```bash
# Build the image
docker build -t trading-indicator-analysis:latest -f docker/Dockerfile .

# Tag for registry (optional)
docker tag trading-indicator-analysis:latest yourusername/trading-indicator-analysis:latest
```

### Run with Docker Compose

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

### Access Services

- **Streamlit UI**: http://localhost:8501
- **MLflow UI**: http://localhost:5000

### Run Single Container

```bash
# Run Streamlit only
docker run -p 8501:8501 -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/mlruns:/app/mlruns \
  -v $(pwd)/reports:/app/reports \
  trading-indicator-analysis:latest
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.20+)
- kubectl configured
- Docker image pushed to registry (optional for local testing)

### Deploy with kubectl

```bash
# Create namespace (optional)
kubectl create namespace trading-indicator

# Apply manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/trading-indicator-streamlit
kubectl logs -f deployment/mlflow-server
```

### Port Forwarding

```bash
# Forward Streamlit
kubectl port-forward svc/streamlit-service 8501:8501

# Forward MLflow (in another terminal)
kubectl port-forward svc/mlflow-service 5000:5000
```

### Access Services

- **Streamlit UI**: http://localhost:8501
- **MLflow UI**: http://localhost:5000

### Deploy with Helm

```bash
# Install Helm chart
helm install trading-indicator k8s/helm/

# Upgrade release
helm upgrade trading-indicator k8s/helm/

# Uninstall release
helm uninstall trading-indicator

# Check release status
helm status trading-indicator
helm get values trading-indicator
```

### Helm with Custom Values

```bash
# Deploy with custom values
helm install trading-indicator k8s/helm/ \
  --set replicaCount=3 \
  --set autoscaling.enabled=true \
  --set autoscaling.maxReplicas=10
```

## Scaling

### Horizontal Pod Autoscaling

```bash
# Apply HPA
kubectl autoscale deployment trading-indicator-streamlit \
  --min=2 --max=5 --cpu-percent=80

# Check HPA status
kubectl get hpa
```

### Manual Scaling

```bash
# Scale deployment
kubectl scale deployment trading-indicator-streamlit --replicas=3

# Check replicas
kubectl get deployment trading-indicator-streamlit
```

## Monitoring

### Check Pod Status

```bash
# Get pod details
kubectl describe pod <pod-name>

# Get pod logs
kubectl logs <pod-name>

# Stream logs
kubectl logs -f <pod-name>
```

### Check Service Status

```bash
# Get service details
kubectl describe service streamlit-service

# Get endpoints
kubectl get endpoints
```

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name>

# Check events
kubectl get events

# Check logs
kubectl logs <pod-name>
```

### Service Not Accessible

```bash
# Check service
kubectl describe service streamlit-service

# Check endpoints
kubectl get endpoints streamlit-service

# Test connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -- sh
# Inside pod: wget -O- http://streamlit-service:8501
```

### Resource Issues

```bash
# Check resource usage
kubectl top nodes
kubectl top pods

# Check resource requests/limits
kubectl describe pod <pod-name> | grep -A 5 "Limits\|Requests"
```

## Production Considerations

### 1. Persistent Storage

```yaml
# Add PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: trading-indicator-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

### 2. Ingress Configuration

```yaml
# Add Ingress for external access
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: trading-indicator-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: trading-indicator.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: streamlit-service
            port:
              number: 8501
```

### 3. Resource Limits

```yaml
# Set resource limits in deployment
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"
```

### 4. Health Checks

```yaml
# Configure liveness and readiness probes
livenessProbe:
  httpGet:
    path: /_stcore/health
    port: 8501
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /_stcore/health
    port: 8501
  initialDelaySeconds: 10
  periodSeconds: 5
```

## Environment Variables

### Docker

```bash
PYTHONUNBUFFERED=1
MLFLOW_TRACKING_URI=file:///app/mlruns
```

### Kubernetes

```yaml
env:
- name: PYTHONUNBUFFERED
  value: "1"
- name: MLFLOW_TRACKING_URI
  value: "http://mlflow-service:5000"
```

## Cleanup

### Docker

```bash
# Stop and remove containers
docker-compose -f docker/docker-compose.yml down

# Remove image
docker rmi trading-indicator-analysis:latest
```

### Kubernetes

```bash
# Delete deployments
kubectl delete deployment trading-indicator-streamlit mlflow-server

# Delete services
kubectl delete service streamlit-service mlflow-service

# Delete namespace
kubectl delete namespace trading-indicator
```

## Performance Tuning

### Streamlit Configuration

```bash
# Streamlit config file (~/.streamlit/config.toml)
[client]
maxMessageSize = 200

[server]
maxUploadSize = 200
enableXsrfProtection = true
```

### MLflow Configuration

```bash
# MLflow backend store
mlflow server --backend-store-uri postgresql://user:password@localhost/mlflow
```

## Security

### 1. Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: trading-indicator-netpol
spec:
  podSelector:
    matchLabels:
      app: trading-indicator
  policyTypes:
  - Ingress
  - Egress
```

### 2. RBAC

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: trading-indicator-role
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

### 3. Secrets Management

```bash
# Create secret for credentials
kubectl create secret generic trading-indicator-secrets \
  --from-literal=api-key=your-api-key
```

## Backup and Recovery

### Backup MLflow Data

```bash
# Backup mlruns directory
tar -czf mlruns-backup.tar.gz mlruns/

# Backup to cloud storage
aws s3 cp mlruns-backup.tar.gz s3://your-bucket/backups/
```

### Restore MLflow Data

```bash
# Restore from backup
tar -xzf mlruns-backup.tar.gz

# Restore from cloud storage
aws s3 cp s3://your-bucket/backups/mlruns-backup.tar.gz .
tar -xzf mlruns-backup.tar.gz
```

## Monitoring and Logging

### Prometheus Metrics

```yaml
# Add Prometheus scrape config
- job_name: 'trading-indicator'
  static_configs:
  - targets: ['localhost:8501']
```

### ELK Stack Integration

```bash
# Send logs to Elasticsearch
kubectl apply -f k8s/logging/filebeat-config.yaml
```

---

For more information, see the main README.md and SETUP.md files.
