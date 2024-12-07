from dataclasses import dataclass
from typing import Optional, Union, List
from .client import PyroApiClient
import json
from pyro_dash_py.job import PyroJob, PyroJobResource
from .core import (
    GET,
    POST,
    DEL,
    require_resource,
)


@dataclass
class ProjectFilter:
    field: str
    value: Union[str, float, int]
    op: Optional[str] = "ILIKE"


class PyroProjectResource:
    """
    An interface for projects in the Pyro ecosystem.

    Provides an organization mechanism for Pyro jobs and job groups.
    """

    def __init__(self, client: PyroApiClient):
        self.client = client
        self._endpoint = "projects"

    def create(self, name: Optional[str] = None):
        """
        # Create a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.create("my pyro project")
        print(project.name)
        print(project.id)
        """
        data = {"name": name}
        raw = self.client.request("POST", self._endpoint, data)
        _dict = {**raw, "_resource": self}
        return PyroProject.from_dict(_dict)

    def get(self, id: str):
        """
        # Retrieve a project by ID

        ## Example
        ```python
        pyro = PyroDash(...)
        id = "p_3QZ12NDKxyokJiwLbNBM7G"
        project = pyro.pyrojects.get(id)
        ```
        """
        url = f"{self._endpoint}/{id}"
        raw = self.client.request("GET", url)
        _dict = {**raw, "_resource": self}
        return PyroProject.from_dict(_dict)

    def filter(self, filters: List[ProjectFilter] = [], page=1, num_per_page=10):
        """
        # Retrieve a list of projects

        The projects returned are filtered and paginated in accordance
        with the params you provide. If no filters are provided,
        then all of the projects are retrieved.

        ## Example
        ```python
        pyro = PyroDash(...)

        # Get all of my projects (returns maximum of 20)
        projects = pyro.projects.filter(num_per_page=20)

        # Get all projects that have wildest in the name (not case sensitive)
        filters = [ProjectFilter("name", "wildest")]
        wildest_projects = pyro.projects.filter(filters)
        ```
        """
        params = {
            "page": page,
            "limit": num_per_page,
            "filters": json.dumps([filter.__dict__ for filter in filters]),
        }
        raw = self.client.request("GET", self._endpoint, params)
        projects: List[PyroProject] = []
        for data in raw["data"]:
            _dict = {**data, "_resource": self}
            project = PyroProject.from_dict(_dict)
            projects.append(project)
        return projects

    def find_by_name(self, name: str):
        """
        # Find a project by name

        This function only expects exactly one match. If more or less
        are found, a `ValueError` will be raised.

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.find_by_name("my project")
        print(project.name)
        >>> "my_project"
        project.list_jobs() # etc
        ```
        """
        projects = self.filter([ProjectFilter("name", name)])
        if len(projects) == 0:
            raise ValueError(f"Cannot find project with name: {name}")
        if len(projects) > 1:
            raise ValueError(f"Name {name} is ambiguous, too many results returned")

        return projects[0]

    def add_job(self, id: str, job_id: str) -> PyroJob:
        """
        # Add a job to a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project_id = "p_2VF7h.."
        job_id = "j_r62X.."
        job = pyro.projects.add_job(project_id, job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/add_job"
        raw = self.client.request(POST, url, {"job_id": job_id})
        _dict = {**raw, "_resource": PyroJobResource(self.client)}
        return PyroJob.from_dict(_dict)

    def duplicate_job(self, id: str, job_id: str) -> PyroJob:
        """
        # Duplicate a job in a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project_id = "p_2VF7h.."
        job_id = "j_r62X.."
        duplicate_job = pyro.projects.duplicate_job(project_id, job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/duplicate_job"
        raw = self.client.request(POST, url, {"job_id": job_id})
        _dict = {**raw, "_resource": PyroJobResource(self.client)}
        return PyroJob.from_dict(_dict)

    def delete(self, id: str):
        """
        # Delete a project

        Deleting a project will also delete any jobs and data
        associated with it. Tread carefully.

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.find_by_name("my cringe project")
        pyro.projects.delete(project.id)
        ```
        """
        url = f"{self._endpoint}/{id}"
        raw = self.client.request(DEL, url)
        _dict = {**raw, "_resource": self}
        return PyroProject.from_dict(_dict)

    def list_jobs(self, id: str) -> list[PyroJob]:
        """
        # Retrieve a list of jobs in a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project_id = "p_2VF7h.."
        jobs = pyro.projects.get_jobs(project_id)
        print(jobs)
        ```
        """
        url = f"{self._endpoint}/{id}/jobs"
        raw = self.client.request(GET, url)
        jobs = []
        for lite_job_data in raw["data"]:
            job_id = lite_job_data["id"]
            url = "jobs/" + job_id
            raw = self.client.request(GET, url)
            _dict = {**raw, "_resource": PyroJobResource(self.client)}
            jobs.append(PyroJob.from_dict(_dict))
        return jobs


@dataclass
class PyroProject:
    id: str
    name: str
    created_at: str
    is_active: str
    _resource: Optional[PyroProjectResource]

    @classmethod
    def from_dict(cls, d: dict) -> "PyroProject":
        return PyroProject(
            d["id"],
            d["name"],
            d["created_at"],
            d["is_active"],
            d["_resource"],
        )

    @require_resource
    def add_job(self, job_id: str):
        """
        # Add a job to a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.create('test project')
        job_id = "j_r62X.."
        job = project.add_job(job_id)
        ```
        """
        assert self._resource is not None
        return self._resource.add_job(self.id, job_id)

    @require_resource
    def delete(self):
        """
        # Delete a project

        Deleting a project will also delete any jobs and data
        associated with it. Tread carefully.

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.find_by_name("my cringe project")
        project.delete()
        ```
        """
        assert self._resource is not None
        return self._resource.delete(self.id)

    @require_resource
    def duplicate_job(self, job_id: str):
        """
        # Duplicate a job in a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.find_by_name("my project")
        job_id = "j_r62X.."
        duped_job = project.duplicate_job(job_id)
        ```
        """
        assert self._resource is not None
        return self._resource.duplicate_job(self.id, job_id)

    @require_resource
    def list_jobs(self):
        """
        # Retrieve all jobs in a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.filter("my project")
        jobs = project.get_jobs()
        ```
        """
        assert self._resource is not None
        return self._resource.list_jobs(self.id)
