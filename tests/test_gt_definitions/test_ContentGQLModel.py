from tests.gqlshared import (
    create_by_id_test,
    create_page_test,
    create_resolve_reference_test,
    create_frontend_query,
    create_update_query,
    create_delete_query
)
test_reference_content = create_resolve_reference_test(table_name="taskcontents", gqltype="ContentGQLModel")
test_query_content_by_id = create_by_id_test(table_name="taskcontents", query_endpoint="contentById", attribute_names=["id"])
test_query_content_page = create_page_test(table_name="taskcontents", query_endpoint="contentPage", attribute_names=["id"])

test_content_insert = create_frontend_query(query="""
    mutation ($id: UUID, $briefDes: String!, $eventId: UUID!) {
  result: contentInsert(
    content: {id: $id, briefDes: $briefDes, eventId: $eventId}
  ) {
    id
    msg
    task {
      briefDesc
      detailedDesc
      event {
        id
      }
      id
    }
  }
}""",
    variables={"id": "3eb467f0-97ce-4cdc-a3f2-257074038bd9", "briefDes": "tester", "eventId": "45b2df80-ae0f-11ed-9bd8-0242ac110003"}
)
test_content_update = create_update_query(query="""
    mutation ($id: UUID!, $lastchange: DateTime!, $briefDes: String!) {
        result: contentUpdate(content: {id: $id, lastchange: $lastchange, briefDes: $briefDes}) {
            id
            msg
            task {
                id
            }
        }
    }""",
    variables={"id": "3eb467f0-97ce-4cdc-a3f2-257074038bd4", "briefDes": "tester"}, table_name="taskcontents"
)

test_content_delete = create_delete_query(query="""
    mutation($id: UUID!) {
        result: contentDelete(id: $id)
        {
            id
  	        msg
        }
    }""",
    variables={"id": "3eb467f0-97ce-4cdc-a3f2-257074038bd4"},
    table_name="taskcontents"
)