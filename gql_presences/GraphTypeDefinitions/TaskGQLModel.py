from typing import Union, Annotated, Optional
import strawberry as strawberryA
import datetime
from gql_presences.GraphResolvers import resolveTaskModelById
from .withInfo import withInfo

EventGQLModel = Annotated["EventGQLModel", strawberryA.lazy(".EventGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberryA.lazy(".UserGQLModel")]


@strawberryA.federation.type(keys=["id"], description="""Entity representing tasks""")
class TaskGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveTaskModelById(session, id)
            result._type_definition = cls._type_definition
            return result

    @strawberryA.field(description="""Primary key of task""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Name of tasks""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Brief description""")
    def brief_des(self) -> Union[str, None]:
        return self.brief_des

    @strawberryA.field(description="""Full description""")
    def detailed_des(self) -> Union[str, None]:
        return self.detailed_des

    @strawberryA.field(description=""" Reference""")
    def reference(self) -> Union[str, None]:
        return self.reference

    @strawberryA.field(description="""Date of entry""")
    def date_of_entry(self) -> datetime.date:
        return self.date_of_entry

    @strawberryA.field(description="""Date of submission""")
    def date_of_submission(self) -> Union[datetime.date, None]:
        return self.date_of_submission

    @strawberryA.field(description="""Date of fullfilment""")
    def date_of_fulfillment(self) -> Union[datetime.date, None]:
        return self.date_of_fulfillment

    @strawberryA.field(description="""event id""")
    async def event(self, info: strawberryA.types.Info) -> Union["EventGQLModel", None]:
        from .EventGQLModel import EventGQLModel
        if self.event_id is None:
            result = None
        else:
            result = await EventGQLModel.resolve_reference(id=self.event_id)
        return result

    @strawberryA.field(description="""event id""")
    async def user(self, info: strawberryA.types.Info) -> Union["UserGQLModel", None]:
        from .UserGQLModel import UserGQLModel
        if self.user_id is None:
            result = None
        else:
            result = await UserGQLModel(id=self.user_id)
        return result


@strawberryA.input
class TaskInsertGQLModel:
    name: str
    user_id: strawberryA.ID

    brief_des: Optional[str] = ""
    detailed_des: Optional[str] = ""
    reference: Optional[str] = ""
    date_of_entry: Optional[datetime.datetime] = datetime.datetime.now()
    date_of_submission: Optional[datetime.datetime] = datetime.datetime.now()
    date_of_fulfillment: Optional[datetime.datetime] = datetime.datetime.now() + datetime.timedelta(days=7)

    event_id: Optional[strawberryA.ID] = None
    id: Optional[strawberryA.ID] = None


@strawberryA.type
class TaskResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def task(self, info: strawberryA.types.Info) -> Union[TaskGQLModel, None]:
        result = await TaskGQLModel.resolve_reference(info, self.id)
        return result


@strawberryA.input
class TaskUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str]

    brief_des: Optional[str] = None
    detailed_des: Optional[str] = None
    reference: Optional[str] = None
    date_of_entry: Optional[datetime.datetime] = None
    date_of_submission: Optional[datetime.datetime] = None
    date_of_fulfillment: Optional[datetime.datetime] = None
    event_id: Optional[strawberryA.ID] = None