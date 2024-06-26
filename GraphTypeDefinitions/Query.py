from typing import List, Union, Annotated
import strawberry as strawberryA
import uuid
TaskGQLModel = Annotated["TaskGQLModel",strawberryA.lazy(".TaskGQLModel")]
ContentGQLModel = Annotated["ContentGQLModel",strawberryA.lazy(".ContentGQLModel")]


def getLoaders(info):
    return info.context['all']


@strawberryA.type(description="""Type for query root""")
class Query:
    # nedotazovat se na TaskOnEventModel
    @strawberryA.field(description="""Finds a workflow by their id""")
    async def say_hello_presences(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result


    from .ContentGQLModel import (
        content_by_id,
        content_page,
        content_delete
    )
    content_page = content_page
    content_by_id = content_by_id
    content_delete = content_delete


    from .TaskGQLModel import (
        task_by_id,
        task_page,
        tasks_by_event,
        task_delete

    )
    task_by_id = task_by_id
    task_page = task_page
    tasks_by_event = tasks_by_event
    task_delete = task_delete