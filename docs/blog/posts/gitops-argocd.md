---
date: 2024-07-01
categories:
  - DevOps
  - GitOps
  - CI/CD
tags:
  - gitops
  - argocd
  - kubernetes
  - ci/cd
  - deployment
authors:
  - alan
readtime: 8
comments: true
image: assets/images/blog/gitops-argocd.svg
description: Implementing GitOps workflows that scale across multiple environments and teams
---

# GitOps with ArgoCD: Best Practices

GitOps has transformed how we manage deployments at scale. Here's what we've learned implementing GitOps with ArgoCD across multiple environments and teams.

<!-- more -->

## Why GitOps?

Traditional deployment methods often suffer from:
- **Configuration drift** between environments
- **Lack of audit trails** for changes
- **Manual deployment processes** that don't scale
- **Inconsistent rollback procedures**

GitOps solves these problems by making Git the single source of truth for your infrastructure and applications.

## Our GitOps Architecture

### Repository Structure

We use a **multi-repo approach** with clear separation of concerns:

```
├── application-repos/
│   ├── service-a/
│   ├── service-b/
│   └── service-c/
└── gitops-repos/
    ├── dev/
    ├── staging/
    └── production/
```

### ArgoCD Application Structure

Each application follows a consistent pattern:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: service-a
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-repo.git
    targetRevision: HEAD
    path: production/service-a
  destination:
    server: https://kubernetes.default.svc
    namespace: service-a
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

## Key Best Practices

### 1. Environment Promotion Strategy

We use **branch-based promotion**:

- `main` branch → Production
- `staging` branch → Staging  
- `develop` branch → Development

### 2. Secret Management

Never store secrets in Git. We use **External Secrets Operator**:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager
    kind: ClusterSecretStore
  target:
    name: database-credentials
  data:
  - secretKey: username
    remoteRef:
      key: prod/db/credentials
      property: username
  - secretKey: password
    remoteRef:
      key: prod/db/credentials
      property: password
```

### 3. Application of Applications Pattern

We use ArgoCD's **App of Apps** pattern for managing multiple applications:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: all-apps
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-repo.git
    targetRevision: HEAD
    path: apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Results and Benefits

After 12 months of GitOps with ArgoCD:

- **99.5%** deployment success rate
- **75%** reduction in deployment time
- **Zero** configuration drift incidents
- **100%** audit trail coverage
- **50%** reduction in rollback time

## Challenges and Solutions

### Challenge: Managing Secrets

**Solution**: External Secrets Operator + AWS Secrets Manager

### Challenge: Scaling to Multiple Teams

**Solution**: ArgoCD Projects with RBAC

### Challenge: Progressive Delivery

**Solution**: Argo Rollouts for canary deployments

## Conclusion

GitOps with ArgoCD has transformed our deployment process, making it more reliable, auditable, and scalable. The key is to start with a solid foundation of best practices and continuously refine your approach as you scale.