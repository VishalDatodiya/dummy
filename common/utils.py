import base64, json


def encode(obj):
    return base64.b64encode(json.dumps(obj).encode()).decode()


def decode(data):
    return json.loads(base64.b64decode(data.encode()).decode())
    
    
print(encode(3))

print(decode('MTIz'))