import uuid
from app.crud.users import get_user_type

def get_user_type_from_id(id: int):
    return get_user_type(id)

def get_uuid(namespace: str):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, namespace))

def get_file_unique_name(user_id: int, listing_id: int, name: str):
    import time
    current_time = int(time.time())
    unique_part = f'{user_id}_{listing_id}_{current_time}'
    unique_id = get_uuid(unique_part)
    return f'{name}_{unique_id}.pdf'
