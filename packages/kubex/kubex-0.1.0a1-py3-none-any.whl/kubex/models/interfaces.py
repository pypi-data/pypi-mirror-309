from kubex.models.base_entity import BaseEntity


class ClusterScopedEntity(BaseEntity): ...


class NamespaceScopedEntity(BaseEntity): ...


class HasStatusSubresource(BaseEntity): ...


class HasScaleSubresource(BaseEntity): ...


class HasLogs(BaseEntity): ...


class Evictable(BaseEntity): ...
