import enum
import typing as t
from logging import LoggerAdapter

import requests
from pydantic import BaseModel, Field

from hrflow_connectors.connectors.taleez.schemas import (
    TaleezJob,
)
from hrflow_connectors.core import (
    ActionEndpoints,
    Warehouse,
    WarehouseReadAction,
)

TALEEZ_JOBS_ENDPOINT = "https://api.taleez.com/0/jobs"
TALEEZ_JOBS_ENDPOINT_LIMIT = 100


GET_ALL_JOBS_ENDPOINT = ActionEndpoints(
    name="Get all jobs",
    description=(
        "Endpoint to retrieve all jobs."
        " and get the list of all jobs with their ids, the request method"
        " is `GET`"
    ),
    url=(
        "https://api.taleez.com/0/jobs"
    ),
)


class JobStatus(str, enum.Enum):
    published = "PUBLISHED"


class PullJobsParameters(BaseModel):
    x_taleez_api_secret: str = Field(
        ..., description="X-taleez-api-secret used to access Taleez API", repr=False
    )
    with_details: bool = Field(..., description="xxx")
    job_status: JobStatus = Field(None, description="Posting status of a job. One of {}".format(
        [e.value for e in JobStatus]
    ))


def read(adapter: LoggerAdapter, parameters: PullJobsParameters) -> t.Iterable[t.Dict]:
    params = dict(
        withDetails=parameters.with_details,
        status=parameters.job_status
    )

    response = requests.get(
        TALEEZ_JOBS_ENDPOINT,
        headers={ "X-taleez-api-secret": parameters.x_taleez_api_secret },
        params=params
    )

    if response.status_code // 100 != 2:
        adapter.error(
            "Failed to pull jobs from Taleez params={}"
            " status_code={} response={}".format(
                params, response.status_code, response.text
            )
        )
        raise Exception("Failed to pull jobs from Taleez")

    response = response.json()
    jobs = response["list"]

    for job in jobs:
        yield job

TaleezJobWarehouse = Warehouse(
    name="Taleez Jobs",
    data_schema=TaleezJob,
    read=WarehouseReadAction(
        parameters=PullJobsParameters,
        function=read,
        endpoints=[GET_ALL_JOBS_ENDPOINT],
    ),
)