from collections import namedtuple

from sqlalchemy import (
    Column,
    Index,
    String,
    UniqueConstraint,
)

from ichnaea.models.base import (
    _Model,
    BigIdMixin,
    ValidationMixin,
)
from ichnaea.models.station import (
    StationMixin,
    StationBlacklistMixin,
)

WifiKey = namedtuple('WifiKey', 'key')


def to_wifikey(obj):
    if isinstance(obj, dict):  # pragma: no cover
        return WifiKey(key=obj['key'])
    elif isinstance(obj, basestring):  # pragma: no cover
        return WifiKey(key=obj)
    else:
        return WifiKey(key=obj.key)


def join_wifikey(model, k):
    return (model.key == k.key,)


class WifiKeyMixin(ValidationMixin):

    key = Column(String(12))

    @classmethod
    def valid_schema(cls):
        from ichnaea.data.schema import ValidWifiKeySchema
        return ValidWifiKeySchema


class WifiMixin(BigIdMixin, WifiKeyMixin):
    pass


class Wifi(WifiMixin, StationMixin, _Model):
    __tablename__ = 'wifi'

    _indices = (
        UniqueConstraint('key', name='wifi_key_unique'),
        Index('wifi_created_idx', 'created'),
        Index('wifi_new_measures_idx', 'new_measures'),
        Index('wifi_total_measures_idx', 'total_measures'),
    )

    def __init__(self, *args, **kw):
        if 'new_measures' not in kw:
            kw['new_measures'] = 0
        if 'total_measures' not in kw:
            kw['total_measures'] = 0
        super(Wifi, self).__init__(*args, **kw)


class WifiBlacklist(WifiMixin, StationBlacklistMixin, _Model):
    __tablename__ = 'wifi_blacklist'

    _indices = (
        UniqueConstraint('key', name='wifi_blacklist_key_unique'),
    )
