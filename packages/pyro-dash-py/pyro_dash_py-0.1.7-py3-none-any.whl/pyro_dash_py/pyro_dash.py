from .project import PyroProjectResource
from .client import PyroApiClient
from .job import PyroJobResource


class PyroDash:
    """
    Primary entrypoint to pyro-dash resources.
    """

    def __init__(self, host: str, email: str, apikey: str):
        self._client = PyroApiClient(host, email, apikey)
        self.jobs = PyroJobResource(self._client)
        self.projects = PyroProjectResource(self._client)
