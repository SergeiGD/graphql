from typing import Optional
from hotel_business.gateways.permissions_gateway import PermissionsGateway
from ..utils import permission_required, token_required
from hotel_business.session.session import get_session


@token_required
@permission_required(permissions=['show_permission'])
def resolve_permissions(*_, permission_id: Optional[int] = None, current_user):
    with get_session() as db:
        if permission_id:
            return {'permissions': [PermissionsGateway.get_by_id(permission_id, db)], 'status': {
                'success': True,
            }}
        return {'permissions': PermissionsGateway.get_all(db), 'status': {
            'success': True,
        }}
