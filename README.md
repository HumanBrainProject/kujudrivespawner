# KubeSpawner Jupyterhub Seadrive integration

This library provides an integration with seadrive by setting up a
seadrive sidecar container in the same pod as the notebook container
for each user and mounting the user's seadrive libraries in a shared
mount.

## Requirements

### OAuth 2.0

This setup relies on OAuth bearer tokens to obtain a token from seafile.

Seahub must be patched to add an extra API endpoint to obtain the
seadrive token using a bearer token.

### Pod Security Policies or Security Context Constraints

Kubernetes needs an appropriate pod security policy (PSP) to allow
Jupyterhub to create privileged containers. If using OpenShift, this
can be handled with a security context constraints (SCC) instead.
