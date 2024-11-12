import json

def load_list_resource(filename: str, type: type = None):
    with open(filename, "r") as file:
        items = json.loads(file.read())
    
    if type is None:
        return items
    
    serialized_items = []
    for item in items:
        serialized_items.append(type(**item))
    return serialized_items