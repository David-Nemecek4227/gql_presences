from typing import List, Annotated
import typing
import strawberry as strawberryA
from gql_presences.GraphTypeDefinitions.GraphResolvers import resolveContentForEvent
from .withInfo import withInfo

TaskGQLModel = Annotated["TaskGQLModel",strawberryA.lazy(".TaskGQLModel")]
ContentGQLModel = Annotated["ContentGQLModel",strawberryA.lazy(".ContentGQLModel")]


# def getLoaders(info):
#     return info.context['all']


@strawberryA.federation.type(extend=True, keys=["id"])
class EventGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return EventGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz

    # rozšiřujeme jen o atributy (1,1)
    @strawberryA.field(description="""content id""")
    async def content(
        self, info: strawberryA.types.Info
    ) -> typing.Union["ContentGQLModel", None]:
        async with withInfo(info) as session:
            result = await resolveContentForEvent(
                session, self.id
            )  # z tabulky obsahů hledáme event_id = event_id v Content
            return next(result, None)

    @strawberryA.field(description="""tasks assiciated with this event""")
    async def tasks(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> List[TaskGQLModel]:
        loader = getLoaders(info).tasks
        result = await loader.filter_by(event_id=self.id)
        return result