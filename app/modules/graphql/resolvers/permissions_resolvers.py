from typing import Optional
from ...models.base import db
from ...models.permissions import Permission
from ..utils import permission_required, token_required


@token_required
@permission_required(permissions=['show_permission'])
def resolve_permissions(*_, permission_id: Optional[int] = None, current_user):
    if permission_id:
        permission = db.session.query(Permission).filter_by(id=permission_id)
        return {'permissions': permission, 'status': {
            'success': True,
        }}
    permissions = db.session.query(Permission).all()
    return {'permissions': permissions, 'status': {
        'success': True,
    }}
