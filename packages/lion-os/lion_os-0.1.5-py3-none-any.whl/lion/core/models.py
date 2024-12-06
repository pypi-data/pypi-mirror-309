"""Configuration class for dynamically creating new Pydantic models.

    Provides a structured way to define and create Pydantic models with:
    - Field composition from multiple sources
    - Base class inheritance
    - Validation rules
    - Model configuration
    - Documentation

    Example:
        ```python
        # Define fields
        fields = [
            FieldModel(
                name="id",
                annotation=int,
                description="Unique identifier"
            ),
            FieldModel(
                name="name",
                annotation=str,
                validator=lambda v: v.strip()
            )
        ]

        # Configure model
        params = NewModelParams(
            name="UserModel",
            field_models=fields,
            doc="User data model",
            frozen=True  # Make immutable
        )

        # Create model class
        UserModel = params.create_new_model()
        ```

    Attributes:
        name: Model class name, defaults to "StepModel"
        parameter_fields: Field definitions as FieldInfo objects
        base_type: Base model class to inherit from
        field_models: Field definitions as FieldModel objects
        exclude_fields: Fields to exclude from model
        field_descriptions: Field documentation mapping
        inherit_base: Whether to inherit from base_type
        config_dict: Model configuration options
        doc: Model docstring
        frozen: Whether model is immutable

    Notes:
        - Fields can come from parameter_fields or field_models
        - Base type fields are inherited if inherit_base=True
    # Dynamic field model
    class DynamicModel(OperableModel):
        base_field: str = "base"

    model = DynamicModel()
    model.add_field("dynamic_field", value="dynamic")

    # Nested data container
    note = Note(
        user={"name": "John", "age": 30},
        settings={"theme": "dark"}
    )
    note.get(["user", "name"])  # "John"
    ```

For detailed documentation and examples, see:
    docs/api_reference/models-api-reference.md

Copyright 2024 HaiyangLi

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import inspect
from collections.abc import Callable, ItemsView, Iterator, ValuesView
from typing import Any, Self, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    create_model,
    field_serializer,
    field_validator,
    model_validator,
)
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from typing_extensions import override

from lion.libs.constants import UNDEFINED
from lion.libs.parse import (
    flatten,
    is_same_dtype,
    nget,
    ninsert,
    npop,
    nset,
    to_list,
    validate_boolean,
)
from lion.libs.utils import copy

INDICE_TYPE = str | list[str | int]
FIELD_NAME = TypeVar("FIELD_NAME", bound=str)


common_config = {
    "populate_by_name": True,
    "arbitrary_types_allowed": True,
    "use_enum_values": True,
}


class BaseAutoModel(BaseModel):
    """Base model class with enhanced serialization capabilities.

    Extends Pydantic's BaseModel to provide:
    - Clean dictionary conversion with UNDEFINED handling
    - Nested model serialization
    - Hash generation based on model content
    - Validation rules

    Example:
        ```python
        class User(BaseAutoModel):
            name: str = Field(min_length=2)
            age: int | None = None
            settings: dict = Field(default_factory=dict)

        user = User(name="John", age=30)
        data = user.to_dict(clean=True)  # Excludes UNDEFINED values
        ```

    Attributes:
        model_config: Default configuration for all instances
            - validate_default: True to validate default values
            - populate_by_name: True to allow field population by alias
            - arbitrary_types_allowed: True to allow any type
            - use_enum_values: True to use enum values in serialization
    """

    def to_dict(self, clean: bool = False) -> dict[str, Any]:
        """Convert model to dictionary, with optional cleaning.

        Args:
            clean: If True, exclude UNDEFINED values from output.
                  If False, include all fields using model_dump().

        Returns:
            Dictionary representation of model with nested models serialized
        """
        if not clean:
            return self.model_dump()
        return {
            k: v
            for k, v in self.model_dump(exclude_unset=True).items()
            if v is not UNDEFINED
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create model instance from dictionary data.

        Args:
            data: Dictionary containing field values

        Returns:
            New model instance

        Raises:
            ValueError: If required fields are missing or validation fails
        """
        return cls.model_validate(data)

    def __hash__(self) -> int:
        """Generate hash based on model's clean dictionary representation.

        Returns:
            Hash value that uniquely identifies the model's content
        """
        return hash(str(self.to_dict(True)))


class SchemaModel(BaseAutoModel):
    """Schema definition model with strict validation.

    Extends BaseAutoModel to provide:
    - Extra field forbidding
    - Disabled default validation
    - Field name listing
    - Nested validation

    Example:
        ```python
        class UserSchema(SchemaModel):
            name: str = Field(min_length=2)
            age: int = Field(gt=0)
            settings: dict[str, Any] = Field(default_factory=dict)

        # Raises error - extra fields forbidden
        user = UserSchema(name="John", age=30, extra="value")
        ```

    Attributes:
        model_config: Schema-specific configuration
            - extra: "forbid" to prevent extra fields
            - validate_default: False to skip default validation
            - Plus inherited BaseAutoModel config
    """

    model_config = ConfigDict(extra="forbid", validate_default=False, **common_config)

    @classmethod
    def keys(cls) -> list[str]:
        """Get list of model field names.

        Returns:
            List of field names defined in model schema
        """
        return list(cls.model_fields.keys())


class FieldModel(SchemaModel):
    """Model for defining and managing field definitions.

    Provides a structured way to define fields with:
    - Type annotations and validation
    - Default values and factories
    - Documentation and metadata
    - Serialization options

    Example:
        ```python
        field = FieldModel(
            name="age",
            annotation=int,
            default=0,
            description="User age in years",
            validator=lambda v: v if v >= 0 else 0
        )
        ```

    Attributes:
        default: Default field value
        default_factory: Function to generate default value
        title: Field title for documentation
        description: Field description
        examples: Example values
        validators: Validation functions
        exclude: Exclude from serialization
        deprecated: Mark as deprecated
        frozen: Mark as immutable
        alias: Alternative field name
        alias_priority: Priority for alias resolution
        name: Field name (required)
        annotation: Type annotation
        validator: Validation function
        validator_kwargs: Validator parameters

    Notes:
        - All attributes except 'name' can be UNDEFINED
        - validator_kwargs are passed to field_validator decorator
        - Cannot have both default and default_factory
    """

    model_config = ConfigDict(extra="allow", validate_default=False, **common_config)

    # Field configuration attributes
    default: Any = UNDEFINED  # Default value
    default_factory: Callable = UNDEFINED  # Factory function for default value
    title: str = UNDEFINED  # Field title
    description: str = UNDEFINED  # Field description
    examples: list = UNDEFINED  # Example values
    validators: list = UNDEFINED  # Validation functions
    exclude: bool = UNDEFINED  # Exclude from serialization
    deprecated: bool = UNDEFINED  # Mark as deprecated
    frozen: bool = UNDEFINED  # Mark as immutable
    alias: str = UNDEFINED  # Alternative field name
    alias_priority: int = UNDEFINED  # Priority for alias resolution

    # Core field attributes
    name: str = Field(..., exclude=True)  # Field name (required)
    annotation: type | Any = Field(UNDEFINED, exclude=True)  # Type annotation
    validator: Callable | Any = Field(UNDEFINED, exclude=True)  # Validation function
    validator_kwargs: dict | Any = Field(
        default_factory=dict, exclude=True
    )  # Validator parameters

    @property
    def field_info(self) -> FieldInfo:
        """Generate Pydantic FieldInfo object from field configuration.

        Returns:
            FieldInfo object with all configured attributes

        Notes:
            - Uses clean dict to exclude UNDEFINED values
            - Sets annotation to Any if not specified
            - Preserves all metadata in field_info
        """
        annotation = self.annotation if self.annotation is not UNDEFINED else Any
        field_obj: FieldInfo = Field(**self.to_dict(True))  # type: ignore
        field_obj.annotation = annotation
        return field_obj

    @property
    def field_validator(self) -> dict[str, Callable] | None:
        """Generate field validator configuration.

        Returns:
            Dictionary mapping validator name to function,
            or None if no validator defined

        Notes:
            - Validator name is f"{field_name}_validator"
            - Uses validator_kwargs if provided
            - Returns None if validator is UNDEFINED
        """
        if self.validator is UNDEFINED:
            return None
        kwargs = self.validator_kwargs or {}
        return {
            f"{self.name}_validator": field_validator(self.name, **kwargs)(
                self.validator
            )
        }


class OperableModel(BaseAutoModel):
    """Model class supporting dynamic field management and operations.

    Provides:
    - Dynamic field addition/updates
    - Field attribute access
    - Metadata tracking
    - Nested model serialization

    Example:
        ```python
        class DynamicModel(OperableModel):
            base_field: str = "base"

        model = DynamicModel()

        # Add field with validation
        def validate_positive(v: int) -> int:
            if v <= 0:
                raise ValueError("Must be positive")
            return v

        model.add_field(
            "age",
            value=25,
            annotation=int,
            validator=validate_positive
        )
        ```

    Attributes:
        extra_fields: Dictionary storing dynamic field definitions
        model_config: Configuration forbidding extra direct fields
    """

    model_config = ConfigDict(extra="forbid", validate_default=False, **common_config)

    extra_fields: dict[str, Any] = Field(default_factory=dict)

    @field_serializer("extra_fields")
    def _serialize_extra_fields(
        self,
        value: dict[str, FieldInfo],
    ) -> dict[str, Any]:
        """Serialize extra fields to dictionary format.

        Args:
            value: Dictionary of field name to FieldInfo mappings

        Returns:
            Dictionary of field name to value mappings,
            with nested models serialized
        """
        output_dict = {}
        for k in value.keys():
            k_value = self.__dict__.get(k)
            if isinstance(k_value, BaseAutoModel):
                k_value = k_value.to_dict()
            output_dict[k] = k_value
        return output_dict

    @field_validator("extra_fields")
    def _validate_extra_fields(
        cls,
        value: list[FieldModel] | dict[str, FieldModel | FieldInfo],
    ) -> dict[str, FieldInfo]:
        """Validate and convert extra fields to FieldInfo objects.

        Args:
            value: List of FieldModels or dict of field definitions

        Returns:
            Dictionary mapping field names to FieldInfo objects

        Raises:
            ValueError: If value format is invalid
        """
        out = {}
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, FieldModel):
                    out[k] = v.field_info
                elif isinstance(v, FieldInfo):
                    out[k] = v
            return out

        elif isinstance(value, list) and is_same_dtype(value, FieldModel):
            return {v.name: v.field_info for v in value}

        raise ValueError("Invalid extra_fields value")

    @override
    def __setattr__(self, field_name: str, value: Any) -> None:
        """Set attribute value with metadata tracking.

        This method prevents direct assignment to metadata and extra_fields,
        and tracks the last update time of modified fields.

        Args:
            field_name: Name of the field to set
            value: Value to set

        Raises:
            AttributeError: If attempting to directly assign to metadata or
                extra_fields
        """
        if field_name in self.extra_fields:
            object.__setattr__(self, field_name, value)
        else:
            super().__setattr__(field_name, value)

    @override
    def to_dict(self, clean: bool = False) -> dict:
        """Convert model to dictionary including extra fields.

        Args:
            clean: If True, exclude UNDEFINED values

        Returns:
            Dictionary containing all fields and their values
        """
        dict_ = self.model_dump()
        dict_.pop("extra_fields")
        dict_.update(self._serialize_extra_fields(self.extra_fields))
        if clean:
            for k, v in dict_.items():
                if v is UNDEFINED:
                    dict_.pop(k)
        return dict_

    @property
    def all_fields(self) -> dict[str, FieldInfo]:
        """Get all fields including model fields and extra fields.

        Returns:
            Dictionary mapping field names to FieldInfo objects,
            excluding the extra_fields field itself
        """
        a = {**self.model_fields, **self.extra_fields}
        a.pop("extra_fields", None)
        return a

    def add_field(
        self,
        field_name: FIELD_NAME,
        /,
        value: Any = UNDEFINED,
        annotation: type = UNDEFINED,
        field_obj: FieldInfo = UNDEFINED,
        field_model: FieldModel = UNDEFINED,
        **kwargs,
    ) -> None:
        """Add a new field to the model's extra fields.

        Args:
            field_name: Name of the field to add
            value: Field value
            annotation: Type annotation
            field_obj: Pre-configured FieldInfo object
            field_model: Pre-configured FieldModel object
            **kwargs: Additional field configuration

        Raises:
            ValueError: If field already exists or invalid configuration
        """
        if field_name in self.all_fields:
            raise ValueError(f"Field '{field_name}' already exists")

        self.update_field(
            field_name,
            value=value,
            annotation=annotation,
            field_obj=field_obj,
            field_model=field_model,
            **kwargs,
        )

    def update_field(
        self,
        field_name: FIELD_NAME,
        /,
        value: Any = UNDEFINED,
        annotation: type = UNDEFINED,
        field_obj: FieldInfo = UNDEFINED,
        field_model: FieldModel = UNDEFINED,
        **kwargs,
    ) -> None:
        """Update existing field or create new one.

        Args:
            field_name: Name of field to update
            value: New field value
            annotation: Type annotation
            field_obj: Pre-configured FieldInfo object
            field_model: Pre-configured FieldModel object
            **kwargs: Additional field configuration

        Raises:
            ValueError: If invalid configuration provided
        """
        if "default" in kwargs and "default_factory" in kwargs:
            raise ValueError(
                "Cannot provide both 'default' and 'default_factory'",
            )

        if field_obj and field_model:
            raise ValueError(
                "Cannot provide both 'field_obj' and 'field_model'",
            )

        # Handle field_obj
        if field_obj:
            if not isinstance(field_obj, FieldInfo):
                raise ValueError(
                    "Invalid field_obj, should be a pydantic FieldInfo object"
                )
            self.extra_fields[field_name] = field_obj

        if field_model:
            if not isinstance(field_model, FieldModel):
                raise ValueError("Invalid field_model, should be a FieldModel object")
            self.extra_fields[field_name] = field_model.field_info

        # Handle kwargs
        if kwargs:
            if field_name in self.all_fields:  # existing field
                for k, v in kwargs.items():
                    self.field_setattr(field_name, k, v)
            else:
                self.extra_fields[field_name] = Field(**kwargs)

        # Handle no explicit defined field
        if not field_obj and not kwargs:
            if field_name not in self.all_fields:
                self.extra_fields[field_name] = Field()

        field_obj = self.all_fields[field_name]

        # Handle annotation
        if annotation is not None:
            field_obj.annotation = annotation
        if not field_obj.annotation:
            field_obj.annotation = Any

        # Handle value
        if value is UNDEFINED:
            if getattr(self, field_name, UNDEFINED) is not UNDEFINED:
                value = getattr(self, field_name)
            elif getattr(field_obj, "default") is not PydanticUndefined:
                value = field_obj.default
            elif getattr(field_obj, "default_factory"):
                value = field_obj.default_factory()

        setattr(self, field_name, value)

    def field_setattr(
        self,
        field_name: FIELD_NAME,
        attr: str,
        value: Any,
        /,
    ) -> None:
        """Set attribute value for a field.

        Args:
            field_name: Name of field to modify
            attr: Name of attribute to set
            value: Value to set

        Raises:
            KeyError: If field not found
        """
        all_fields = self.all_fields
        if field_name not in all_fields:
            raise KeyError(f"Field {field_name} not found in object fields.")
        field_obj = all_fields[field_name]
        if hasattr(field_obj, attr):
            setattr(field_obj, attr, value)
        else:
            if not isinstance(field_obj.json_schema_extra, dict):
                field_obj.json_schema_extra = {}
            field_obj.json_schema_extra[attr] = value

    def field_hasattr(
        self,
        field_name: FIELD_NAME,
        attr: str,
        /,
    ) -> bool:
        """Check if field has specific attribute.

        Args:
            field_name: Name of field to check
            attr: Name of attribute to check

        Returns:
            True if attribute exists, False otherwise

        Raises:
            KeyError: If field not found
        """
        all_fields = self.all_fields
        if field_name not in all_fields:
            raise KeyError(f"Field {field_name} not found in object fields.")
        field_obj = all_fields[field_name]
        if hasattr(field_obj, attr):
            return True
        elif isinstance(field_obj.json_schema_extra, dict):
            if field_name in field_obj.json_schema_extra:
                return True
        else:
            return False

    def field_getattr(
        self,
        field_name: FIELD_NAME,
        attr: str,
        default: Any = UNDEFINED,
        /,
    ) -> Any:
        """Get attribute value for a field.

        Args:
            field_name: Name of field to access
            attr: Name of attribute to get
            default: Default value if attribute not found

        Returns:
            Attribute value

        Raises:
            KeyError: If field not found
            AttributeError: If attribute not found and no default
        """
        all_fields = self.all_fields

        if field_name not in all_fields:
            raise KeyError(f"Field {field_name} not found in object fields.")

        if str(attr).strip("s").lower() == "annotation":
            return self.model_fields[field_name].annotation

        field_obj = all_fields[field_name]

        # Check fieldinfo attr
        value = getattr(field_obj, attr, UNDEFINED)
        if value is not UNDEFINED:
            return value
        else:
            if isinstance(field_obj.json_schema_extra, dict):
                value = field_obj.json_schema_extra.get(attr, UNDEFINED)
                if value is not UNDEFINED:
                    return value

        # Handle undefined attr
        if default is not UNDEFINED:
            return default
        else:
            raise AttributeError(
                f"field {field_name} has no attribute {attr}",
            )


class Note(BaseAutoModel):
    """Container for managing nested dictionary data structures.

    Provides:
    - Deep nested data access
    - Dictionary-like interface
    - Flattening capabilities
    - Update operations

    Example:
        ```python
        note = Note(
            user={
                "name": "John",
                "settings": {
                    "theme": "dark"
                }
            }
        )

        # Access nested data
        name = note.get(["user", "name"])
        theme = note["user"]["settings"]["theme"]

        # Update nested structure
        note.update(["user", "settings"], {"language": "en"})
        ```

    Attributes:
        content: Nested dictionary structure
        model_config: Configuration allowing arbitrary types
    """

    content: dict[str, Any] = Field(default_factory=dict)  # Nested data structure

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        populate_by_name=True,
    )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize Note with dictionary data.

        Args:
            **kwargs: Key-value pairs for initial content
        """
        super().__init__()
        self.content = kwargs

    @field_serializer("content")
    def _serialize_content(self, value: Any) -> dict[str, Any]:
        """Serialize content to dictionary format.

        Args:
            value: Content to serialize

        Returns:
            Deep copy of content dictionary
        """
        output_dict = copy(value, deep=True)
        return output_dict

    def to_dict(self) -> dict[str, Any]:
        """Convert Note to dictionary, excluding undefined values.

        Returns:
            Dictionary representation with UNDEFINED values removed
        """
        out = copy(self.content)
        for k, v in self.content.items():
            if v is UNDEFINED:
                out.pop(k)
        return out

    def pop(
        self,
        indices: INDICE_TYPE,
        /,
        default: Any = UNDEFINED,
    ) -> Any:
        """Remove and return item from nested structure.

        Args:
            indices: Path to item
            default: Value to return if not found

        Returns:
            Removed value or default

        Raises:
            KeyError: If path not found and no default
        """
        indices = to_list(indices, flatten=True, dropna=True)
        return npop(self.content, indices, default)

    def insert(self, indices: INDICE_TYPE, value: Any, /) -> None:
        """Insert value into nested structure at specified indices.

        Args:
            indices: Path where to insert
            value: Value to insert
        """
        indices = to_list(indices, flatten=True, dropna=True)
        ninsert(self.content, indices, value)

    def set(self, indices: INDICE_TYPE, value: Any, /) -> None:
        """Set value in nested structure at specified indices.

        Args:
            indices: Path where to set
            value: Value to set
        """
        indices = to_list(indices, flatten=True, dropna=True)
        if self.get(indices, None) is None:
            self.insert(indices, value)
        else:
            nset(self.content, indices, value)

    def get(
        self,
        indices: INDICE_TYPE,
        /,
        default: Any = UNDEFINED,
    ) -> Any:
        """Get value from nested structure at specified indices.

        Args:
            indices: Path to value
            default: Value to return if not found

        Returns:
            Value at path or default

        Raises:
            KeyError: If path not found and no default
        """
        indices = to_list(indices, flatten=True, dropna=True)
        return nget(self.content, indices, default)

    def keys(self, /, flat: bool = False, **kwargs: Any) -> list:
        """Get keys of the Note.

        Args:
            flat: If True, return flattened keys
            kwargs: Additional flattening options

        Returns:
            List of keys, optionally flattened
        """
        if flat:
            kwargs["coerce_keys"] = kwargs.get("coerce_keys", False)
            kwargs["coerce_sequence"] = kwargs.get("coerce_sequence", "list")
            return flatten(self.content, **kwargs).keys()
        return list(self.content.keys())

    def values(self, /, flat: bool = False, **kwargs: Any) -> ValuesView:
        """Get values of the Note.

        Args:
            flat: If True, return flattened values
            kwargs: Additional flattening options

        Returns:
            View of values, optionally flattened
        """
        if flat:
            kwargs["coerce_keys"] = kwargs.get("coerce_keys", False)
            kwargs["coerce_sequence"] = kwargs.get("coerce_sequence", "list")
            return flatten(self.content, **kwargs).values()
        return self.content.values()

    def items(self, /, flat: bool = False, **kwargs: Any) -> ItemsView:
        """Get items of the Note.

        Args:
            flat: If True, return flattened items
            kwargs: Additional flattening options

        Returns:
            View of items, optionally flattened
        """
        if flat:
            kwargs["coerce_keys"] = kwargs.get("coerce_keys", False)
            kwargs["coerce_sequence"] = kwargs.get("coerce_sequence", "list")
            return flatten(self.content, **kwargs).items()
        return self.content.items()

    def clear(self) -> None:
        """Clear all content."""
        self.content.clear()

    def update(
        self,
        indices: INDICE_TYPE,
        value: Any,
    ) -> None:
        """Update nested structure at specified indices.

        Args:
            indices: Location to update
            value: New value to set

        Raises:
            ValueError: If trying to update dict with non-dict
        """
        existing = None
        if not indices:
            existing = self.content
        else:
            existing = self.get(indices, None)

        if existing is None:
            if not isinstance(value, (list, dict)):
                value = [value]
            self.set(indices, value)

        if isinstance(existing, list):
            if isinstance(value, list):
                existing.extend(value)
            else:
                existing.append(value)

        elif isinstance(existing, dict):
            if isinstance(value, self.__class__):
                value = value.content

            if isinstance(value, dict):
                existing.update(value)
            else:
                raise ValueError(
                    "Cannot update a dictionary with a non-dictionary value."
                )

    @classmethod
    def from_dict(cls, kwargs: Any) -> "Note":
        """Create Note instance from dictionary.

        Args:
            kwargs: Dictionary to initialize with

        Returns:
            New Note instance
        """
        return cls(**kwargs)

    def __contains__(self, indices: INDICE_TYPE) -> bool:
        """Check if indices exist in content.

        Args:
            indices: Path to check

        Returns:
            True if path exists, False otherwise
        """
        return self.content.get(indices, UNDEFINED) is not UNDEFINED

    def __len__(self) -> int:
        """Get length of content.

        Returns:
            Number of top-level keys
        """
        return len(self.content)

    def __iter__(self) -> Iterator[str]:
        """Get iterator over content.

        Returns:
            Iterator over top-level keys
        """
        return iter(self.content)

    def __next__(self) -> str:
        """Get next item from content iterator.

        Returns:
            Next key in iteration
        """
        return next(iter(self.content))

    @override
    def __str__(self) -> str:
        """Get string representation of content.

        Returns:
            String representation of content dict
        """
        return str(self.content)

    @override
    def __repr__(self) -> str:
        """Get detailed string representation of content.

        Returns:
            Detailed string representation of content dict
        """
        return repr(self.content)

    def __getitem__(self, indices: INDICE_TYPE) -> Any:
        """Get item using index notation.

        Args:
            indices: Path to value

        Returns:
            Value at path

        Raises:
            KeyError: If path not found
        """
        indices = to_list(indices, flatten=True, dropna=True)
        return self.get(indices)

    def __setitem__(self, indices: INDICE_TYPE, value: Any) -> None:
        """Set item using index notation.

        Args:
            indices: Path where to set
            value: Value to set
        """
        self.set(indices, value)


class NewModelParams(SchemaModel):
    """Configuration class for dynamically creating new Pydantic models."""

    name: str | None = None
    parameter_fields: dict[str, FieldInfo] = Field(default_factory=dict)
    base_type: type[BaseModel] = Field(default=BaseModel)
    field_models: list[FieldModel] = Field(default_factory=list)
    exclude_fields: list = Field(default_factory=list)
    field_descriptions: dict = Field(default_factory=dict)
    inherit_base: bool = Field(default=True)
    config_dict: dict | None = Field(default=None)
    doc: str | None = Field(default=None)
    frozen: bool = False
    _validators: dict[str, Callable] | None = PrivateAttr(default=None)
    _use_keys: set[str] = PrivateAttr(default_factory=set)

    @property
    def use_fields(self):
        """Get field definitions to use in new model."""
        params = {k: v for k, v in self.parameter_fields.items() if k in self._use_keys}
        params.update(
            {
                f.name: f.field_info
                for f in self.field_models
                if f.name in self._use_keys
            }
        )
        return {k: (v.annotation, v) for k, v in params.items()}

    @field_validator("parameter_fields", mode="before")
    def validate_parameters(cls, value):
        """Validate parameter field definitions."""
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValueError("Fields must be a dictionary.")
        for k, v in value.items():
            if not isinstance(k, str):
                raise ValueError("Field names must be strings.")
            if not isinstance(v, FieldInfo):
                raise ValueError("Field values must be FieldInfo objects.")
        return copy(value)

    @field_validator("base_type", mode="before")
    def validate_base(cls, value) -> type[BaseModel]:
        """Validate base model type."""
        if value is None:
            return BaseModel
        if isinstance(value, type) and issubclass(value, BaseModel):
            return value
        if isinstance(value, BaseModel):
            return value.__class__
        raise ValueError("Base must be a BaseModel subclass or instance.")

    @field_validator("exclude_fields", mode="before")
    def validate_fields(cls, value) -> list[str]:
        """Validate excluded fields list."""
        if value is None:
            return []
        if isinstance(value, dict):
            value = list(value.keys())
        if isinstance(value, set | tuple):
            value = list(value)
        if isinstance(value, list):
            if not all(isinstance(i, str) for i in value):
                raise ValueError("Field names must be strings.")
            return copy(value)
        raise ValueError("Fields must be a list, set, or dictionary.")

    @field_validator("field_descriptions", mode="before")
    def validate_field_descriptions(cls, value) -> dict[str, str]:
        """Validate field descriptions dictionary."""
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValueError("Field descriptions must be a dictionary.")
        for k, v in value.items():
            if not isinstance(k, str):
                raise ValueError("Field names must be strings.")
            if not isinstance(v, str):
                raise ValueError("Field descriptions must be strings.")
        return value

    @field_validator("inherit_base", mode="before")
    def validate_inherit_base(cls, value) -> bool:
        """Validate inherit_base flag."""
        try:
            return validate_boolean(value)
        except Exception:
            return True

    @field_validator("name", mode="before")
    def validate_name(cls, value) -> str:
        """Validate model name."""
        if value is None:
            return "StepModel"
        if not isinstance(value, str):
            raise ValueError("Name must be a string.")
        return value

    @field_validator("field_models", mode="before")
    def _validate_field_models(cls, value):
        """Validate field model definitions."""
        if value is None:
            return []
        value = [value] if not isinstance(value, list) else value
        if not all(isinstance(i, FieldModel) for i in value):
            raise ValueError("Field models must be FieldModel objects.")
        return value

    @model_validator(mode="after")
    def validate_param_model(self) -> Self:
        """Validate complete model configuration."""
        if self.base_type is not None:
            self.parameter_fields.update(copy(self.base_type.model_fields))

        self.parameter_fields.update({f.name: f.field_info for f in self.field_models})

        use_keys = list(self.parameter_fields.keys())
        use_keys.extend(list(self._use_keys))

        if self.exclude_fields:
            use_keys = [i for i in use_keys if i not in self.exclude_fields]

        self._use_keys = set(use_keys)

        validators = {}

        for i in self.field_models:
            if i.field_validator is not None:
                validators.update(i.field_validator)
        self._validators = validators

        if self.field_descriptions:
            for i in self.field_models:
                if i.name in self.field_descriptions:
                    i.description = self.field_descriptions[i.name]

        if not isinstance(self.name, str):
            if hasattr(self.base_type, "class_name"):
                if callable(self.base_type.class_name):
                    self.name = self.base_type.class_name()
                else:
                    self.name = self.base_type.class_name
            elif inspect.isclass(self.base_type):
                self.name = self.base_type.__name__

        return self

    def create_new_model(self) -> type[BaseModel]:
        """Create new Pydantic model with specified configuration."""
        a: type[BaseModel] = create_model(
            self.name,
            __config__=self.config_dict,
            __doc__=self.doc,
            __base__=self.base_type if self.inherit_base else None,
            __validators__=self._validators,
            **self.use_fields,
        )
        if self.frozen:
            a.model_config["frozen"] = True
        return a


__all__ = [
    "BaseModel",
    "SchemaModel",
    "FieldModel",
    "OperableModel",
    "Note",
    "NewModelParams",
    "BaseAutoModel",
]
