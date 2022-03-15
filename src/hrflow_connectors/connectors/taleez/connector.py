import typing as t

from datetime import datetime

from hrflow_connectors.connectors.hrflow.warehouse import (
    HrFlowJobWarehouse,
)
from hrflow_connectors.connectors.taleez.warehouse import (
    TaleezJobWarehouse,
)
from hrflow_connectors.core import (
    BaseActionParameters,
    Connector,
    ConnectorAction,
    WorkflowType,
)

def get_job_location(taleez_job: t.Union[t.Dict, None]) -> t.Dict:
    if taleez_job is None:
        return dict(lat=None, lng=None, text="")

    lat = taleez_job.get("lat")
    lat = float(lat) if lat is not None else lat

    lng = taleez_job.get("lng")
    lng = float(lng) if lng is not None else lng

    concatenate = []
    for field in ["postalCode", "city", "country"]:
        if taleez_job.get(field):
            concatenate.append(taleez_job.get(field))

    return dict(lat=lat, lng=lng, text=" ".join(concatenate))


def get_sections(taleez_job: t.Dict) -> t.List[t.Dict]:
    sections = []
    for section_name in [
        "jobDescription",
        "profileDescription",
        "companyDescription"
    ]:
        section = taleez_job.get(section_name)
        if section is not None:
            sections.append(
                dict(
                    name="taleez-sections-{}".format(section_name), 
                    title=section_name, 
                    description=section,
                )
            )
    return sections


def get_tags(taleez_job: t.Dict) -> t.List[t.Dict]:
    taleez_tags = taleez_job.get('tags')
    t = lambda name, value: dict(name=name, value=value)

    custom_fields = [
        "contract",
        "profile",
        "contractLength",
        "fullTime",
        "workHours",
        "qualification",
        "remote",
        "recruiterId",
        "companyLabel",
        "urlApplying",
        "currentStatus",
    ]

    tags = [t("{}_{}".format("taleez", field), taleez_job.get(field)) for field in custom_fields]
    tags += [t("{}_{}".format("taleez", "tag"), tag) for tag in taleez_tags]
    return tags


def format_job(taleez_job: t.Dict) -> t.Dict:
    job = dict(
        name=taleez_job.get("label", "Undefined"), 
        reference=str(taleez_job.get("id")),
        created_at=datetime.fromtimestamp(taleez_job["dateCreation"]).isoformat(),
        updated_at=datetime.fromtimestamp(taleez_job["dateLastPublish"]).isoformat(),
        location=get_job_location(taleez_job),
        url=taleez_job.get("url"),
        summary=None,
        sections=get_sections(taleez_job),
        tags=get_tags(taleez_job),
    )
    return job


DESCRIPTION = (
    "Taleez est une solution globale de gestion des candidatures et de diffusion d'offres d'emploi."
    "Pilotez intégralement vos processus de recrutement et intégrez vos équipes dans les décisions."
)
Taleez = Connector(
    name="Taleez",
    description=DESCRIPTION,
    url="https://www.taleez.com/",
    actions=[
        ConnectorAction(
            name="pull_jobs",
            type=WorkflowType.pull,
            description=(
                "Retrieves all jobs via the ***Taleez*** API and send them"
                " to a ***Hrflow.ai Board***."
            ),
            parameters=BaseActionParameters.with_default_format(
                "PullJobsActionParameters", format=format_job
            ),
            origin=TaleezJobWarehouse,
            target=HrFlowJobWarehouse,
        )
    ],
)
