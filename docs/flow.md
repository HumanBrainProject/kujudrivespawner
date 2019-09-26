# Spawner principles

## Flow

Before spawning a notebook, the spawner connects to a patched seafile instance to obtain a seafile token using an OAuth bearer token.

The bearer token is used to generate a secret

## Failure modes

The seafile server responds with a
- 401: End result 500
- 5xx: End result 500

Kubernetes API
- Secret creation failure: End result 500
- token update necessary?

KubeSpawner
- Fails to start seadrive-sidecar
- Fails to start notebook-server
