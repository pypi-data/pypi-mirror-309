from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from librbac.domain.permissions import UserProtocol


if TYPE_CHECKING:
    from librbac.domain.permissions import Permission


@dataclass
class OIDCUser(UserProtocol):
    pk: str | UUID
    aud: str
    client_id: str
    exp: int
    iat: int
    iss: str
    sub: str | UUID
    uid: str | UUID
    rbac_permissions: tuple['Permission', ...]

    # пользователь по-умолчанию считается аутентифицированным
    is_authenticated = True


def get_user_from_token(request, id_token) -> OIDCUser:
    """Возвращает объект пользователя с разрешениями."""
    from librbac.contrib.oidc.utis import get_jwt_permissions

    token_data = {**id_token, 'pk': id_token['uid']}
    permissions = tuple(get_jwt_permissions(token_data.pop('permissions')))
    return OIDCUser(**token_data, rbac_permissions=permissions)
