from typing import List, Union, Annotated
import strawberry as strawberryA

TaskGQLModel = Annotated["TaskGQLModel",strawberryA.lazy(".TaskGQLModel")]
ContentGQLModel = Annotated["ContentGQLModel",strawberryA.lazy(".ContentGQLModel")]


def getLoaders(info):
    return info.context['all']


@strawberryA.type(description="""Type for query root""")
class Query:
    # nedotazovat se na TaskOnEventModel
    @strawberryA.field(description="""Finds a workflow by their id""")
    async def say_hello_presences(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result

    @strawberryA.field(description="""Finds tasks by their id""")
    async def task_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[TaskGQLModel, None]:
        result = await TaskGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds tasks by their page""")
    async def task_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[TaskGQLModel]:
        loader = getLoaders(info).tasks
        result = await loader.page(skip=skip, limit=limit)
        return result

    @strawberryA.field(description="""Finds presence by their id""")
    async def tasks_by_event(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> List[TaskGQLModel]:
        loader = getLoaders(info).tasks
        result = await loader.filter_by(event_id=id)
        return result

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