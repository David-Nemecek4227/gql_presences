import strawberry
import uuid
import datetime
import typing
import logging
from .BaseGQLModel import IDType
from uoishelpers.resolvers import (
    create1NGetter,
    createEntityByIdGetter,
    createEntityGetter,
)

from DBDefinitions import (
    TaskModel,
    ContentModel,
)

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

# user

#resolveUserModelPage = createEntityGetter(UserModel)
#resolveUserModelById = createEntityByIdGetter(UserModel)

# task on event

resolveTasksForUser = create1NGetter(TaskModel, foreignKeyName="user_id")

# tasks

resolveTaskModelByPage = createEntityGetter(TaskModel)
resolveTaskModelById = createEntityByIdGetter(TaskModel)
resolveTasksForEvent = create1NGetter(TaskModel, foreignKeyName="event_id")
# content

resolveContentModelByPage = createEntityGetter(ContentModel)
resolveContentModelById = createEntityByIdGetter(ContentModel)
resolveContentForEvent = create1NGetter(ContentModel, foreignKeyName="event_id")


def createRootResolver_by_id(scalarType: None, description="Retrieves item by its id"):
    assert scalarType is not None

    @strawberry.field(description=description)
    async def by_id(
            self, info: strawberry.types.Info, id: IDType
    ) -> typing.Optional[scalarType]:
        result = await scalarType.resolve_reference(info=info, id=id)
        return result

    return by_id


def createRootResolver_by_page(
        scalarType: None,
        whereFilterType: None,
        loaderLambda=lambda info: None,
        description="Retrieves items paged",
        skip: int = 0,
        limit: int = 10,
        order_by: typing.Optional[str] = None,
        desc: typing.Optional[bool] = None):
    assert scalarType is not None
    assert whereFilterType is not None

    @strawberry.field(description=description)
    async def paged(
            self, info: strawberry.types.Info,
            skip: int = skip, limit: int = limit, where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        loader = loaderLambda(info)
        assert loader is not None
        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf, orderby=order_by, desc=desc)
        return result

    return paged

###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

# resolveItemById = createEntityByIdGetter(EntityModel)
# resolveItemPage = createEntityGetter(EntityModel)

# ...
