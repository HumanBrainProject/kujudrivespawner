'''
Utilities for the KubeSpawner configuration.
'''

import configparser
import io

from kubernetes.client.models import (
    V1ObjectMeta,
    V1Secret
)
import kubernetes.client.rest
from kubespawner import KubeSpawner
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPClientError
from traitlets import Unicode
from .config import DEFAULT_DRIVE_CONFIG


class KuJuDriveSpawner(KubeSpawner):
    '''The Kubernetes Jupyterhub Drive spawner launches a seadrive sidecar
    container in the user's notebook pod to mount the user's
    libraries.
    '''
    def generate_drive_config(self, url, username, token, **kwargs):
        base = DEFAULT_DRIVE_CONFIG.copy()
        base.update(**kwargs)
        cp = configparser.ConfigParser()
        cp.read_dict(base)
        cp['account'].update(dict(server=url, username=username, token=token))
        cfg = io.StringIO()
        cp.write(cfg)
        cfg.seek(0)
        data = {
            'seadrive.conf': cfg.read()
        }
        metadata = V1ObjectMeta(
            name='seadrive-{username}-conf'.format(username=username),
            annotations={'username': username})
        secret = V1Secret(string_data=data, metadata=metadata)
        return secret

    async def pre_spawn_hook(self, spawner):
        user = spawner.user
        spawner.log.debug("Running pre spawn hook for %s" % user.name)
        auth_state = await user.get_auth_state()
        drive_token = await self.get_drive_token(auth_state)
        secret = self.generate_drive_config(self.drive_url, user.name, drive_token)
        # @todo this could check whether the secret exists first.
        try:
            spawner.api.create_namespaced_secret(self.namespace, secret)
            spawner.log.debug("Created secret for %s" % user.name)
        except kubernetes.client.rest.ApiException as e:
            if e.status == 409:
                # @TODO update?
                pass
            else:
                raise
        return user

    async def get_drive_token(self, auth_state: dict) -> str:
        client = AsyncHTTPClient()
        request = HTTPRequest(
            self.drive_url + '/api2/account/token/',
            headers={'Authorization': 'Bearer {token}'.format(
                token=auth_state['access_token'])},
            connect_timeout=1.0,
            request_timeout=1.0
        )
        try:
            resp = await client.fetch(request)
        except HTTPClientError as e:
            self.log.warning("Failed to obtain drive token for user {username}.\n" +
                             "Exception: {e}".format(username=self.user.name, e=e))
            e.message = 'Your Drive is not initialized yet, please visit {drive_url} to enable your drive account'.format(drive_url=self.drive_url)
            raise
        return resp.body.decode('utf-8')

    drive_url = Unicode(
        allow_none=False,
        config=True,
        help='The url of the Seafile server. eg https://drive.example.com',
    )

    seadrive_sidecar_image = Unicode(
        help='The seadrive sidecar image name and tag.',
        default_value='',
        config=True,
    )
