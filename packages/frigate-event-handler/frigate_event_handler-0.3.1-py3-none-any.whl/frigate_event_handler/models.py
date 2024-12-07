from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal, TypeVar

from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin

IpCheckLookupSource = Literal["MaxMind", "NEP"]
IpCheckAccessGroup = Literal["NO", "EEA", "WORLD"]
DisplayAspectRatioVideo = Literal["16:9", "4:3"]

T = TypeVar("T", bound="DataClassORJSONMixin")


def list_to_bounding_box(val: list[int]) -> BoundingBox:
    return BoundingBox(*val)


@dataclass
class BaseDataClassORJSONMixin(DataClassORJSONMixin):
    class Config(BaseConfig):
        omit_none = True
        allow_deserialization_not_by_alias = True


@dataclass
class Snapshot(BaseDataClassORJSONMixin):
    frame_time: float
    box: list[int]
    area: int
    region: list[int]
    score: float
    attributes: list[str] | None = None


@dataclass
class BoundingBox(BaseDataClassORJSONMixin):
    x1: int
    y1: int
    x2: int
    y2: int


@dataclass(kw_only=True)
class Event(BaseDataClassORJSONMixin):
    id: str
    camera: str
    frame_time: datetime = field(
        metadata=field_options(
            deserialize=lambda value: datetime.fromtimestamp(value, tz=timezone.utc),
            serialize=lambda value: value.timestamp(),
        )
    )
    snapshot: Snapshot | None
    label: str
    sub_label: str | None
    top_score: float
    false_positive: bool
    start_time: datetime = field(
        metadata=field_options(
            deserialize=lambda value: datetime.fromtimestamp(value, tz=timezone.utc),
            serialize=lambda value: value.timestamp(),
        )
    )
    end_time: datetime | None = field(
        default=None,
        metadata=field_options(
            deserialize=lambda value: datetime.fromtimestamp(value, tz=timezone.utc),
            serialize=lambda value: value.timestamp(),
        ),
    )
    score: float
    box: BoundingBox = field(metadata=field_options(deserialize=list_to_bounding_box))
    area: int
    ratio: float
    region: BoundingBox = field(metadata=field_options(deserialize=list_to_bounding_box))
    active: bool
    stationary: bool
    motionless_count: int
    position_changes: int
    current_zones: list[str]
    entered_zones: list[str]
    has_clip: bool
    has_snapshot: bool
    attributes: dict[str, str]
    current_attributes: list[str]
    pending_loitering: bool


@dataclass
class EventMessage(BaseDataClassORJSONMixin):
    type: str
    before: Event
    after: Event


@dataclass
class StatusResponse(BaseDataClassORJSONMixin):
    success: bool
    message: str
