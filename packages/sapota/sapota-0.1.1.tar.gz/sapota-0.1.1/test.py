from sapota import Sapota, HTTPMETHOD, SapotaCollection
import json
def test_sapota():
    url = "https://api.example.com/data"
    headers = [("Content-Type", "application/json"), ("Authorization", "Bearer YOUR_TOKEN")]
    method = HTTPMETHOD.POST
    body = '{"key1":"value1", "key2":"value2"}'

    d = Sapota(url, headers, method, body)
    command = d.get_request_command()
    print(command)
    
    expected_command = (
        'curl -X POST https://api.example.com/data '
        '-H "Content-Type: application/json" '
        '-H "Authorization: Bearer YOUR_TOKEN" '
        "-d '{\"key1\":\"value1\", \"key2\":\"value2\"}'"
    )

    assert command == expected_command, f"Expected: {expected_command}, but got: {command}"
    print("Test passed!")

def test_sapota_collection():
    url = "https://api.example.com/data"
    headers = [("Content-Type", "application/json"), ("Authorization", "Bearer YOUR_TOKEN")]
    method = HTTPMETHOD.POST
    body = '{"key1":"value1", "key2":"value2"}'

    d = Sapota(url, headers, method, body)
    d2 = Sapota(url, headers, method, body)
    d3 = Sapota(url, headers, method, body)
    d_collection = [d,d2,d3]
    collection = SapotaCollection(d_collection)
    postman_collection_json = collection.export_collection()
    print(postman_collection_json)
    
    with open("sapota_collection.json", "w") as f:
        f.write(postman_collection_json)
    print("Collection saved as sapota_collection.json")
    
if __name__ == "__main__":
    test_sapota()
    test_sapota_collection()