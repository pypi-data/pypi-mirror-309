from datetime import datetime
from typing import Dict
import urllib.parse

# from . import Bucket
from .._constants import (CredentialUser, RequestMethod)

class AuthUtil:
    sign: Dict = None
    def __init__(self, bucket) -> None:
        self.bucket = bucket
        self._requester = bucket._requester
        self.user_type = self._requester._app.credential.current_user_type()
        self.user = self._requester._app.credential.current_user()

    def get_user_type(self) -> str:
        return self.user_type

    def get_user_scope(self) -> str:
        return self.user

    def get_bucket_signature(self) -> Dict[str, str]:
        """Get the bucket signature.

        Permission: admin

        Returns:
            Dict[str, str]: Return the signature.
        """
        if self.user_type == 'admin' or self.user == 'admin':
            if self.sign and int(self.sign.get('expiry_time')) > \
                int(datetime.now().timestamp() * 1000):
                return urllib.parse.parse_qs(self.sign.get('signature'))
            req_params = {
                'bucket_name': self.bucket.bucket_details.get('bucket_name')
            }
            resp = self._requester.request(
                method=RequestMethod.POST,
                path='/bucket/signature',
                params= req_params,
                user=CredentialUser.ADMIN
            ).response_json.get('data')
            self.sign = resp
            return urllib.parse.parse_qs(resp.get('signature'))
        return None
