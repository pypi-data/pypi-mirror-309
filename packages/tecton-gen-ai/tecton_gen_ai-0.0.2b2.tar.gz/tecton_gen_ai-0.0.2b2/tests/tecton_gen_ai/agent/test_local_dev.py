from pytest import fixture

from tecton_gen_ai.api import Agent, prompt
from tecton_gen_ai.testing import make_local_batch_feature_view


@fixture
def mock_data():
    return [
        {
            "user_id": "user1",
            "name": "Jim",
            "age": 30,
            "food_preference": "American",
        },
        {
            "user_id": "user2",
            "name": "John",
            "age": 40,
            "food_preference": "Italian",
        },
        {
            "user_id": "user3",
            "name": "Jane",
            "age": 50,
            "food_preference": "Chinese",
        },
    ]


@fixture
def mock_agent_service(tecton_unit_test, mock_data, mock_knowledge):
    user_info = make_local_batch_feature_view(
        "user_info", mock_data, entity_keys=["user_id"], description="User info"
    )

    @prompt(sources=[user_info])
    def sys_prompt(location: str, user_info):
        name = user_info["name"]
        return f"You are serving {name} in {location}"

    def get_tecton_employee_count() -> int:
        """
        Returns the number of employees in Tecton
        """
        return 110

    return Agent(
        name="test",
        description="Test agent",
        prompt=sys_prompt,
        tools=[user_info, get_tecton_employee_count],
        knowledge=[mock_knowledge],
    )


def test_agent(mock_agent_service):
    client = mock_agent_service
    assert "You are serving Jane in Chicago" == client.invoke_prompt(
        dict(user_id="user3", location="Chicago")
    )
    sys_prompt = client.invoke_system_prompt(dict(user_id="user3", location="Chicago"))
    assert "You are serving Jane in Chicago" in sys_prompt
    assert "Test agent" in sys_prompt
    assert "context" in sys_prompt.lower()
    assert client.invoke_tool("user_info", dict(user_id="user1")) == {
        "name": "Jim",
        "age": 30,
        "food_preference": "American",
    }
    assert client.invoke_tool("get_tecton_employee_count") == 110

    assert client.search("knowledge", query="food", filter={"zip": 98010}) == []
    assert (
        len(client.search("knowledge", query="food", top_k=5, filter={"zip": 98005}))
        == 3
    )
    assert len(client.search("knowledge", query="food", top_k=5)) == 5
