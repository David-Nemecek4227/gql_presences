from typing import Union, Annotated, Optional,List
import strawberry as strawberryA
from .withInfo import withInfo
import datetime
from gql_presences.GraphResolvers import (
    resolveContentModelById,
)
EventGQLModel = Annotated["EventGQLModel",strawberryA.lazy(".EventGQLModel")]
def getLoaders(info):
    return info.context['all']

@strawberryA.federation.type(keys=["id"], description="""Entity representing content""")
class ContentGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveContentModelById(session, id)
            result._type_definition = cls._type_definition
            return result

    @strawberryA.field(description="""Primary key of content""")
    def id(self) -> strawberryA.ID:
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
    event_id: Optional[strawberryA.ID] = None
    id: Optional[strawberryA.ID] = None


@strawberryA.input
class ContentUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    brief_des: Optional[str] = None
    detailed_des: Optional[str] = None
    event_id: Optional[strawberryA.ID] = None

@strawberryA.type
class ContentResultGQLModel:
    id: strawberryA.ID = None
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
    self, info: strawberryA.types.Info, id: strawberryA.ID
) -> Union[ContentGQLModel, None]:
    result = await ContentGQLModel.resolve_reference(info, id)
    return result

@strawberryA.field(description="""Finds content by their page""")
async def content_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
) -> List[ContentGQLModel]:
    loader = getLoaders(info).contents
    result = await loader.page(skip=skip, limit=limit)
    return result

#####################################################################
#
# Mutation section
#
#####################################################################

@strawberryA.mutation(description="Adds a task.")
async def content_insert(self, info: strawberryA.types.Info, content: ContentInsertGQLModel) -> ContentResultGQLModel:
    loader = getLoaders(info).contents
    row = await loader.insert(content)
    result = ContentResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result


@strawberryA.mutation(description="Update the content.")
async def content_update(self, info: strawberryA.types.Info, content: ContentUpdateGQLModel) -> ContentResultGQLModel:
    loader = getLoaders(info).contents
    row = await loader.update(content)
    result = ContentResultGQLModel()
    result.msg = "ok"
    result.id = content.id
    if row is None:
        result.msg = "fail"

    return result

