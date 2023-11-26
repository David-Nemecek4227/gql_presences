from typing import Union, Annotated, Optional
import strawberry as strawberryA
from .withInfo import withInfo

from gql_presences.GraphResolvers import (
    resolveContentModelById,
)
EventGQLModel = Annotated["EventGQLModel",strawberryA.lazy(".EventGQLModel")]


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
