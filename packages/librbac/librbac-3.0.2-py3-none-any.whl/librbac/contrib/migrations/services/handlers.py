from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from explicit.adapters.messaging import AbstractAdapter

from ..domain.events import PermissionMarkedObsolete
from ..domain.events import PermissionsReplaced


def publish_to_adapter(event: PermissionMarkedObsolete | PermissionsReplaced, messaging_adapter: 'AbstractAdapter'):
    """Обработчик событий миграций разрешений, публикующий событий в межсервисную шину."""
    from librbac.contrib.migrations.config import migrations_config
    messaging_adapter.publish(migrations_config.rbac_topic_permission, event.dump())
