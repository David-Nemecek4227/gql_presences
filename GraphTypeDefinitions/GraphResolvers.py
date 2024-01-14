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
