from io import BufferedReader
from typing import List, Dict, Literal, Union
import mimetypes
import urllib.parse

from .. import validator
from ..exceptions import CatalystAPIError, CatalystStratusError
from ..types import ParsableComponent
from ..types.stratus import (
    StratusObjectsRes,
    StratusBucket,
    CopyObjectResponse,
    BucketCorsResponse,
    DeleteObjectOptions,
    InitiateMultipartUploadResponse,
    RenameObjectResponse,
    MultipartUploadSummaryRes,
    StratusDownloadOptions,
    StratusUploadOptions,
    UnzipObjectResponse,
    DeleteObjectPathResponse
)
from .object import StratusObject
from .._http_client import AuthorizedHttpClient
from .._constants import (
    STRATUS_SUFFIX,
    ENVIRONMENT,
    RequestMethod,
    CredentialUser,
    CatalystService,
    Components
)
from ._auth_util import AuthUtil

class Bucket(ParsableComponent):
    def __init__(self, stratus_instance, bucket_details: Dict):
        validator.is_non_empty_dict(bucket_details, 'bucket_details', CatalystStratusError)
        self._requester: AuthorizedHttpClient = stratus_instance._requester
        self._bucket_name = bucket_details.get('bucket_name')
        self.bucket_details = bucket_details
        self._auth_util = AuthUtil(self)
        if self._requester._app.config.get(ENVIRONMENT) == 'Development':
            self.bucket_domain = f'https://{self._bucket_name}-development{STRATUS_SUFFIX}'
        else:
            self.bucket_domain = f'https://{self._bucket_name}{STRATUS_SUFFIX}'

    def __repr__(self) -> str:
        return str(self.bucket_details)

    def get_component_name(self):
        return Components.STRATUS

    def get_name(self):
        return self._bucket_name

    def get_details(self) -> StratusBucket:
        """Retrieves details of the bucket.

        Permission: admin

        Returns:
            StratusBucket: Bucket details.
        """

        resp = self._requester.request(
            method=RequestMethod.GET,
            path='/bucket',
            user=CredentialUser.ADMIN
        )
        data: StratusBucket = resp.response_json.get('data')[0]
        return data

    def list_paged_objects(
        self,
        max_keys = None,
        prefix = None,
        next_token = None,
        folder_listing = False
    ) -> StratusObjectsRes:
        """Lists all objects in the bucket with their details, using pagination.

        Args:
            max_keys (int, optional): The maximum number of objects returned in a single response.
                Defaults to 1000.
            prefix (str, optional): Get the response keys that starts with this prefix.
            next_token (str, optional): When the response is truncated (truncated is set to true),
                the response includes the next_continuation_token element. To get the next
                    list of objects, this token can be used as continuationToken query parameter.
            folder_listing (bool, optional): Enables listing of objects in a folder structure.
                Defaults to False.

        Permission: admin

        Returns:
            List[StratusObjectsRes]: List of objects in the bucket.
        """
        req_params = {
            'bucket_name': self._bucket_name,
            'max_keys':  max_keys,
            'prefix': prefix,
            'continuation_token': next_token,
            'folder_listing': folder_listing
        }
        resp = self._requester.request(
            method=RequestMethod.GET,
            path='/bucket/objects',
            params= req_params,
            user=CredentialUser.ADMIN
        )
        data: StratusObjectsRes = resp.response_json.get('data')
        objects: List[StratusObject] = []
        for key in data['contents']:
            objects.append(StratusObject(self, key))
        data['contents'] = objects
        return data

    def list_iterable_objects(self, prefix = None, max_keys = None):
        """Lists the objects in the bucket using pagination.

        Args:
            prefix (str, optional): Get the response keys that starts with this prefix.
            max_keys (int, optional): The maximum number of objects returned in a single response.
                Defaults to 1000.

        Permission: admin

        Yields:
            List[Objects]: List the objects in the bucket.
        """
        next_token: str = None
        while True:
            objects = self.list_paged_objects(max_keys, prefix, next_token)
            yield from objects['contents']
            if not objects['truncated']:
                break
            next_token = objects['next_continuation_token']

    # def get_multiple_objects(
    #     self,
    #     objects: Union[List[str], str],
    #     prefix: List[str] = None,
    #     next_token = None
    # ):
    #     """Download one or more objects in the bucket as zip.

    #     Args:
    #         objects (Union[List[str], str]): List of object names or '*' or 'Top'
    #         prefix (List[str], optional): List of prefix. Defaults to [].
    #         next_token (str, optional): Token to continue next iteration . Defaults to None.

    #     Returns:
    #         stream: Downloaded content as stream
    #     """
    #     if isinstance(objects, list):
    #         objects = [{'key': key} for key in objects]

    #     req_json = {
    #         'objects': objects,
    #         'prefix': prefix
    #     }
    #     resp = self._requester.request(
    #         method=RequestMethod.POST,
    #         json= req_json,
    #         params= {'continuationToken': next_token},
    #         url=self.bucket_domain + '/?zip',
    #         external = True,
    #         catalyst_service=CatalystService.STRATUS,
    #         user=CredentialUser.USER
    #     )
    #     data = resp.response.content
    #     response = {
    #         'data' : data,
    #         'continuation_token' : resp.headers.get('Continuation-Token')
    #     }
    #     return response

    def put_object(
        self,
        object_name: str,
        body: Union[BufferedReader, str, bytes],
        options: StratusUploadOptions = None
    ):
        """Upload an object to the bucket.

        Args:
            object_name (str): Name of the object.
            body (Union[BufferedReader, str, bytes]): The content of the object to upload.
            options (StratusUploadOptions, optional): Optional configuration options for the upload.
                Defaults to None.

        Permission: admin, user

        Returns:
            bool: 'True' if the upload was successful, otherwise 'False'.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        self._validate_object_body(body)

        content_type, _other = mimetypes.guess_type(object_name)
        auth_sign = self._auth_util.get_bucket_signature()
        url = self.bucket_domain + ('/_signed' if auth_sign else '')
        header = {
            'compress': 'false'
        }
        if options:
            header['overwrite'] = options.get('overwrite')
            header['expires-after'] =  options.get('ttl')
            meta_data = options.get('meta_data')
            meta_data =  ";".join([f"{key}={value}" for key, value in meta_data.items()]) + ";" \
                if meta_data else None
            header['x-user-meta'] =  meta_data
        if content_type:
            header['Content-Type'] = content_type

        resp = self._requester.request(
            method=RequestMethod.PUT,
            url=url + f'/{urllib.parse.quote(object_name)}',
            data=body,
            params=auth_sign,
            stream=True,
            headers=header,
            external = True,
            auth=not auth_sign,
            catalyst_service=CatalystService.STRATUS,
            user=CredentialUser.USER
        )
        return resp.status_code == 200

    def truncate(self) -> Dict[str,str]:
        """Delete all objects in the bucket, effectively emptying it.

        Permission: admin

        Returns:
            Dict[str,str]: A message indicating the initiation of the truncation process.
        """
        param = { 'bucket_name': self._bucket_name }
        resp = self._requester.request(
			method= RequestMethod.DELETE,
			path= '/bucket/truncate',
			params=param,
			user= CredentialUser.ADMIN
        )
        return resp.response_json.get('data')

    def get_object(self, object_name: str, options: StratusDownloadOptions = None):
        """Download an object from the bucket..

        Args:
            object_name (str): Name of the object.
            options (StratusDownloadOptions, optional):
                Set of options to download the object. Defaults to None.

        Permission: admin, user

        Returns:
            stream: Object in the form of stream.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        sign = self._auth_util.get_bucket_signature() or {}
        params = {**sign}
        headers = {}
        if options:
            headers['Range'] = 'bytes=' + options.get('range') if options.get('range') else None
            params['version_id'] =  options.get('version_id')
        url = self.bucket_domain + ('/_signed' if sign else '')
        resp = self._requester.request(
            method=RequestMethod.GET,
            url= url + f'/{urllib.parse.quote(object_name)}',
            params=params,
            stream=True,
            catalyst_service=CatalystService.STRATUS,
            headers=headers,
            external=True,
            auth=not sign,
            user=CredentialUser.USER
        )
        data = resp.response.content
        return data

    def delete_object(self,
        object_name: str,
        version_id: str = None,
        ttl: Union[str, int] = None
    ) -> Dict[str, str]:
        """Delete the object in the bucket.

        Args:
            object_name (str): Name of the object.
            version_id(str, optional): A unique identifier for the specific version of the object.
            ttl(Union[str, int], optional): Time delay (in seconds) before the object is deleted.

        Permission: admin, user

        Returns:
            Dict[str, str]: The result of the delete multiple objects operation.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        if (self._auth_util.get_user_type() == 'admin' or \
            self._auth_util.get_user_scope() == 'admin'):
            objects = [{
                'key': object_name,
                'version_id': version_id
            }]
            return self.delete_objects(objects, ttl)
        options = {
            'versionId': version_id,
            'deleteAllVersions': not version_id,
            'ttl': ttl
        }
        resp = self._requester.request(
                method=RequestMethod.DELETE,
                url=f'{self.bucket_domain}/{urllib.parse.quote(object_name)}',
                params={ **options },
                external=True,
                catalyst_service=CatalystService.STRATUS,
                user=CredentialUser.USER
            )
        data = { 'message': resp.response.content }
        return data

    def delete_objects(
        self,
        objects: List[DeleteObjectOptions],
        ttl: Union[str, int] = None
    ) -> Dict[str, str]:
        """Delete multiple objects in the bucket.

        Args:
            objects (List[DeleteObjectOptions]): A list of objects to be deleted,
                including their version IDs (if versioning is enabled).
            ttl(Union[str, int], optional): Time delay (in seconds) before the object is deleted.

        Permission: admin

        Returns:
            Dict[str, str]: Result of deleting multiple objects.
        """
        validator.is_non_empty_list(objects, 'objects_list', CatalystStratusError)
        req_body = {
            'objects': objects,
            'ttl_in_seconds': ttl
        }
        resp = self._requester.request(
            method=RequestMethod.PUT,
            path='/bucket/object',
            params={'bucket_name':self._bucket_name},
            json=req_body,
            user=CredentialUser.ADMIN
        )
        data = resp.response_json.get('data')
        return data

    def get_cors(self) -> List[BucketCorsResponse]:
        """Get the CORS details of the bucket.

        Permission: admin

        Returns:
            List[BucketCorsResponse]: List of CORS configured for the bucket.
        """
        resp = self._requester.request(
            method=RequestMethod.GET,
            path='/bucket/cors',
            params={'bucket_name':self._bucket_name},
            user=CredentialUser.ADMIN
        )
        data = resp.response_json.get('data')
        return data

    def purge_cache(self, objects: List[str] = None) -> Dict[str,str]:
        """Clear the cached objects in the bucket.

        Args:
            objects (List[str], optional): A list of object names or paths to be cleared
                from the cache. If not provided, all cached items will be cleared.

        Permission: admin

        Returns:
            Dict[str, str]: The result of the purge cache.
        """
        resp = self._requester.request(
            method=RequestMethod.PUT,
            path='/bucket/purge-cache',
            params={'bucket_name':self._bucket_name},
            json=objects or [],
            user=CredentialUser.ADMIN
        )
        data = resp.response_json.get('data')
        return data

    def unzip_object(self, object_name: str, dest_path: str) -> UnzipObjectResponse:
        """Extract the contents of a ZIP object and upload each file as an
            individual object to the same bucket.

        Args:
            object_name (str): Name of the object.
            dest_path (str): The destination path where the object will be extracted.

        Permission: admin

        Returns:
            UnzipObjectResponse: Response of the unzip object operation.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        validator.is_non_empty_string_or_number(dest_path, 'dest_path', CatalystStratusError)
        req_json = {
            'bucket_name': self._bucket_name,
            'object_key': object_name,
            'destination': dest_path
        }
        resp = self._requester.request(
            method=RequestMethod.POST,
            path='/bucket/object/zip-extract',
            params=req_json,
            user=CredentialUser.ADMIN
        )
        data = resp.response_json.get('data')
        return data

    def get_unzip_status(self, object_name: str, task_id: Union[str, int]) -> Dict[str, str]:
        """Get the status of the unzipObject operation.

        Args:
            object_name (str): Name of the object.
            task_id (Union[str, int]): The ID returned after initiating the unzip operation,
                used to track the task's progress.

        Permission: admin

        Returns:
            Dict[str,str]: Result of the uzip status.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        validator.is_non_empty_string_or_number(task_id, 'task_id', CatalystStratusError)
        req_json = {
            'bucket_name': self._bucket_name,
            'object_key': object_name,
            'task_id': task_id
        }
        resp = self._requester.request(
            method=RequestMethod.GET,
            path='/bucket/object/zip-extract/status',
            params=req_json,
            user=CredentialUser.ADMIN
        )
        data = resp.response_json.get('data')
        return data

    def generate_presigned_url(
        self,
        object_name: str,
        url_action: Literal['PUT', 'GET'],
        expiry_in_sec: str = None,
        active_from: str = None,
        version_id: str = None
    ) -> Dict[str,str]:
        """Generate pre signed url for the given object.

        Args:
            object_name (str): Name of the object.
            url_action (Literal['PUT', 'GET']): Operation to be performed using the generated URL.
            expiry_in_sec (str, optional): Expiry time in seconds. Defaults to None.
            active_from (str, optional):
                Date in milliseconds, the URL will be active from the given date. Defaults to None.
            version_id (str, optional): Version id to download the particular version of the object.
                Only for 'GET' url action.

        Permission: admin

        Returns:
            Dict[str, str]: The pre-signed URL for accessing the object.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        validator.is_non_empty_string(url_action, 'url_action', CatalystStratusError)
        req_param = {
            'bucket_name': self._bucket_name,
            'object_key': object_name,
            'expiry_in_seconds': expiry_in_sec,
            'active_from': active_from,
            'version_id': version_id
        }
        resp = self._requester.request(
            method= url_action,
            path='/bucket/object/signed-url',
            params = req_param,
            user=CredentialUser.ADMIN,
            catalyst_service=CatalystService.SERVERLESS
        )
        data = resp.response_json.get('data')
        return data

    def delete_path(self, path) -> DeleteObjectPathResponse:
        """Delete the given path and it's objects in the bucket.

        Args:
            path (str): The path to delete.

        Permission: admin

        Returns:
            DeleteObjectPathResponse: Result of the delete path.
        """
        validator.is_non_empty_string(path, 'path', CatalystStratusError)
        req_json = {
            'bucket_name': self._bucket_name,
            'prefix': path
        }
        resp = self._requester.request(
            method=RequestMethod.DELETE,
            path='/bucket/object/prefix',
            params=req_json,
            user=CredentialUser.ADMIN
        )
        data = resp.response_json.get('data')
        return data

    def head_object(self, object_name, version_id = None, throw_err = None) -> bool:
        """Check if a specific object exists and if the user has permission to access it.

        Args:
            object_name (str): Name of the object
            version_id (str, optional):The version ID to check for a specific version.
                Defaults to None.
            throw_err (boolean, optional):
                Set to 'True' to throw an error if the object is not found;
                otherwise, it returns a boolean indicating the result. Defaults to 'False.'

        Permission: admin

        Raises:
            CatalystStratusError: If the object name is empty.
            CatalystAPIError: If the object is not found and `throw_err` is True.

        Returns:
            bool: 'True' if the object exists and the user has access, 'False' otherwise.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        try:
            param = {
                'bucket_name': self._bucket_name,
                'object_key': object_name,
                'version_id': version_id
            }
            resp = self._requester.request(
                method=RequestMethod.HEAD,
                path='/bucket/object',
                params = param,
                catalyst_service=CatalystService.SERVERLESS,
                user=CredentialUser.ADMIN
            )
            return resp.status_code == 200
        except CatalystAPIError as err:
            if not throw_err:
                if err.http_status_code in (404, 403, 400):
                    return False
            raise err

    def copy_object(self, source_object, dest_object) -> CopyObjectResponse:
        """Copy the given object to the destination.

        Args:
            source_object (str): Name of the source object.
            dest_object (str): Name of the destination object.

        Raises:
            CatalystStratusError: If any errors happen.

        Permission: admin

        Returns:
            CopyObjectResponse: Response of the copy operation.
        """
        req_json = {
            'bucket_name': self._bucket_name,
            'object_key': source_object,
            'destination': dest_object
        }
        validator.is_non_empty_string(source_object, 'source_object', CatalystStratusError)
        validator.is_non_empty_string(dest_object, 'dest_object', CatalystStratusError)
        resp = self._requester.request(
            method=RequestMethod.POST,
            path='/bucket/object/copy',
            params=req_json,
            user=CredentialUser.ADMIN
        )
        data = resp.response_json.get('data')
        return data

    def rename_object(self, source_object, dest_object) -> RenameObjectResponse:
        """Renames an object in the bucket.

        Args:
            source_object (str): Current name of the object.
            dest_object (str): New name of the object.

        Permission: admin

        Returns:
            RenameObjectResponse: Details of the renamed object.
        """
        validator.is_non_empty_string(source_object, 'source_object', CatalystStratusError)
        validator.is_non_empty_string(dest_object, 'dest_object', CatalystStratusError)
        req_json = {
            'bucket_name': self._bucket_name,
            'current_key':source_object,
            'rename_to': dest_object
        }
        resp = self._requester.request(
            method=RequestMethod.PATCH,
            path='/bucket/object',
            params=req_json,
            user=CredentialUser.ADMIN
        )
        data = resp.response_json.get('data')
        return data

    def initiate_multipart_upload(self, object_name: str) -> InitiateMultipartUploadResponse:
        """To Initiate the multipart upload.

        Args:
            object_name (str): Name of the object.

        Permission: admin, user

        Returns:
            InitiateMultipartUploadResponse: Initiated the multipart upload and returns the details.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        content_type, _other = mimetypes.guess_type(object_name)
        sign = self._auth_util.get_bucket_signature()
        url = self.bucket_domain + ('/_signed' if sign else '')
        auth = not bool(sign)
        resp = self._requester.request(
            method=RequestMethod.PUT,
            url=url +f'/{urllib.parse.quote(object_name)}?multipart',
            headers={
                'compress': 'false',
                'Content-Type': content_type if content_type else 'application/octet-stream'
            },
            params=sign,
            catalyst_service=CatalystService.STRATUS,
            auth= auth,
            external=True,
            user=CredentialUser.USER
        )
        return resp.response_json

    def upload_part(self,
            object_name: str,
            upload_id: str,
            data: Union[BufferedReader, bytes],
            part_number: Union[str, int],
            overwrite = 'false'
    ) -> bool:
        """Upload the individual parts of the file, with a distinct part number.

        Args:
            object_name(str): Name of the object.
            upload_id(str): Unique identifier for the multipart upload.
            data (Union[BufferedReader, bytes]): Body of the object.
            part_number (Union[str, int]): A unique number for the part to be uploaded,
                used for determining the position in the order of combining the multipart object.

        Permission: admin, user

        Returns:
            bool:'True' if upload part operation was completed successfully.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        validator.is_non_empty_string(upload_id, 'upload_id', CatalystStratusError)
        if not validator.is_buffered_reader(data) and not isinstance(data, bytes):
            raise CatalystStratusError(
                'Invalid-Argument',
                'Object part must be an instance of BufferedReader.', type(data)
            )
        sign = self._auth_util.get_bucket_signature() or {}
        url = self.bucket_domain + ('/_signed' if sign else '')
        params = {
            'uploadId': upload_id,
            'partNumber': part_number,
            **sign
        }
        resp = self._requester.request(
            method=RequestMethod.PUT,
            url= url +f'/{urllib.parse.quote(object_name)}',
            headers = {
                'overwrite': overwrite,
            },
            data=data,
            params=params,
            stream=True,
            catalyst_service=CatalystService.STRATUS,
            auth = not bool(sign),
            external=True,
            user=CredentialUser.USER
        )
        return resp.status_code == 200

    def complete_multipart_upload(self, object_name: str, upload_id: str) -> bool:
        """To Complete the multipart upload.

        Args:
            object_name(str): Name of the object.
            upload_id(str): Unique identifier for the multipart upload.

        Permission: admin, user

        Returns:
            bool: 'True' if the multipart upload was completed successfully..
        """

        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        validator.is_non_empty_string(upload_id, 'upload_id', CatalystStratusError)
        sign = self._auth_util.get_bucket_signature() or {}
        url = self.bucket_domain + ('/_signed' if sign else '')
        resp = self._requester.request(
            method=RequestMethod.PUT,
            url= url +f'/{urllib.parse.quote(object_name)}?completeMultipart',
            params={
                'uploadId': upload_id,
                **sign
            },
            catalyst_service=CatalystService.STRATUS,
            auth=not bool(sign),
            external = True,
            user=CredentialUser.USER
        )
        data = resp.status_code
        return data == 202

    def get_multipart_upload_summary(
        self,
        object_name: str,
        upload_id: str
    ) -> MultipartUploadSummaryRes:
        """Get a summary of the uploaded parts.

        Args:
            object_name(str): Name of the object.
            upload_id(str): Unique identifier for the multipart upload.

        Permission: admin, user

        Returns:
            MultipartUploadSummaryResRes: Details the of multipart upload object.
        """

        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        validator.is_non_empty_string(upload_id, 'upload_id', CatalystStratusError)
        sign = self._auth_util.get_bucket_signature() or {}
        url = self.bucket_domain + ('/_signed' if sign else '')
        resp = self._requester.request(
            method=RequestMethod.GET,
            url=url +f'/{urllib.parse.quote(object_name)}?multipartSummary',
            params={
                **sign,
                'uploadId': upload_id
            },
            catalyst_service=CatalystService.STRATUS,
            auth = not bool(sign),
            external = True,
            user=CredentialUser.USER
        )
        return resp.response_json


    def object(self, object_name) -> StratusObject:
        """Get the object Instance.

        Args:
            object_name (str): Name of the object.

        Permission: admin, user

        Returns:
            StratusObject: object instance.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        return StratusObject(self, {'key': object_name })

    def _validate_object_body(self, object_body):
        if not isinstance(object_body, (BufferedReader, bytes, memoryview, bytearray)) \
            and not validator.is_non_empty_string(object_body):
            raise CatalystStratusError(
                'invalid_object_body',
                'Object must be an instance of BufferReader or string and cannot be empty'
            )

    def to_dict(self):
        return self.bucket_details

    def to_string(self):
        return repr(self)
