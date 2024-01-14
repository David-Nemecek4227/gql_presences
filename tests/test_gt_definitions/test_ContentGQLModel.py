from tests.gqlshared import (
    create_by_id_test,
    create_page_test,
    create_resolve_reference_test,
    create_frontend_query,
    create_update_query
)
test_reference_content = create_resolve_reference_test(table_name="taskcontents", gqltype="ContentGQLModel")
test_query_content_by_id = create_by_id_test(table_name="taskcontents", query_endpoint="content_by_id", attribute_names=["id"])
test_query_content_page = create_page_test(table_name="taskcontents", query_endpoint="content_page", attribute_names=["id"])

test_content_insert = create_frontend_query(query="""
    mutation ($id: UUID, $brief_des: String!, $event_id: String!) {
        result: content_insert(insert: {id: $id, brief_des: $brief_des, event_id: $event_id}) {
            id
            msg
            }
    }""",
    variables={"id": "3eb467f0-97ce-4cdc-a3f2-257074038bd9", "brief_des": "tester", "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110003"}
)

test_content_update = create_update_query(
    query="""mutation ($id: UUID!, $brief_des: String!, $lastchange: DateTime!) {
        result: content_update(content: {id: $id, brief_des: $brief_des, lastchange: $lastchange}) {
            id
            msg
            }
        
    }""",
    variables={"id": "3eb467f0-97ce-4cdc-a3f2-257074038bd6", "brief_des": "updated"},
    table_name="taskcontents"
)