import typing as t

from pydantic import BaseModel


# Job

class TaleezJob(BaseModel):
    id: int
    token: str
    dateCreation: int
    dateFirstPublish: int
    dateLastPublish: int
    label: str
    profile: str #Enum TODO
    currentStatus: str #Enum TODO
    contract: str #Enum TODO
    contractLength: int
    fullTime: bool
    workHours: int
    qualification: str #Enum TODO
    remote: bool
    country: str #Enum TODO
    city: str
    postalCode: str
    lat: str
    lng: str
    recruiterId: int
    who: str
    logo: str
    banner: str
    companyLabel: str
    tags: t.List[str]
    url: str
    urlApplying: str
    jobDescription: str
    profileDescription: str
    companyDescription: str
    public: bool
