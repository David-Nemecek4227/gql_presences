from tests.gqlshared import (
    create_by_id_test,
    create_page_test,
    create_resolve_reference_test,
    create_frontend_query
)

test_reference_task = create_resolve_reference_test(table_name="tasks", gqltype="TaskGQLModel")
test_query_task_by_id = create_by_id_test(table_name="tasks", query_endpoint="task_by_id", attribute_names=["id"])
test_query_content_page = create_page_test(table_name="tasks", query_endpoint="task_page", attribute_names=["id"])


test_task_insert = create_frontend_query(query="""
    mutation ($name: String!, $id: UUID!, $brief_des: String!, $user_id: UUID!) {
        result: content_insert(insert: {name: $name, id: $id, brief_des: $brief_des, user_id: $user_id}) {
            id
            msg
            }
    }""",
    variables={"name": "testing", "id": "adde473d-5c78-4171-bf16-8e7f97bef5f3", "brief_des": "tester", "user_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
)

# test_content_update = create_update_query(
#     query="""mutation ($id: UUID!, $brief_des: String!, $lastchange: DateTime!) {
#         result: content_update(content: {id: $id, brief_des: $brief_des, lastchange: $lastchange}) {
#             id
#             msg
#             }
#
#     }""",
#     variables={"id": "3eb467f0-97ce-4cdc-a3f2-257074038bd6", "brief_des": "updated"},
#     table_name="tasks"
# )