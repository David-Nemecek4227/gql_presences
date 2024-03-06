import strawberry as strawberryA
from typing import Annotated




@strawberryA.type
class Mutation:

    from .TaskGQLModel import (
        task_insert,
        task_update,
        task_delete
    )
    task_insert=task_insert
    task_update=task_update
    task_delete=task_delete

    from .ContentGQLModel import (
        content_insert,
        content_update,
        content_delete
    )
    content_update=content_update
    content_insert=content_insert
    content_delete=content_delete
