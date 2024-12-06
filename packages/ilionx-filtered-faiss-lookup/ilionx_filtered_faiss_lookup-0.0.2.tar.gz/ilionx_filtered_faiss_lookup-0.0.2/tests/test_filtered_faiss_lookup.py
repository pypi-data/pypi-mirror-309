import pytest
import unittest

from promptflow.connections import CustomConnection
from ilionx_filtered_faiss_lookup.tools.filtered_faiss_lookup import filtered_faiss_lookup


@pytest.fixture
def my_custom_connection() -> CustomConnection:
    my_custom_connection = CustomConnection(
        {
            "api-key" : "my-api-key",
            "api-secret" : "my-api-secret",
            "api-url" : "my-api-url"
        }
    )
    return my_custom_connection


class TestTool:
    def test_filtered_faiss_lookup(self, my_custom_connection):
        result = filtered_faiss_lookup(my_custom_connection, input_text="Microsoft")
        assert result == "Hello Microsoft"


# Run the unit tests
if __name__ == "__main__":
    unittest.main()