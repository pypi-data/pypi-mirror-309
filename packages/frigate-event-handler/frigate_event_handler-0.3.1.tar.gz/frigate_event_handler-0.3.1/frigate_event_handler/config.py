from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from mashumaro.jsonschema import build_json_schema
from mashumaro.mixins.yaml import DataClassYAMLMixin

if TYPE_CHECKING:
    from os import PathLike


@dataclass
class MQTTConfig(DataClassYAMLMixin):
    host: str = field(default="localhost")
    port: int = field(default=1883)
    topic: str = field(default="frigate/events")
    username: str | None = None
    password: str | None = None
    client_id: str | None = None


@dataclass
class FrigateConfig(DataClassYAMLMixin):
    base_url: str
    api_key: str | None = None


@dataclass
class VisionAgentBaseConfig(DataClassYAMLMixin):
    vision_model: str | None = None
    refine_model: str | None = None
    vision_prompt: str | None = None
    refine_prompt: str | None = None
    prompt_context: str | None = None


@dataclass
class VisionAgentCameraConfig(VisionAgentBaseConfig):
    enabled: bool = True


@dataclass
class VisionAgentConfig(VisionAgentBaseConfig):
    api_base_url: str | None = None
    api_key: str | None = None
    resize_video: tuple[int, int] | None = None
    stack_grid: bool = False
    stack_grid_size: tuple[int, int] | None = None
    remove_similar_frames: bool | None = None
    hashing_max_frames: int | None = None
    hash_size: int | None = None

    cameras: dict[str, VisionAgentCameraConfig] | None = None


@dataclass
class Config(DataClassYAMLMixin):
    mqtt: MQTTConfig
    frigate: FrigateConfig
    vision_agent: VisionAgentConfig
    debug: bool = False
    debug_dir: str = field(default="./debug")


def load_config(config_file: PathLike) -> Config:
    config_file = Path(config_file)
    with config_file.open("r") as f:
        return Config.from_yaml(f.read())


def parse_config(config: str) -> Config:
    return Config.from_yaml(config)


def get_config_json_schema() -> str:
    return build_json_schema(Config).to_json()
