from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseK8sModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
