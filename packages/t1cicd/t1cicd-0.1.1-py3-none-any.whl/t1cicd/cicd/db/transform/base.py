from typing import Optional, Type

from pydantic import BaseModel
from typing_extensions import Generic, TypeVar

T = TypeVar("T", bound=BaseModel)
R = TypeVar("R", bound=BaseModel)


class ModelRelationship(Generic[T, R]):
    def __init__(
        self,
        parent_model: Type[T],
        related_model: Type[R],
        related_ids_field: str,
        nested_relationship: Optional["ModelRelationship"] = None,
    ):
        self.parent_model = parent_model
        self.related_model = related_model
        self.related_ids_field = related_ids_field
        self.nested_relationship = nested_relationship

    def replace_ids_with_objects(
        self,
        parent: T,
        related_objects: list[R],
        next_level_objects: list | None = None,
    ) -> dict:
        result = parent.model_dump()
        objects_map = {obj.id: obj for obj in related_objects}

        nest_field_name = self.related_model.__name__.lower()

        related_ids = result.pop(self.related_ids_field)

        nested_objects = []
        for _id in related_ids:
            if _id in objects_map:
                obj = objects_map[_id]
                if self.nested_relationship and next_level_objects:
                    nested_objects.append(
                        self.nested_relationship.replace_ids_with_objects(
                            obj, next_level_objects
                        )
                    )
                else:
                    nested_objects.append(obj.model_dump())

        result[nest_field_name] = nested_objects
        return result
