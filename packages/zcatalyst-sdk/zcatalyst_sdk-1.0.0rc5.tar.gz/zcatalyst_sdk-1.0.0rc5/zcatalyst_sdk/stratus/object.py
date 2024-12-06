

from typing import Dict
from ..types.stratus import (
    StratusObjectDetails,
    ObjectVersionsRes,
    StratusObjectsRes
)
from .. import validator
from ..exceptions import CatalystStratusError
from ..types import ParsableComponent
from .._http_client import AuthorizedHttpClient
from .._constants import (
    RequestMethod,
    CredentialUser,
    Components
)

class StratusObject(ParsableComponent):
    def __init__(self, bucket_instance, object_details: Dict):
        validator.is_non_empty_dict(object_details, 'object_details', CatalystStratusError)
        self._requester: AuthorizedHttpClient = bucket_instance._requester
        self._object_name = object_details.get('key')
        self.object_details = object_details
        self.req_params = {
            'bucket_name': bucket_instance.get_name(),
            'object_key': self._object_name
        }

    def __repr__(self) -> str:
        return str(self.object_details)

    def get_component_name(self):
        return Components.STRATUS

    def get_details(self, version_id = None) -> StratusObjectDetails:
        """Get the object details.

        Args:
            version_id (str, optional): Id to get specific version of object details.
            Defaults to None.

        Permission: admin

        Returns:
            StratusObjectDetails: Response of the get details operation.
        """
        params = {
            **self.req_params,
            'version_id': version_id
        }
        resp = self._requester.request(
            method=RequestMethod.GET,
            path='/bucket/object',
            params = params,
            user=CredentialUser.ADMIN
        )
        data = resp.response_json.get('data')
        return data

    def list_paged_versions(
        self,
        max_versions = None,
        next_token = None
    ) -> StratusObjectsRes:
        """Get the list of versions for the given object.

        Args:
            max_versions (str, optional): Maximum number of versions returned in the response.
                Defaults to None.
            next_token (str, optional): Token to get next set of versions if available.
                Defaults to None.

        Permission: admin

        Returns:
            StratusObjectsRes: List of versions and it's details.
        """
        req_params = {
            **self.req_params,
            'max_versions':  max_versions,
            'continuation_token': next_token
        }
        resp = self._requester.request(
            method=RequestMethod.GET,
            path='/bucket/object/versions',
            params = req_params,
            user=CredentialUser.ADMIN
        )
        data = resp.response_json.get('data')
        return data

    def list_iterable_versions(self, max_versions = None):
        """Get the list of versions as iterable.

        Args:
            max_versions (str, optional): Maximum number of versions returned in response.
            Defaults to None.

        Permission: admin

        Yields:
            versions: version details.
        """
        next_token: str = None
        while True:
            data: ObjectVersionsRes = self.list_paged_versions(max_versions, next_token)
            yield from data['version']
            if not data['is_truncated']:
                break
            next_token = data['next_token']

    def put_meta(self,meta_details: Dict[str, str]) -> Dict[str, str]:
        """Add meta details to the object.

        Args:
            meta_details (Dict[str, str]): Add meta details in the form of key valur pairs.

        Permission: admin

        Returns:
            Dict[str, str]: Response of the put meta operation.
        """
        meta_data = {
            'meta_data': meta_details
        }
        resp = self._requester.request(
            method=RequestMethod.PUT,
            path='/bucket/object/metadata',
            params = self.req_params,
            json=meta_data,
            user=CredentialUser.ADMIN
        )
        data = resp.response_json.get('data')
        return data

    def generate_cache_signed_url(self, url, expires=None) -> Dict[str,str]:
        """Generate cache signed url for the object in caching enabled bucket.

        Args:
            url (str): Cached url of the object.
            expires (str, optional): Time in seconds. Defaults to None.

        Permission: admin

        Returns:
            Dict[str,str]: Response of the generate cache signed url.
        """
        req_param = {
            'url': url,
            'expiry_in_seconds': expires
        }
        resp = self._requester.request(
            method=RequestMethod.GET,
            path='/auth/signed-url',
            params = req_param,
            user=CredentialUser.ADMIN
        )
        data = resp.response_json.get('data')
        return data

    def to_dict(self):
        return self.object_details

    def to_string(self):
        return repr(self)
