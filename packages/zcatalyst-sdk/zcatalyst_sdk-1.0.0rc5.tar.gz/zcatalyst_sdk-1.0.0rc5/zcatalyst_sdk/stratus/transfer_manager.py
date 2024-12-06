from io import BufferedReader
import logging
import asyncio
from typing import Union

from requests import RequestException

from ..stratus.bucket import Bucket

from . import validator

from ..types.stratus import MultipartUploadSummaryRes

from ..exceptions import CatalystStratusError
from ..types import Component
from .._http_client import AuthorizedHttpClient
from .._constants import Components

logger = logging.getLogger()

class MultipartUpload():
    def __init__(self, bucket_instance, object_name, upload_id):
        self._requester: AuthorizedHttpClient = bucket_instance._requester
        self.bucket: Bucket = bucket_instance
        self.object_name = object_name
        self.upload_id = upload_id

    def upload_part(self,
            data: Union[BufferedReader, bytes],
            part_number: Union[str, int]
    ) -> bool:
        """Upload the individual parts of the file, with a distinct part number.

        Args:
            data (Union[BufferedReader, bytes]): Body of the object.
            part_number (Union[str, int]): Number to ordering the object parts.

        Permission: admin, user

        Returns:
            bool:'True' if upload part operation is completed successfully.
        """
        resp = self.bucket.upload_part(self.object_name, self.upload_id, data, part_number)
        return resp

    def complete_upload(self) -> bool:
        """Completes the multipart upload.

        Permission: admin, user

        Returns:
            bool: 'True' if the multipart upload is completed successfully.
        """
        resp = self.bucket.complete_multipart_upload(self.object_name, self.upload_id)
        return resp

    def get_upload_summary(self) -> MultipartUploadSummaryRes:
        """Get a summary of the uploaded parts.

        Permission: admin, user

        Returns:
           MultipartUploadSummaryRes: Details of the multipart upload.
        """
        resp = self.bucket.get_multipart_upload_summary(self.object_name, self.upload_id)
        return resp


class TransferManager(Component):
    def __init__(self, bucket_instance):
        self._requester: AuthorizedHttpClient = bucket_instance._requester
        self.bucket: Bucket = bucket_instance
        self.bucket_domain = bucket_instance.bucket_domain

    def get_component_name(self):
        return Components.STRATUS

    def create_multipart_instance(self, object_name: str, upload_id: str = None) -> MultipartUpload:
        """Initializing the multipart upload to create the multipart instance.

        Args:
            object_name (str): Name of the object.
            upload_id(str, optional): Upload Id if the the upload is already initiated.

        Permission: admin, user

        Returns:
            MultipartUpload: MultipartUpload Instance.
        """
        if not upload_id:
            upload_id = self.bucket.initiate_multipart_upload(object_name)['upload_id']
        return MultipartUpload(self.bucket, object_name, upload_id)

    def _get_object_part(
        self,
        object_name: str,
        start: int,
        end: int,
        version_id: str = None,
        retry = 3
    ):
        """Get part of the object in the bucket.

        Args:
            object_name (str): Name of the object.
            start (int): starting byte or the lower bound of the byte range.
            end (int): ending byte or the upper bound of the byte range.
            version_id (str, optional): A unique identifier for the specific version of the object.
            retry (int, optional): Retry the request when failed. Defaults to 3.

        Raises:
            CatalystStratusError: Raised if the object_name, start, or end values are empty.

        Returns:
            stream: part of the object as stream.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        validator.is_parsable_number(start, 'start_value', CatalystStratusError)
        validator.is_parsable_number(end, 'end_value', CatalystStratusError)
        try:
            data = self.bucket.get_object(
                object_name, { 'version_id': version_id, 'range':f'{start}-{end}'})
        except RequestException as err:
            if retry < 0:
                raise CatalystStratusError(
                    'STRATUS ERROR',
                    'Error while downloading the object',
                    object_name
                    ) from err
            retry-=1
            self._get_object_part(object_name, start, end, version_id, retry)
        return data

    def get_iterable_object(self, object_name: str, part_size: int, version_id: str = None):
        """Get an object as iterable multipart streams.

        Args:
            object_name (str): Name of the object.
            part_size (str): Size of the individual object part.
            version_id (str, optional): A unique identifier for the specific version of the object.

        Returns:
            str: success message

        Permission: admin

        Yields:
            stream: part of the object as stream.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        validator.is_parsable_number(part_size, 'part_size', CatalystStratusError)
        part_size = part_size * (1024 * 1024)
        file_size = self.bucket.object(object_name).get_details()['size']
        start=0
        while start < file_size:
            end_range = min(start + part_size, file_size) - 1
            res = self._get_object_part(object_name, start, end_range, version_id)
            yield res
            start = end_range + 1
        return "Successfully Downloaded"

    async def _upload_part(
        self,
        part_ins: MultipartUpload,
        chunk: BufferedReader,
        part_number: int
    ):
        res = part_ins.upload_part(chunk, str(part_number) + '')
        if res:
            logger.info('Part %d Uploaded', part_number)
        else:
            raise CatalystStratusError('STRATUS ERROR',
                f'Error while uploading the object {part_ins.object_name}')
        return res

    def generate_part_downloaders(self, object_name: str, part_size: int, version_id = None):
        """Get the object as a list of downloadable parts.

        Args:
            object_name (str): Name of the object.
            part_size (int): Size of the individual object part.
            version_id (str, optional): A unique identifier for the specific version of the object.

        Permission: admin

        Returns:
            List[Function]: List of downloadable object parts.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        validator.is_parsable_number(part_size, 'part_size', CatalystStratusError)
        part_size = part_size * (1024 * 1024)
        file_size = self.bucket.object(object_name).get_details()['size']
        parts = []
        start = 0
        while start < file_size:
            end_range = min(start + part_size, file_size) - 1
            parts.append(
                lambda start=start,
                        end_range=end_range,
                        object_name=object_name,
                        version_id=version_id:
                self._get_object_part(object_name, start, end_range, version_id)
            )
            start = end_range + 1
        return parts

    def put_object_as_parts(self, object_name: str, file: BufferedReader, part_size: int) -> str:
        """Upload the object as multiple parts and combine these parts into single object.

        Args:
            object_name (str): Name of the object.
            file (BufferedReader): Body of the object.
            part_size (int): Size of the individual object part.

        Permission: admin, user

        Returns:
            str: success message.
        """
        validator.is_non_empty_string(object_name, 'object_name', CatalystStratusError)
        validator.is_parsable_number(part_size, 'part_size', CatalystStratusError)
        return asyncio.run(self._put_object(object_name, file, part_size))

    async def _put_object(self, object_name: str, file: BufferedReader, part_size: int):
        part_size = part_size * (1024 * 1024)
        initiate_res = self.create_multipart_instance(object_name)
        part_number = 1
        tasks = []
        try:
            while True:
                chunk = file.read(part_size)
                if not chunk:
                    break
                tasks.append(self._upload_part(initiate_res, chunk, part_number))
                part_number += 1
                if part_number > 1000:
                    raise CatalystStratusError(
                        'invalid-partsize',
                        'Part number exceeded the limit 1000. Please increase the part size.',
                        object_name
                    )
        except Exception as err:
            raise CatalystStratusError('STRATUS_ERROR', str(err), object_name) from None

        uploaded_parts = await asyncio.gather(*tasks)

        if uploaded_parts:
            complete_res = initiate_res.complete_upload()
            if complete_res:
                logger.info('Upload Completed')
            else:
                raise CatalystStratusError(
                    'STRATUS_ERROR',
                    'Error while completing multipart upload',
                    object_name
                ) from None

        return 'success'
