from typing import Union, Annotated, Optional,List
import typing
import uuid
import strawberry as strawberryA
import datetime
from .BaseGQLModel import BaseGQLModel
from utils.Dataloaders import getLoadersFromInfo
EventGQLModel = Annotated["EventGQLModel",strawberryA.lazy(".EventGQLModel")]
# def getLoaders(info):
#     return info.context['all']

@strawberryA.federation.type(keys=["id"], description="""Entity representing content""")
class ContentGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        loader = getLoadersFromInfo(info).contents
        return loader
    # async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
    #     async with withInfo(info) as session:
    #         result = await resolveContentModelById(session, id)
    #         result._type_definition = cls._type_definition
    #         return result

    @strawberryA.field(description="""Primary key of content""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="""Brief description""")
    def brief_desc(self) -> str:
        return self.brief_des

    @strawberryA.field(description="""Full description""")
    def detailed_desc(self) -> Optional[str]:
        return self.detailed_des

    @strawberryA.field(description="""event id""")
    async def event(self, info: strawberryA.types.Info) -> Union["EventGQLModel", None]:
        from .EventGQLModel import EventGQLModel
        if self.event_id is None:
            result = None
        else:
            result = EventGQLModel(id=self.event_id)
        return result


@strawberryA.input
class ContentInsertGQLModel:
    brief_des: Optional[str] = ""
    detailed_des: Optional[str] = ""
    event_id: Optional[uuid.UUID] = None
    id: typing.Optional[uuid.UUID] = strawberryA.field(description="primary key (UUID), could be client generated", default=None)


@strawberryA.input
class ContentUpdateGQLModel:
    lastchange: datetime.datetime = strawberryA.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of operation")

    brief_des: Optional[str] = None
    detailed_des: Optional[str] = None
    event_id: Optional[uuid.UUID] = None

@strawberryA.type
class ContentResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="primary key of CU operation object")
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def task(self, info: strawberryA.types.Info) -> Union[ContentGQLModel, None]:
        result = await ContentGQLModel.resolve_reference(info, self.id)
        return result

#####################################################################
#
# Special fields for query
#
#####################################################################

@strawberryA.field(description="""Finds content by their id""")
async def content_by_id(
    self, info: strawberryA.types.Info, id: uuid.UUID
) -> Union[ContentGQLModel, None]:
    result = await ContentGQLModel.resolve_reference(info, id)
    return result

@strawberryA.field(description="""Finds content by their page""")
async def content_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
) -> List[ContentGQLModel]:
    loader = getLoadersFromInfo(info).contents
    result = await loader.page(skip=skip, limit=limit)
    return result

#####################################################################
#
# Mutation section
#
#####################################################################

@strawberryA.mutation(description="Adds a task.")
async def content_insert(self, info: strawberryA.types.Info, content: ContentInsertGQLModel) -> ContentResultGQLModel:
    loader = getLoadersFromInfo(info).contents
    row = await loader.insert(content)
    result = ContentResultGQLModel(id=row.id, msg="ok")
    result.msg = "ok"
    result.id = row.id
    return result


@strawberryA.mutation(description="Update the content.")
async def content_update(self, info: strawberryA.types.Info, content: ContentUpdateGQLModel) -> ContentResultGQLModel:
    loader = getLoadersFromInfo(info).contents
    row = await loader.update(content)
    result = ContentResultGQLModel(id=row.id, msg="ok")

    if row is None:
        result.msg = "fail"

    return result

