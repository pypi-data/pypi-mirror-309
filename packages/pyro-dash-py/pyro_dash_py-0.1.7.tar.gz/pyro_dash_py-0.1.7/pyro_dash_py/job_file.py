from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import requests

from .client import PyroApiClient
from .core import POST, PUT, require_resource


@dataclass
class PyroUploadCreds:
    access_key_id: str
    secret_access_key: str
    session_token: str


@dataclass
class PyroUploadIntent:
    creds: PyroUploadCreds
    key: str
    bucket: str
    region: str


def _file_stream_generator(file, chunk_size=25 * 1024 * 1024):
    """
    Stream file data in chunks
    default chunk size is 25 MB

    We use this to upload files in chunks for the multipart upload
    each multipart signed URL receives a chunk

    Example:

    ```python
    fpath = "dev_notes.txt"
    multipart_signed_urls = ["https://s3.fakeUploadLink1.com", "https://s3.fakeUploadLink2.com]
    with open(fpath, "rb") as file:
        i = 0
        for signed_url in multipart_signed_urls:
            print(f"Uploading part {i+1} of {len(multipart_signed_urls)}...")
            chunk = next(_file_stream_generator(file))
            response = requests.put(signed_url, data=chunk)

    ```
    """
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        yield chunk


class PyroJobFileResource:
    def __init__(self, client: PyroApiClient):
        self._client = client

    def create(self, job_id: str, name: str, size: int):
        data = {"display_name": name, "size_bytes": size}
        url = f"jobs/{job_id}/files"
        raw = self._client.request(POST, url, data)
        _dict = {**raw, "_resource": self}
        return PyroFile.from_dict(_dict)

    def update(self, job_id: str, file_id: str, **kwargs) -> "PyroFile":
        url = f"jobs/{job_id}/files/{file_id}"
        resp = self._client.request(PUT, url, data=None, json={**kwargs})
        _dict = {**resp, "_resource": self}
        return PyroFile.from_dict(_dict)

    def create_upload_intent(self, job_id: str, file_id: str):
        url = f"jobs/{job_id}/files/{file_id}/create_upload_intent"
        raw = self._client.request(POST, url)
        intent = PyroUploadIntent(
            PyroUploadCreds(
                raw["creds"]["accessKeyId"],
                raw["creds"]["secretAccessKey"],
                raw["creds"]["sessionToken"],
            ),
            raw["key"],
            raw["bucket"],
            raw["region"],
        )
        return intent

    def signed_url(self, file_id: str):
        url = f"files/{file_id}/signed_url"
        raw = self._client.request(POST, url)
        return raw["url"]

    def signed_url_for_upload(self, file_id: str):
        url = f"files/{file_id}/signed_url_for_upload"
        raw = self._client.request(POST, url)
        return raw["url"]

    def to_s3(self, signed_url: str, fpath: Path):
        with open(fpath, "rb") as file:
            response = requests.put(signed_url, data=file)

    def signed_urls_id_for_multipart_upload(self, file_id: str):
        """
        Initiate process for uploading a a file in parts

        Returns signed URLs and an uploadId

        Example:
        ```python
            urls, uploadId = files.signed_urls_id_for_multipart_upload(file.id)
        ```
        """
        url = f"files/{file_id}/signed_urls_for_multipart_upload"
        raw = self._client.request(POST, url)
        return (
            raw["multipartUploadObject"]["urls"],
            raw["multipartUploadObject"]["uploadId"],
        )

    def multipart_to_s3(
        self, multipart_signed_urls: list[str], fpath: Path
    ) -> list[str]:
        """
        Upload file in 25 MB chunks, one for each multipart signed URL.

        Returns array of eTags

        Each multipartUpload response contains an Etag

        After uploading has finished
        the completeMultiPartUpload command will require all eTags

        Example:

        ```python
        eTags = files.multipart_to_s3(urls, path)
        ```
        """

        eTags = []
        with open(fpath, "rb") as file:
            for i, signed_url in enumerate(multipart_signed_urls):
                print(f"Uploading part {i+1} of {len(multipart_signed_urls)}...")
                try:
                    chunk = next(_file_stream_generator(file))
                    response = requests.put(signed_url, data=chunk)
                except:
                    raise requests.HTTPError("Error when uploading chunk to signed URL")
                if response.status_code != 200:
                    raise requests.HTTPError(
                        f"multipart_to_s3: unexpected status code {response.status_code}"
                    )
                eTag = response.raw.headers["Etag"]
                if eTags.__contains__(eTag):
                    raise ValueError("Duplicate eTag received")
                eTags.append(eTag)
        return eTags

    def complete_multipart_upload(self, file_id, uploadId, eTags):
        """
        Complete a multipart Upload.

        Should only be called after all parts have been uploaded

        Example:
        ```python
        urls, uploadId = files.signed_urls_id_for_multipart_upload(file.id)
        eTags = files.multipart_to_s3(urls, path)
        files.complete_multipart_upload(file.id, uploadId, eTags)

        ```
        """
        url = f"files/{file_id}/complete_multipart_upload"
        raw = self._client.request(
            POST,
            url,
            data={"uploadId": uploadId, "eTags": eTags},
        )
        status_code = raw["completeResponse"]["$metadata"]["httpStatusCode"]
        if status_code != 200:
            raise requests.HTTPError(
                f"complete_multipart_upload: Unexpected status code {status_code}"
            )
        return


@dataclass
class PyroFile:
    id: str
    name: str
    extension: str
    size_bytes: str
    is_active: str
    created_at: str
    status: str
    display_name: str
    s3_uri: Optional[str]
    life_cycle: Optional[str]
    _resource: Optional[PyroJobFileResource]

    @classmethod
    def from_dict(cls, d: dict) -> "PyroFile":
        return PyroFile(
            d["id"],
            d["name"],
            d["extension"],
            d["size_bytes"],
            d["is_active"],
            d["created_at"],
            d["status"],
            d["display_name"],
            d["s3_uri"],
            d["life_cycle"],
            d["_resource"],
        )

    @require_resource
    def to_s3(self):
        raise NotImplementedError

    @require_resource
    def download(self, fpath: Optional[Path] = None):
        assert self._resource is not None
        url = self._resource.signed_url(self.id)
        _path = Path(f"{self.display_name}")

        if fpath is not None:
            if fpath.is_dir():
                _path = fpath / self.display_name
            else:
                _path = fpath

        # FIXME: the entire will be stored in memory
        # should be able to write to disk in chunks
        resp = requests.get(url)

        with open(_path, "wb") as file:
            file.write(resp.content)

        return _path
