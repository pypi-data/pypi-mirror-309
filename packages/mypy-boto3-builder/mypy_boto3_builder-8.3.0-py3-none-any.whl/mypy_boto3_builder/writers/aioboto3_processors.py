"""
Processors for parsing and writing `aioboto3` modules.
"""

from collections.abc import Iterable
from pathlib import Path

from boto3.session import Session

from mypy_boto3_builder.constants import TemplatePath
from mypy_boto3_builder.logger import get_logger
from mypy_boto3_builder.package_data import TypesAioBoto3LitePackageData, TypesAioBoto3PackageData
from mypy_boto3_builder.parsers.parse_wrapper_package import parse_types_aioboto3_package
from mypy_boto3_builder.service_name import ServiceName
from mypy_boto3_builder.structures.types_aioboto3_package import TypesAioBoto3Package
from mypy_boto3_builder.utils.path import print_path
from mypy_boto3_builder.writers.package_writer import PackageWriter


def process_types_aioboto3(
    *,
    session: Session,
    output_path: Path,
    service_names: Iterable[ServiceName],
    generate_setup: bool,
    version: str,
    static_files_path: Path,
) -> TypesAioBoto3Package:
    """
    Parse and write stubs package `types-aioboto3`.

    Arguments:
        session -- boto3 session
        output_path -- Package output path
        service_names -- List of known service names
        generate_setup -- Generate ready-to-install or to-use package
        version -- Package version
        static_files_path -- Path to static files

    Return:
        Parsed TypesAioBoto3Package.
    """
    logger = get_logger()
    package = parse_types_aioboto3_package(session, service_names, TypesAioBoto3PackageData)
    package.version = version
    logger.debug(f"Writing {package.pypi_name} to {print_path(output_path)}")

    package_writer = PackageWriter(
        output_path=output_path, generate_setup=generate_setup, cleanup=True
    )
    package_writer.write_package(
        package,
        templates_path=TemplatePath.types_aioboto3,
        static_files_path=static_files_path,
    )
    return package


def process_types_aioboto3_lite(
    *,
    session: Session,
    output_path: Path,
    service_names: Iterable[ServiceName],
    generate_setup: bool,
    version: str,
    static_files_path: Path,
) -> TypesAioBoto3Package:
    """
    Parse and write stubs package `types-aioboto3-lite`.

    Arguments:
        session -- boto3 session
        output_path -- Package output path
        service_names -- List of known service names
        generate_setup -- Generate ready-to-install or to-use package
        version -- Package version
        static_files_path -- Path to static files

    Return:
        Parsed AioBotocoreStubsPackage.
    """
    logger = get_logger()
    package = parse_types_aioboto3_package(session, service_names, TypesAioBoto3LitePackageData)
    package.version = version
    logger.debug(f"Writing {package.pypi_name} to {print_path(output_path)}")

    package_writer = PackageWriter(
        output_path=output_path,
        generate_setup=generate_setup,
        cleanup=True,
    )
    package_writer.write_package(
        package,
        templates_path=TemplatePath.types_aioboto3,
        static_files_path=static_files_path,
        exclude_template_names=["session.pyi.jinja2"],
    )
    return package


def process_types_aioboto3_docs(
    session: Session,
    output_path: Path,
    service_names: Iterable[ServiceName],
) -> TypesAioBoto3Package:
    """
    Parse and write master package docs.

    Arguments:
        session -- boto3 session
        output_path -- Package output path
        service_names -- List of known service names

    Return:
        Parsed AioBotocoreStubsPackage.
    """
    logger = get_logger()
    package = parse_types_aioboto3_package(session, service_names, TypesAioBoto3PackageData)

    logger.debug(f"Writing {package.pypi_name} to {print_path(output_path)}")

    package_writer = PackageWriter(output_path=output_path, generate_setup=False, cleanup=True)
    package_writer.write_docs(
        package,
        templates_path=TemplatePath.types_aioboto3_docs,
    )

    return package
