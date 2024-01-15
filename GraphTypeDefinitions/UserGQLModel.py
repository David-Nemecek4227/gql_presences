import typing
import uuid
from typing import Annotated
import strawberry as strawberryA
from GraphTypeDefinitions.GraphResolvers import (
    resolveTasksForUser,
)
from .withInfo import withInfo
TaskGQLModel = Annotated["TaskGQLModel",strawberryA.lazy(".TaskGQLModel")]


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: uuid.UUID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return UserGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz

    @strawberryA.field(description="""task id""")
    async def tasks(self, info: strawberryA.types.Info) -> typing.List["TaskGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveTasksForUser(session, self.id)
            return result