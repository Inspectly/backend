import uuid
from crud.users import get_user_type

def get_user_type_from_id(id: int):
    return get_user_type(id)

def get_uuid(namespace: str):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, namespace))
