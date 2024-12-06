"""Module for dynamic serializers using Django REST Framework."""

from typing import List, Dict, Any, Type
from rest_framework import serializers

FIELD_TYPE_MAP: Dict[str, Type[serializers.Field]] = {
    "CharField": serializers.CharField,
    "EmailField": serializers.EmailField,
    "URLField": serializers.URLField,
    "UUIDField": serializers.UUIDField,
    "IntegerField": serializers.IntegerField,
    "FloatField": serializers.FloatField,
    "DecimalField": serializers.DecimalField,
    "BooleanField": serializers.BooleanField,
    "DateField": serializers.DateField,
    "DateTimeField": serializers.DateTimeField,
    "TimeField": serializers.TimeField,
    "ListField": serializers.ListField,
    "DictField": serializers.DictField,
    "ChoiceField": serializers.ChoiceField,
    "SlugField": serializers.SlugField,
    "FileField": serializers.FileField,
    "ImageField": serializers.ImageField,
    "SerializerMethodField": serializers.SerializerMethodField,
    "HyperlinkedIdentityField": serializers.HyperlinkedIdentityField,
    "HyperlinkedRelatedField": serializers.HyperlinkedRelatedField,
    "PrimaryKeyRelatedField": serializers.PrimaryKeyRelatedField,
    "RelatedField": serializers.RelatedField,
}


class DynamicSerializer(serializers.Serializer):
    """Base class for dynamic serializers."""

    def create(self, validated_data: Dict[str, Any]) -> Any:
        """Create an instance based on validated data.

        Args:
            validated_data (Dict[str, Any]): The validated data to create an instance.

        Returns:
            Any: The created instance (replace with actual creation logic).
        """
        return validated_data  # Replace with actual creation logic

    def update(self, instance: Any, validated_data: Dict[str, Any]) -> Any:
        """Update an instance based on validated data.

        Args:
            instance (Any): The instance to update.
            validated_data (Dict[str, Any]): The validated data to update the instance.

        Returns:
            Any: The updated instance (replace with actual update logic).
        """
        return validated_data  # Replace with actual update logic

    def get_fields_config(self) -> Dict[str, Any]:
        """Return the fields configuration as a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the fields configuration.
        """
        fields_config = {}
        for field_name, field in self.fields.items():
            field_info = {
                "name": field_name,
                "type": field.__class__.__name__,
                "required": getattr(field, "required", None),
                "default": getattr(field, "default", None),
                "validators": [
                    validator.__class__.__name__ for validator in field.validators
                ],
            }
            # Include additional attributes dynamically
            for attr in dir(field):
                if not attr.startswith("_") and attr not in field_info:
                    field_info[attr] = getattr(field, attr)

            fields_config[field_name] = field_info

        return fields_config


def create_dynamic_serializer(
    field_config: List[Dict[str, Any]],
    base_class: Type[DynamicSerializer] = DynamicSerializer,
) -> Type[DynamicSerializer]:
    """Create a dynamic serializer class based on field configuration.

    Args:
        field_config (List[Dict[str, Any]]): A list of dictionaries defining the fields.

    Returns:
        Type[DynamicSerializer]: A dynamically created serializer class.
    """
    fields: Dict[str, serializers.Field] = {}

    for field_info in field_config:
        field_name = field_info["name"]
        field_type = field_info.get("type", "CharField")
        validators = field_info.get("validators", [])
        default_value = field_info.get("default", None)
        kwargs = field_info.get("kwargs", {})
        field_class = FIELD_TYPE_MAP.get(field_type)
        fields[field_name] = field_class(
            validators=validators, default=default_value, **kwargs
        )

    return type("DynamicSerializer", (base_class,), fields)
