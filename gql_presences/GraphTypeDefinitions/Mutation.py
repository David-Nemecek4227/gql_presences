import strawberry as strawberryA
from typing import Annotated


TaskInsertGQLModel = Annotated["TaskInsertGQLModel", strawberryA.lazy(".TaskGQLModel")]
TaskResultGQLModel = Annotated["TaskResultGQLModel", strawberryA.lazy(".TaskGQLModel")]
TaskUpdateGQLModel = Annotated["TaskUpdateGQLModel", strawberryA.lazy(".TaskGQLModel")]


def getLoaders(info):
    return info.context['all']


@strawberryA.type
class Mutation:
    @strawberryA.mutation(description="Adds a task.")
    async def task_insert(self, info: strawberryA.types.Info, task: TaskInsertGQLModel) -> TaskResultGQLModel:
        loader = getLoaders(info).tasks
        row = await loader.insert(task)
        result = TaskResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="Update the task.")
    async def task_update(self, info: strawberryA.types.Info, task: TaskUpdateGQLModel) -> TaskResultGQLModel:
        loader = getLoaders(info).tasks
        row = await loader.update(task)
        result = TaskResultGQLModel()
        result.msg = "ok"
        result.id = task.id
        if row is None:
            result.msg = "fail"

        return result
