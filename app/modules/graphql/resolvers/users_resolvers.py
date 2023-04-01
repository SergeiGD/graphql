from ...models.users import Worker, Client


def resolve_user_type(obj, *_):
    if isinstance(obj, Worker):
        return "Worker"
    if isinstance(obj, Client):
        return "Client"
    return None
