from typing import List, Optional
from dataclasses import dataclass
from pathlib import Path

from .job_file import PyroFile, PyroJobFileResource

from .core import (
    GET,
    POST,
    PUT,
    DEL,
    IncompatibleJobTypeError,
    PyroJobTypes,
    PyroJobStatusTypes,
    require_resource,
)
from .client import PyroApiClient


@dataclass
class Validation:
    valid: bool
    issues: list
    warnings: list

    @classmethod
    def from_dict(cls, d: dict) -> "Validation":
        return Validation(
            d["valid"],
            d["issues"],
            d["warnings"],
        )


@dataclass
class PyroJobPreview:
    config: object
    validation: Validation
    file_validation: Validation

    @classmethod
    def from_dict(cls, d: dict) -> "PyroJobPreview":
        return PyroJobPreview(
            d["config"],
            Validation.from_dict(d["validation"]),
            # NOTE: camel case here because this is
            # what we get from the api :,D
            Validation.from_dict(d["fileValidation"]),
        )


@dataclass
class PyroJobRunStats:
    id: str
    type: PyroJobTypes
    status: PyroJobStatusTypes

    @classmethod
    def from_dict(cls, d: dict) -> "PyroJobRunStats":
        return PyroJobRunStats(d["id"], d["type"], d["status"])


@dataclass
class PyroJobInactive:
    id: str
    type: PyroJobTypes
    status: PyroJobStatusTypes
    is_active: bool

    @classmethod
    def from_dict(cls, d: dict) -> "PyroJobInactive":
        return PyroJobInactive(
            d["id"],
            d["type"],
            d["status"],
            d["is_active"],
        )


@dataclass
class PyroJobDuration:
    start: Optional[str]
    end: Optional[str]
    runtime: Optional[str]

    @classmethod
    def from_dict(cls, d: dict) -> "PyroJobDuration":
        return PyroJobDuration(
            d.get("start", None),
            d.get("end", None),
            d.get("runtime", None),
        )


@dataclass
class ItemizedCostEntry:
    compute_time_millis: float
    cents_per_hour: int
    total_cents: float
    is_active: bool

    @classmethod
    def from_dict(cls, d: dict):
        return ItemizedCostEntry(
            d["computeTimeMillis"],
            d["centsPerHour"],
            d["totalCents"],
            d["is_active"],
        )


@dataclass
class PyroJobCost:
    id: str
    total_compute_time_millis: float
    total_cents: float
    itemized_costs: list[ItemizedCostEntry]

    @classmethod
    def from_dict(cls, d: dict):
        return PyroJobCost(
            d["id"],
            d["totalComputeTimeMillis"],
            d["totalCents"],
            [ItemizedCostEntry.from_dict(item) for item in d["itemized"]],
        )


@dataclass
class PyroJobLogs:
    chunk_size: int
    size: int
    start: int
    end: int
    data: list[str]
    presigned_url: str

    @classmethod
    def from_dict(cls, d: dict):
        return PyroJobLogs(
            d["chunkSize"],
            d["size"],
            d["start"],
            d["end"],
            d["data"],
            d["presignedUrl"],
        )


class PyroJobResource:
    """
    An interface for the collection of computation jobs in the Pyro ecosystem.
    Such as WildEST, FSim, Fuelscape, Liability Risk Pipeline, etc.

    Provides a centralized way to perform operations on all of your jobs.
    It is not constrained to one specific job.
    """

    def __init__(self, client: PyroApiClient):
        """
        Constructs a `PyroJobResource`.

        Example:
        ```python
        # requires a PyroApiClient
        client = PyroApiClient(
            host="https://api.dashboard.pyrologix.com",
            email="dev@pyrologix.com",
            apikey="my-pyro-api-key"
        )

        jobs = PyroJobResource(client)
        jobs.create(...)
        jobs.filter(...)
        ```
        """
        self._client = client
        self._endpoint = "jobs"

    @classmethod
    def from_client(cls, client: PyroApiClient) -> "PyroJobResource":
        return PyroJobResource(client)

    def create(self, job_type: str):
        """
        # Create a Job

        ## Example:
        ```python
        pyro = PyroDash(...)
        job = pyro.jobs.create("wildest")
        ```
        """
        raw = self._client.request(POST, self._endpoint, {"type": job_type})
        _dict = {**raw, "_resource": self}
        return PyroJob.from_dict(_dict)

    def get(self, id: str):
        """
        # Retrieve a job by id

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_r62X.."
        job = pyro.jobs.get(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}"
        raw = self._client.request(GET, url)
        _dict = {**raw, "_resource": self}
        return PyroJob.from_dict(_dict)

    def filter(self, **kwargs):
        """
        # Retrieve a list of jobs

        At this time, providing filters is not supported. (Coming soon!)
        So, just returns a list of all of your jobs.

        ## Example:
        ```python
        pyro = PyroDash(...)
        jobs = pyro.jobs.filter()
        ```
        """
        # NOTE: the GET /jobs endpoint accepts filters that are
        # either in the query string OR in the body
        # we specify our filters in the json body because it's more
        # "compatible" with objects (i.e. less buggy)
        resp = self._client.request(GET, self._endpoint, data=None, json={**kwargs})

        jobs = []
        for raw_job in resp["data"]:
            job = PyroJob.from_dict({**raw_job, "_resource": self})
            jobs.append(job)

        return PyroJobList(
            resp["page"],
            resp["limit"],
            resp["totalPages"],
            resp["totalRecords"],
            jobs,
        )

    def update(self, id: str, **kwargs) -> "PyroJob":
        """
        # Update a job

        Allows you to update any property of a job.
        Simply specify the property you wish to update in the kwargs
        of this function. e.g. name="name", config={..}

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_r62X.."
        job = pyro.jobs.update(job_id, name="My Cool Job")
        ```
        """
        # NOTE: unfortunately, api requires the params to be in the body even though
        # this is a put request...
        url = f"{self._endpoint}/{id}"
        resp = self._client.request(PUT, url, data=None, json={**kwargs})
        _dict = {**resp, "_resource": self}
        return PyroJob.from_dict(_dict)

    def set_config(self, id: str, config: dict) -> "PyroJob":
        """
        # Set the config of a job

        Allows you to set the config of a job.
        Keep in mind, this function does not perform any
        config validation. Tread carefully.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_r62X.."
        config = {"num_simulations": 10000, "tile_width": 20000, ...}
        job = pyro.jobs.set_config(job_id, config)
        ```
        """
        # NOTE: unfortunately, api requires the params to be in the body even though
        # this is a put request...
        url = f"{self._endpoint}/{id}"
        resp = self._client.request(PUT, url, data=None, json={"config": config})
        _dict = {**resp, "_resource": self}
        return PyroJob.from_dict(_dict)

    def duplicate(self, id: str) -> "PyroJob":
        """
        # Duplicate a job

        When duplicating a job, only the files, config, and compute config
        are carried over. All results and artifacts are ignored.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_r62X.."
        duped_job = pyro.jobs.duplicate(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/duplicate"
        raw = self._client.request(POST, url)
        _dict = {**raw, "_resource": self}
        return PyroJob.from_dict(_dict)

    def add_file(self, id: str, fpath: str):
        """
        Add a file to a job.

        Given a job id and a path (as a string) to a file
        creates a new file record, binds it to the job, and uploads
        it to the proper s3 location.

        A signed-url is issued by the backend that allows the
        upload to take place client-side.

        If the file is larger than 1 GB, file is uploaded in multiple parts.
        Each part is up to 25 MB.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_r62X.."
        file = pyro.jobs.add_file(job_id, "~/data/wildest_test/trinity_small/slp.tif")
        print(file.name)
        >>> "slp.tif"
        ```
        """
        path = Path(fpath)
        files = PyroJobFileResource(self._client)
        file = files.create(id, path.name, path.stat().st_size)
        intent = files.create_upload_intent(id, file.id)
        if int(file.size_bytes) > (1024**3):
            urls, uploadId = files.signed_urls_id_for_multipart_upload(file.id)
            eTags = files.multipart_to_s3(urls, path)
            files.complete_multipart_upload(file.id, uploadId, eTags)
        else:
            signed_url = files.signed_url_for_upload(file.id)
            files.to_s3(signed_url, path)

        updated_file = files.update(id, file.id, status="ready")
        return updated_file

    def preview(self, id: str) -> PyroJobPreview:
        """
        # Preview a job

        Allows you to "preview" the config, files, and validation
        checks for a job.

        It is recommended that you preview a job before you start it.
        Just to mitigate any potential issues with the job that the system automatically detects.
        If you're missing files, have an illogical config, etc.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        preview = pyro.jobs.preview(job_id)
        ```
        """

        url = f"{self._endpoint}/{id}/preview"
        raw = self._client.request(GET, url)
        return PyroJobPreview.from_dict(raw)

    def start(self, id: str) -> PyroJobRunStats:
        """
        # Start a job

        Starts a job and runs it on the pyro compute platform.

        All compute scaling-up/down is taken care of for you. After a job is
        started, you can check out the logs, monitor the status and duration
        or view it in the dashboard UI!

        The job will run until it enters a "completed" state, in other words,
        until it fails, exits successfully, or is cancelled.

        In order to start a job, the job must have status: "not submitted".
        Otherwise, you will receive an error.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        stats = pyro.jobs.start(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/start"
        raw = self._client.request(POST, url)
        return PyroJobRunStats.from_dict(raw)

    def delete(self, id: str) -> PyroJobInactive:
        """
        # Delete a job

        Deletes a job and all other data and artifacts
        associated with it. Tread carefully.

        Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_eCcxN"
        pyro.jobs.delete(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}"
        raw = self._client.request(DEL, url)
        return PyroJobInactive.from_dict(raw)

    def cancel(self, id: str) -> PyroJobRunStats:
        """
        # Cancel a job

        Stops a job that is running or scheduled to run.

        To run again after cancelling a job, status must be set back to "not submitted".
        This is typically done by using the job.retry() function.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVDw"
        stats = pyro.jobs.cancel(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/cancel"
        raw = self._client.request(POST, url)
        return PyroJobRunStats.from_dict(raw)

    def retry(self, id: str) -> PyroJobRunStats:
        """
        # Retry a job

        Brings a job to a "fresh state" by removing all non-input files
        and cleaning up any compute artifacts.

        After using `retry()` you can run `start()` again.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        stats = pyro.jobs.retry(job_id)
        pyro.jobs.start(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/retry"
        raw = self._client.request(POST, url)
        return PyroJobRunStats.from_dict(raw)

    def list_inputs(self, id: str) -> list[PyroFile]:
        """
        # Lists a job's input files

        Given a job id, returns a list containing `PyroFile` instances.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        inputs = pyro.jobs.list_inputs(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/files"
        resp = self._client.request(GET, url)

        # FIXME: there is no need to do this filter
        # client side. The server can handle this
        # if you provide the right query.
        file_resource = PyroJobFileResource(self._client)
        files: List[PyroFile] = []
        for raw_file in resp:
            if raw_file["life_cycle"] == "input":
                files.append(
                    PyroFile.from_dict({**raw_file, "_resource": file_resource})
                )
        return files

    def list_outputs(self, id: str) -> list[PyroFile]:
        """
        # Lists a job's output files

        Given a job id, returns a list containing `PyroFile` instances.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        outputs = jobs.list_outputs(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/files"
        resp = self._client.request(GET, url)
        # FIXME: there is no need to do this filter
        # client side. The server can handle this
        # if you provide the right query.
        file_resource = PyroJobFileResource(self._client)
        files: List[PyroFile] = []
        for raw_file in resp:
            if raw_file["life_cycle"] == "output":
                files.append(
                    PyroFile.from_dict({**raw_file, "_resource": file_resource})
                )
        return files

    def list_files(self, id: str) -> List[PyroFile]:
        """
        # Lists a job's files

        Lists all files associated with a job. The result will include all
        inputs and outputs (if any) for the provided job.

        Given a job id, returns a list containing `PyroFile` instances.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        files = pyro.jobs.list_files(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/files"
        resp = self._client.request(GET, url)
        file_resource = PyroJobFileResource(self._client)
        files: List[PyroFile] = []
        for raw_file in resp:
            files.append(PyroFile.from_dict({**raw_file, "_resource": file_resource}))

        return files

    def get_file(self, id: str, file_id: str) -> PyroFile:
        """
        # Retrieve a job's file by id

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        file_id = "f_eB5Fv"
        file = pyro.jobs.get_file(job_id, file_id)
        ```
        """
        url = f"{self._endpoint}/{id}/files"
        resp = self._client.request(GET, url)
        file_resource = PyroJobFileResource(self._client)
        for raw_file in resp:
            if raw_file["id"] == file_id:
                return PyroFile.from_dict({**raw_file, "_resource": file_resource})

        raise FileNotFoundError

    def duration(self, id: str) -> PyroJobDuration:
        """
        # Retrieve the duration of a job

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        duration = pyro.jobs.duration(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/duration"
        raw = self._client.request(GET, url)

        return PyroJobDuration.from_dict(raw)

    def cost(self, id: str) -> PyroJobCost:
        """
        # Retrieve the cost of a job

        Returns total costs and total runtime of a job.
        Additionally a job may have multiple running nodes,
        information for each node is stored as an ItemizedCostEntry within itemized costs

        ## Example
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        cost = pyro.jobs.cost(job_id)
        print(cost.total_compute_time_millis)
        print(cost.total_cents)
        >>> 560762.205
        >>> 44.39
        ```
        """
        url = f"{self._endpoint}/{id}/cost"
        raw = self._client.request(POST, url)

        return PyroJobCost.from_dict(raw)

    def get_logs(self, id: str) -> PyroJobLogs:
        """
        # Retrieve a job's logs

        ## Example
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        logs = pyro.jobs.get_logs(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/logs"
        raw = self._client.request(POST, url)

        return PyroJobLogs.from_dict(raw)

    def get_status(self, id: str) -> PyroJobStatusTypes:
        """
        # Retrieve the status of a job

        ## Example
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        status = pyro.jobs.get_status(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}"
        raw = self._client.request(GET, url)

        return PyroJobStatusTypes(raw["status"])


@dataclass
class PyroJobComputeConfig:
    cluster: Optional[str] = None
    node_group: Optional[str] = None
    max_uptime: Optional[str] = None


@dataclass
class PyroJob:
    """
    Serves as an interface to a specific PyroJob.
    Holds the properties for that job and allows operations on it.

    In general, you will likely construct or retrieve a job using
    the `PyroJobResource` class which typically returns a `PyroJob` instance.
    Then you have `update`, `add_file`, `duplicate`, `start`, etc. methods
    available to you without having to keep track of a job id.

    Technically you can construct this class directly, but this is cumbersome
    and you should probably use the `..Resource` classes to do this work for you.
    """

    id: str
    _resource: Optional[PyroJobResource] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[PyroJobTypes] = None
    compute_config: Optional[dict] = None
    config: Optional[dict] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[str] = None

    @classmethod
    def default(cls, **kwargs) -> "PyroJob":
        return PyroJob(**kwargs)

    @classmethod
    def from_dict(cls, _dict: dict) -> "PyroJob":
        """
        # Create a `PyroJob` from a python dict.
        """
        return PyroJob(
            _dict["id"],
            _dict["_resource"],
            _dict["name"],
            _dict["description"],
            _dict["type"],
            _dict["compute_config"],
            _dict["config"],
            _dict["status"],
            _dict["is_active"],
            _dict["created_at"],
        )

    def set_resource(self, resource: PyroJobResource):
        self._resource = resource

    @require_resource
    def update(self, **kwargs):
        """
        # Update a job

        Allows you to update any property of a job.
        Simply specify the property you wish to update in the kwargs
        of this function. e.g. name="name", config={..}

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_r62X.."
        job = pyro.jobs.get(job_id)
        job.update(name="My Cool Job")
        ```
        """
        assert self._resource is not None
        self._resource.update(self.id, **kwargs)

    @require_resource
    def duplicate(self):
        """
        # Duplicate a job

        When duplicating a job, only the files, config, and compute config
        are carried over. All results and artifacts are ignored.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_r62X.."
        job = pyro.jobs.get(job_id)
        duped_job = job.duplicate()
        ```
        ```
        """
        assert self._resource is not None
        return self._resource.duplicate(self.id)

    @require_resource
    def delete(self):
        """
        # Delete a job

        Deletes a job and all other data and artifacts
        associated with it. Tread carefully.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_eCcxN"
        job = pyro.jobs.get(job_id)
        job.delete()
        ```
        """
        assert self._resource is not None
        return self._resource.delete(self.id)

    @require_resource
    def add_file(self, fpath: str):
        """
        # Add a file to a job.

        ## Example:
        ```python
        my_job = pyro.jobs.create("wildest")
        my_job.add_file("~/data/wildest_test/trinity_small/fm40.tif")
        ```
        """
        assert self._resource is not None
        return self._resource.add_file(self.id, fpath)

    @require_resource
    def set_name(self, name: str):
        """
        # Set a job's name

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_r62X.."
        job = pyro.jobs.get(job_id)
        job.set_name("My Cool Job")
        ```
        """
        assert self._resource is not None
        self.name = name
        return self._resource.update(self.id, name=name)

    @require_resource
    def use_weather_scenario(self, speed: int, direction: int, mc: int):
        """
        # Configure a job to use a specific weather scenario

        Only applicable to WildEST jobs.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_r62X.."
        job = pyro.jobs.create("wildest")
        job.use_weather_scenario(40, 180, 3)
        ```
        """
        assert self._resource is not None
        if self.type != "wildest":
            raise IncompatibleJobTypeError(
                "weather scenarios are only valid for WildEST"
            )

        # Access flammap module
        modules = self.config.get("modules")
        flammap = modules.get("flammap")

        # Define calibrated params for different values of mc
        flammap_configs = {
            3: {"temp": [91], "live_woody": [70], "rel_humidity": [14], "live_herbaceous": [30]},
            5: {"temp": [84], "live_woody": [90], "rel_humidity": [28], "live_herbaceous": [45]},
            8: {"temp": [72], "live_woody": [110], "rel_humidity": [52], "live_herbaceous": [60]}
        }

        # Update flammap based on the value of mc
        if mc in flammap_configs:
            flammap.update(flammap_configs[mc])

        old_config = {} if self.config is None else self.config
        cfg = {
            **old_config,
            "wind_speeds": [speed],
            "wind_directions": [direction],
            "moisture_contents": [mc],
            "modules": {**modules, "flammap": flammap},
        }
        self._resource.set_config(self.id, cfg)

    @require_resource
    def set_config(self, config: dict):
        """
        # Set a job's config

        Allows you to set the config of a job.
        Keep in mind, this function does not perform any
        config validation. And acts as a setter so whatever you provide
        will indeed become the job's config. Tread carefully.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_r62X.."
        job = pyro.jobs.get(job_id)
        config = {"num_simulations": 10000, "tile_width": 20000, ...}
        updated_job = job.set_config(config)
        ```
        """
        assert self._resource is not None
        return self._resource.set_config(self.id, config)

    @require_resource
    def list_files(self):
        """
        # List all files associated with a job

        ## Example
        ```python
        pyro = PyroDash(..)
        job_id = "j_dsqVD"
        job = pyro.jobs.get(job_id)
        files = job.list_files()
        ```
        """
        assert self._resource is not None
        return self._resource.list_files(self.id)

    @require_resource
    def preview(self):
        """
        # Preview a job

        Allows you to "preview" the config, files, and validation
        checks for that job.

        It is recommended that you preview a job before you start it.
        Just to mitigate any potential issues with the job that the system automatically detects.
        If you're missing files, have an illogical config, etc.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        preview = pyro.jobs.preview(job_id)
        ```
        """
        assert self._resource is not None
        return self._resource.preview(self.id)

    @require_resource
    def start(self):
        """
        # Start a job

        Starts a job and runs it on the pyro compute platform.

        All compute scaling-up/down is taken care of for you. After a job is
        started, you can check out the logs, monitor the status and duration
        or view it in the dashboard UI!

        The job will run until it enters a "completed" state, in other words,
        until it fails, exits successfully, or is cancelled.

        In order to start a job, the job must have status: "not submitted".
        Otherwise, you will receive an error.

        ## Example

        ```python
        pyro = PyroDash(...)
        job = pyro.jobs.create("fsim")
        job.add_file(...)
        print(job.get_status())
        >>> "Not Submitted"
        job.start()
        print(job.get_status())
        >>> "PENDING"
        ```
        """
        assert self._resource is not None
        return self._resource.start(self.id)

    @require_resource
    def cancel(self):
        """
        # Cancel a job

        Stops a job that is running or scheduled to run.

        To run again after cancelling a job, status must be set back to "not submitted".
        This is typically done by using the job.retry() function.

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVDw"
        job = pyro.jobs.get(job_id)
        job.cancel()
        ```
        """
        assert self._resource is not None
        return self._resource.cancel(self.id)

    @require_resource
    def list_inputs(self):
        """
        # List a job's input files

        ## Example
        ```python
        pyro = PyroDash(..)
        job_id = "j_dsqVD"
        job = pyro.jobs.get(job_id)
        files = job.list_inputs()
        ```
        """
        assert self._resource is not None
        return self._resource.list_inputs(self.id)

    @require_resource
    def list_outputs(self):
        """
        # List a job's output files

        ## Example
        ```python
        pyro = PyroDash(..)
        job_id = "j_dsqVD"
        job = pyro.jobs.get(job_id)
        files = job.list_outputs()
        ```
        """
        assert self._resource is not None
        return self._resource.list_outputs(self.id)

    @require_resource
    def duration(self):
        """
        # Retrieve the duration of a job

        ## Example:
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        job = pyro.jobs.get(job_id)
        duration = job.duration()
        ```
        """
        assert self._resource is not None
        return self._resource.duration(self.id)

    @require_resource
    def cost(self):
        """
        # Retrieve the cost of a job

        Returns total costs and total runtime of a job.
        Additionally a job may have multiple running nodes,
        information for each node is stored as an ItemizedCostEntry within itemized costs

        ## Example
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        job = pyro.jobs.get(job_id)
        cost = job.cost()
        print(cost.total_compute_time_millis)
        print(cost.total_cents)
        >>> 560762.205
        >>> 44.39
        ```
        """
        assert self._resource is not None
        return self._resource.cost(self.id)

    @require_resource
    def logs(self):
        """
        # Retrieve a job's logs

        ## Example
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        job = pyro.jobs.get(job_id)
        logs = job.logs()
        ```
        """
        assert self._resource is not None
        return self._resource.get_logs(self.id)

    @require_resource
    def get_status(self):
        """
        # Retrieve the up-to-date status of a job

        Since the status potentially changes server side, such as when the job
        is running and enters a completed state, you won't be notified of such
        changes.

        Calling this method gives you a clean way to retrieve
        the status of the job.

        ## Example
        ```python
        pyro = PyroDash(...)
        job_id = "j_dsqVD"
        job = pyro.jobs.get(job_id)
        status = job.get_status()
        ```
        """
        assert self._resource is not None
        return self._resource.get_status(self.id)


@dataclass
class PyroJobList:
    page: int
    limit: int
    total_pages: int
    total_records: int
    data: List[PyroJob]
