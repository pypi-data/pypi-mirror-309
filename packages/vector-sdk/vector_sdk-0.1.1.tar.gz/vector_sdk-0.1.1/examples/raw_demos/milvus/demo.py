"""
Milvus Vector Database Demo
Basic operations with Milvus Python client.
"""

from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections


def test_milvus():
    # Connect to Milvus
    connections.connect("default", host="localhost", port="19530")
    print("Connected to Milvus")

    # Create collection
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=8),
    ]
    schema = CollectionSchema(fields=fields, description="test collection")
    collection = Collection(name="test_collection", schema=schema)
    print("Collection created")


if __name__ == "__main__":
    test_milvus()
