# Kubernetes RBAC Configuration Guide

This repository contains examples and configurations for Kubernetes Role-Based Access Control (RBAC).

## Directory Structure
```
RBAC_Configuration/
├── README.md
├── roles/
│   ├── pod-reader-role.yaml
│   └── deployment-manager-role.yaml
├── cluster-roles/
│   └── cluster-admin-role.yaml
├── role-bindings/
│   └── pod-reader-binding.yaml
├── cluster-role-bindings/
│   └── cluster-admin-binding.yaml
└── service-accounts/
    └── app-service-account.yaml
```

## Components Overview

1. **Roles**: Namespace-scoped permission sets
2. **ClusterRoles**: Cluster-wide permission sets
3. **RoleBindings**: Binds roles to users/groups/service accounts within a namespace
4. **ClusterRoleBindings**: Binds cluster roles to users/groups/service accounts cluster-wide
5. **ServiceAccounts**: Identities for processes running in pods

## Usage

1. Create Service Account:
```bash
kubectl apply -f service-accounts/app-service-account.yaml
```

2. Apply Roles:
```bash
kubectl apply -f roles/
```

3. Apply ClusterRoles:
```bash
kubectl apply -f cluster-roles/
```

4. Apply RoleBindings:
```bash
kubectl apply -f role-bindings/
```

5. Apply ClusterRoleBindings:
```bash
kubectl apply -f cluster-role-bindings/
```

## Best Practices

1. Follow the principle of least privilege
2. Use namespaced roles when possible instead of cluster roles
3. Regularly audit RBAC permissions
4. Use groups for role bindings instead of individual users
5. Document all RBAC changes
6. Use service accounts for applications
7. Avoid using cluster-admin role when possible
