from typing import Union, Annotated, Optional, List
import typing
import uuid
import strawberry as strawberryA
import datetime
from .BaseGQLModel import BaseGQLModel

from utils.Dataloaders import getLoadersFromInfo

from .externals import EventGQLModel, UserGQLModel
# EventGQLModel = Annotated["EventGQLModel", strawberryA.lazy(".EventGQLModel")]
# UserGQLModel = Annotated["UserGQLModel", strawberryA.lazy(".UserGQLModel")]
# def getLoaders(info):
#     return info.context['all']
from .GraphPermissions import OnlyForAuthentized

@strawberryA.federation.type(keys=["id"], description="""Entity representing tasks""")
class TaskGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).tasks
    # async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
    #     async with withInfo(info) as session:
    #         result = await resolveTaskModelById(session, id)
    #         result._type_definition = cls._type_definition
    #         return result

    @strawberryA.field(description="""Primary key of task""",
        permission_classes=[OnlyForAuthentized()])
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="""Timestamp""",
        permission_classes=[OnlyForAuthentized()])
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Name of tasks""",
        permission_classes=[OnlyForAuthentized()])
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Brief description""",
        permission_classes=[OnlyForAuthentized()])
    def brief_des(self) -> Union[str, None]:
        return self.brief_des

    @strawberryA.field(description="""Full description""",
        permission_classes=[OnlyForAuthentized()])
    def detailed_des(self) -> Union[str, None]:
        return self.detailed_des

    @strawberryA.field(description=""" Reference""",
        permission_classes=[OnlyForAuthentized()])
    def reference(self) -> Union[str, None]:
        return self.reference

    @strawberryA.field(description="""Date of entry""",
        permission_classes=[OnlyForAuthentized()])
    def date_of_entry(self) -> datetime.date:
        return self.date_of_entry

    @strawberryA.field(description="""Date of submission""",
        permission_classes=[OnlyForAuthentized()])
    def date_of_submission(self) -> Union[datetime.date, None]:
        return self.date_of_submission

    @strawberryA.field(description="""Date of fullfilment""",
        permission_classes=[OnlyForAuthentized()])
    def date_of_fulfillment(self) -> Union[datetime.date, None]:
        return self.date_of_fulfillment

    @strawberryA.field(description="""event id""",
        permission_classes=[OnlyForAuthentized()])
    async def event(self, info: strawberryA.types.Info) -> Union["EventGQLModel", None]:
        from .externals import EventGQLModel
        # if self.event_id is None:
        #     result = None
        # else:
        #     result = await EventGQLModel.resolve_reference(id=self.event_id)
        result = await EventGQLModel.resolve_reference(id=self.event_id)
        return result

    @strawberryA.field(description="""event id""",
        permission_classes=[OnlyForAuthentized()])
    async def user(self, info: strawberryA.types.Info) -> Union["UserGQLModel", None]:
        from .externals import UserGQLModel
        # if self.user_id is None:
        #     result = None
        # else:
        #     result = await UserGQLModel(id=self.user_id)
        result = await UserGQLModel.resolve_reference(id=self.user_id)
        return result


@strawberryA.input
class TaskInsertGQLModel:
    name: str
    user_id: uuid.UUID
    brief_des: Optional[str] = ""
    detailed_des: Optional[str] = ""
    reference: Optional[str] = ""
    date_of_entry: Optional[datetime.datetime] = datetime.datetime.now()
    date_of_submission: Optional[datetime.datetime] = datetime.datetime.now()
    date_of_fulfillment: Optional[datetime.datetime] = datetime.datetime.now() + datetime.timedelta(days=7)
    event_id: Optional[uuid.UUID] = None
    id: typing.Optional[uuid.UUID] = strawberryA.field(description="primary key (UUID), could be client generated", default=None)


@strawberryA.type
class TaskResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key of CU operation object")
    msg: str = None

    @strawberryA.field(description="""Result of user operation""",
        permission_classes=[OnlyForAuthentized()])
    async def task(self, info: strawberryA.types.Info) -> Union[TaskGQLModel, None]:
        result = await TaskGQLModel.resolve_reference(info, self.id)
        return result


@strawberryA.input
class TaskUpdateGQLModel:
    lastchange: datetime.datetime = strawberryA.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")
    name: Optional[str]=None
    brief_des: Optional[str] = None
    detailed_des: Optional[str] = None
    reference: Optional[str] = None
    date_of_entry: Optional[datetime.datetime] = None
    date_of_submission: Optional[datetime.datetime] = None
    date_of_fulfillment: Optional[datetime.datetime] = None
    event_id: Optional[uuid.UUID] = None

#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberryA.field(description="""Finds tasks by their id""",
        permission_classes=[OnlyForAuthentized()])
async def task_by_id(
    self, info: strawberryA.types.Info, id: uuid.UUID
) -> Union[TaskGQLModel, None]:
    result = await TaskGQLModel.resolve_reference(info, id)
    return result

@strawberryA.field(description="""Finds tasks by their page""",
        permission_classes=[OnlyForAuthentized()])
async def task_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
) -> List[TaskGQLModel]:
    loader = getLoadersFromInfo(info).tasks
    result = await loader.page(skip=skip, limit=limit)
    return result

@strawberryA.field(description="""Finds presence by their id""",
        permission_classes=[OnlyForAuthentized()])
async def tasks_by_event(
    self, info: strawberryA.types.Info, id: uuid.UUID
) -> List[TaskGQLModel]:
    loader = getLoadersFromInfo(info).tasks
    result = await loader.filter_by(event_id=id)
    return result

#####################################################################
#
# Mutation section
#
#####################################################################

@strawberryA.mutation(description="Adds a task.",
        permission_classes=[OnlyForAuthentized()])
async def task_insert(self, info: strawberryA.types.Info, task: TaskInsertGQLModel) -> TaskResultGQLModel:
    loader = getLoadersFromInfo(info).tasks
    row = await loader.insert(task)
    result = TaskResultGQLModel(id=row.id, msg="ok")
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the task.",
        permission_classes=[OnlyForAuthentized()])
async def task_update(self, info: strawberryA.types.Info, task: TaskUpdateGQLModel) -> TaskResultGQLModel:
    loader = getLoadersFromInfo(info).tasks
    row = await loader.update(task)
    result = TaskResultGQLModel(id=row.id, msg="ok")
    # result.msg = "ok"
    result.id = row.id
    result.msg = "fail" if row is None else "ok"
    # if row is None:
    #     result.msg = "fail"

    return result

@strawberryA.mutation(description="Delete the task.",
        permission_classes=[OnlyForAuthentized()])
async def task_delete(self, info: strawberryA.types.Info, id: uuid.UUID) -> TaskResultGQLModel:
    loader = getLoadersFromInfo(info).tasks
    row = await loader.delete(id=id)
    result = TaskResultGQLModel(id=id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result