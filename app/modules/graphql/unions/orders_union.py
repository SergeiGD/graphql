from ...models.orders import Order, Cart


def resolve_order_type(obj, *_):
    if isinstance(obj, Order):
        return 'Order'
    if isinstance(obj, Cart):
        return 'Cart'
    return None
