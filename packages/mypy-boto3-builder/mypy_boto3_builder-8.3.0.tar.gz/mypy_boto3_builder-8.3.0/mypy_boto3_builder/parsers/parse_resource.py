"""
Parser for Boto3 ServiceResource sub-resource, produces `structures.Resource`.
"""

import inspect
from types import MethodType

from boto3.docs.utils import is_resource_action
from boto3.resources.base import ServiceResource as Boto3ServiceResource

from mypy_boto3_builder.logger import get_logger
from mypy_boto3_builder.parsers.helpers import get_dummy_method
from mypy_boto3_builder.parsers.parse_attributes import parse_attributes
from mypy_boto3_builder.parsers.parse_collections import parse_collections
from mypy_boto3_builder.parsers.parse_references import parse_references
from mypy_boto3_builder.parsers.shape_parser import ShapeParser
from mypy_boto3_builder.service_name import ServiceName
from mypy_boto3_builder.structures.attribute import Attribute
from mypy_boto3_builder.structures.resource_record import ResourceRecord
from mypy_boto3_builder.type_annotations.internal_import import InternalImport
from mypy_boto3_builder.type_maps.service_stub_map import get_stub_method_map
from mypy_boto3_builder.utils.strings import get_short_docstring


def parse_resource(
    name: str,
    resource: Boto3ServiceResource,
    service_name: ServiceName,
    shape_parser: ShapeParser,
) -> ResourceRecord:
    """
    Parse boto3 sub Resource data.

    Arguments:
        resource -- Original boto3 resource.

    Returns:
        Resource structure.
    """
    logger = get_logger()
    result = ResourceRecord(
        name=name,
        service_name=service_name,
    )

    shape_method_map = shape_parser.get_resource_method_map(name)
    stub_method_map = get_stub_method_map(service_name, name)
    method_map = {**shape_method_map, **stub_method_map}

    public_methods = get_resource_public_methods(resource.__class__)
    for method_name, public_method in public_methods.items():
        method = method_map.get(method_name)

        if method is None:
            logger.warning(f"Unknown method {name}.{method_name}, replaced with a dummy")
            method = get_dummy_method(method_name)

        docstring = get_short_docstring(inspect.getdoc(public_method) or "")
        method.docstring = docstring
        result.methods.append(method)

    attributes = parse_attributes(service_name, name, resource, shape_parser)
    result.attributes.extend(attributes)

    result.attributes.extend(shape_parser.get_resource_identifier_attributes(name))

    references = parse_references(resource)
    result.attributes.extend(references)

    collections = parse_collections(service_name, name, resource, shape_parser)
    for collection in collections:
        result.collections.append(collection)
        result.attributes.append(
            Attribute(
                collection.attribute_name,
                InternalImport(collection.name, service_name, stringify=False),
                is_collection=True,
            )
        )

    return result


def get_resource_public_methods(
    resource_class: type[Boto3ServiceResource],
) -> dict[str, MethodType]:
    """
    Extract public methods from boto3 sub resource.

    Arguments:
        resource_class -- boto3 resource meta.

    Returns:
        A dictionary of method name and method.
    """
    class_members = inspect.getmembers(resource_class)
    methods: dict[str, MethodType] = {}
    for name, member in class_members:
        if name.startswith("_"):
            continue

        if not is_resource_action(member):
            continue

        methods[name] = member

    return methods
