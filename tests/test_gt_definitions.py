import sys

# setting path
sys.path.append("../gql_granting")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from GraphTypeDefinitions import schema

from .shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    create_context,
)


def createByIdTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    attlist = ' '.join(attributeNames)

    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        assert data.get(tableName, None) is not None
        datatable = data[tableName]
        assert len(datatable) > 0
        datarow = data[tableName][0]

        query = "query($id: ID!){" f"{queryEndpoint}(id: $id)" "{" + attlist + "}}"

        context_value = await create_context(async_session_maker)
        variable_values = {"id": datarow["id"]}
        print("createByIdTest", queryEndpoint, variable_values, flush=True)
        resp = await schema.execute(
            query, context_value=context_value, variable_values=variable_values
        )  # , variable_values={"title": "The Great Gatsby"})
        print(resp, flush=True)
        assert resp.errors is None

        respdata = resp.data[queryEndpoint]

        assert respdata is not None

        for att in attributeNames:
            assert respdata[att] == datarow[att]

    return result_test


def createPageTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    attlist = ' '.join(attributeNames)

    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()

        query = "query{" f"{queryEndpoint}" "{" + attlist + "}}"

        context_value = await create_context(async_session_maker)
        resp = await schema.execute(query, context_value=context_value)
        print(resp, flush=True)
        assert resp.errors is None

        respdata = resp.data[queryEndpoint]
        datarows = data[tableName]

        for rowa, rowb in zip(respdata, datarows):
            for att in attributeNames:
                assert rowa[att] == rowb[att]

    return result_test


def createResolveReferenceTest(tableName, gqltype, attributeNames=["id", "name"]):
    attlist = ' '.join(attributeNames)

    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        table = data[tableName]
        for row in table:
            rowid = row['id']

            query = (
                    'query { _entities(representations: [{ __typename: ' + f'"{gqltype}", id: "{rowid}"' +
                    ' }])' +
                    '{' +
                    f'...on {gqltype}' +
                    '{' +
                    attlist + '}' +
                    '}' +
                    '}')

            context_value = await create_context(async_session_maker)
            resp = await schema.execute(query, context_value=context_value)
            data = resp.data
            print(data, flush=True)
            data = data['_entities'][0]

            assert data['id'] == rowid

    return result_test

# test_query_task_by_id = createByIdTest(tableName="tasks", queryEndpoint="taskById")
# test_query_lessons_page = createPageTest(tableName="plan_lessons", queryEndpoint="plannedLessonPage")

# @pytest.mark.asyncio
# async def test_task_mutation():
#     async_session_maker = await prepare_in_memory_sqllite()
#     await prepare_demodata(async_session_maker)
#
#     data = get_demodata()
#
#     table = data["users"]
#     row = table[0]
#     user_id = row["id"]
#
#
#     name = "task X"
#     query = '''
#             mutation(
#                 $name: String!
#                 $user_id: ID!
#                 ) {
#                 operation: taskInsert(task: {
#                     name: $name
#                     userId: $user_id
#                 }){
#                     id
#                     msg
#                     entity: task {
#                         id
#                         name
#                         lastchange
#                     }
#                 }
#             }
#         '''
#
#     context_value = await create_context(async_session_maker)
#     variable_values = {
#         "user_id": user_id,
#         "name": name
#     }
#     resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
#
#     print(resp, flush=True)
#
#     assert resp.errors is None
#     data = resp.data['operation']
#     assert data["msg"] == "ok"
#     data = data["entity"]
#     assert data["name"] == name
#
#     #assert data["name"] == name
#
#
#     id = data["id"]
#     lastchange = data["lastchange"]
#     name = "NewName"
#     query = '''
#             mutation(
#                 $id: ID!,
#                 $lastchange: DateTime!
#                 $name: String!
#                 ) {
#                 operation: taskUpdate(task: {
#                 id: $id,
#                 lastchange: $lastchange
#                 name: $name
#             }){
#                 id
#                 msg
#                 entity: task {
#                     id
#                     name
#                     lastchange
#                 }
#             }
#             }
#         '''
#     newName = "newName"
#     context_value = await create_context(async_session_maker)
#     variable_values = {"id": id, "name": newName, "lastchange": lastchange}
#     resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
#     assert resp.errors is None
#
#     data = resp.data['operation']
#     assert data['msg'] == "ok"
#     data = data["entity"]
#     assert data["name"] == newName
#
#     # lastchange je jine, musi fail
#     resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
#     assert resp.errors is None
#     data = resp.data['operation']
#     assert data['msg'] == "fail"
#
#     pass
