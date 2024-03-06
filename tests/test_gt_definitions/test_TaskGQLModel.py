from tests.gqlshared import (
    create_by_id_test,
    create_page_test,
    create_resolve_reference_test,
    create_frontend_query,
    create_update_query,
    create_delete_query
)

test_reference_task = create_resolve_reference_test(table_name="tasks", gqltype="TaskGQLModel")
test_query_task_by_id = create_by_id_test(table_name="tasks", query_endpoint="taskById", attribute_names=["id"])
test_query_content_page = create_page_test(table_name="tasks", query_endpoint="taskPage", attribute_names=["id"])


test_task_insert = create_frontend_query(query="""
    mutation ($name: String!, $id: UUID!, $briefDes: String!, $userId: UUID!) {
  result: taskInsert(
    task: {name: $name, id: $id, briefDes: $briefDes, userId: $userId}
  ) {
    id
    msg
    task {
      briefDes
      dateOfEntry
      dateOfFulfillment
      dateOfSubmission
      detailedDes
      id
      lastchange
      name
      reference
    }
  }
}""",
    variables={"name": "testing", "id": "adde473d-5c78-4171-bf16-8e7f97bef5f3", "briefDes": "tester", "userId": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
)

test_task_update = create_update_query(query="""
    mutation ($id: UUID!, $lastchange: DateTime!, $briefDes: String!) {
        result: taskUpdate(task: {id: $id, lastchange: $lastchange, briefDes: $briefDes}) {
            msg
            task {
                id
            }
        }
    }""",
    variables={"id": "adde473d-5c78-4171-bf16-8e7f97bef5f9", "briefDes": "tester"}, table_name="tasks"
)

test_task_delete = create_delete_query(query="""
    mutation($id: UUID!) {
        result: taskDelete(id: $id)
        {
            id
  	        msg
        }
    }""",
    variables={"id": "adde473d-5c78-4171-bf16-8e7f97bef5f9"},
    table_name="tasks"
)