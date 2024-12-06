"""
Weaviate Vector Database Demo
Basic operations with Weaviate's Python client.
"""

import weaviate
from weaviate.embedded import EmbeddedOptions


def test_weaviate():
    # Initialize client (using embedded mode for demo)
    client = weaviate.Client(embedded_options=EmbeddedOptions())
    print("Connected to Weaviate")

    # Create schema
    class_obj = {
        "class": "Article",
        "vectorizer": "text2vec-transformers",
        "properties": [{"name": "content", "dataType": ["text"]}],
    }

    client.schema.create_class(class_obj)
    print("Schema created")

    # Add data
    client.data_object.create({"content": "This is a test article"}, "Article")
    print("Data added")


if __name__ == "__main__":
    test_weaviate()
