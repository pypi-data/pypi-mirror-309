"""Herd gRPC client library."""
import json
import grpc
from typing import Optional
from . import keyvaluestore_pb2 as herd_serv
from . import keyvaluestore_pb2_grpc as herd_grpc

class HerdClient:
    """Client for the Herd gRPC service."""
    
    # Initialize the client with host and port
    def __init__(self, host: str = 'localhost', port: int = 50051):
        """Initialize the client with host and port."""
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = herd_grpc.KeyValueServiceStub(self.channel)
        
        # Check if the channel is ready
        try:
            grpc.channel_ready_future(self.channel).result(timeout=10)
            print("Channel is ready")
        except grpc.FutureTimeoutError:
            print("Error: Channel not ready")
    
    # Set a value in the key-value store.
    # Returns True if the value was converted to json -> bytes, and set successfully.
    def set(self, key: str, value) -> bool:
        """Set a key-value pair."""

        # Convert value to json string bytes
        value_jbytes = json.dumps(value).encode('utf-8')

        request = herd_serv.SetRequest(key=key, value=value_jbytes)
        response = self.stub.Set(request)
        return response.item.key == key and response.item.value == value_jbytes
    
    def get(self, key: str) -> Optional[bytes]:
        """Get value by key."""
        request = herd_serv.GetRequest(key=key)
        response = self.stub.Get(request)

        # Convert value bytes to string
        value = json.loads(response.value.decode('utf-8'))

        # Response is KeyValue message
        return value if response.key == key else None

    def getAll(self) -> Optional[dict]:
        """Get all key-value pairs."""
        request = herd_serv.GetAllRequest()
        response = self.stub.GetAll(request)
        return {item.key: json.loads(item.value.decode('utf-8')) for item in response.items}

    def getKeys(self) -> Optional[list]:
        """Get all keys."""
        request = herd_serv.GetKeysRequest()
        response = self.stub.GetKeys(request)
        
        return [key for key in response.keys]

    def getValues(self) -> Optional[list]:
        """Get all values."""
        request = herd_serv.GetValuesRequest()
        response = self.stub.GetValues(request)

        return [json.loads(value.decode('utf-8')) for value in response.values]
    
    def delete(self, key: str) -> bool:
        """Delete a key-value pair."""
        request = herd_serv.DeleteRequest(key=key)
        response = self.stub.Delete(request)
        return response.deleted_item.key == key

    def deleteAll(self) -> bool:
        """Delete all key-value pairs."""

        request = herd_serv.DeleteAllRequest()
        self.stub.DeleteAll(request)

        # Return true if kv store is empty
        return len(self.getAll()) == 0
    
    def close(self):
        """Close the gRPC channel."""
        self.channel.close()