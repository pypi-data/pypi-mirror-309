import importlib
import inspect
import os
import sys
from types import ModuleType
from typing import Any

import click
from loguru import logger

from earthscale.auth import authenticate as run_auth
from earthscale.auth import get_supabase_client
from earthscale.datasets.dataset import Dataset, DatasetDomain
from earthscale.ingest import (
    ingest_dataset_to_earthscale,
    is_dataset_readable_by_earthscale,
    validate_if_dataset_is_ingestable,
)
from earthscale.repositories.dataset import DatasetRepository


@click.group()
def cli() -> None:
    """Earthscale command line tool."""
    pass


def find_datasets_for_module(
    module: ModuleType,
) -> list[Dataset[Any]]:
    datasets = []
    for _, obj in inspect.getmembers(module):
        if isinstance(obj, Dataset):
            datasets.append(obj)
    return datasets


def _register_dataset(
    dataset: Dataset[Any],
    dataset_repo: DatasetRepository,
    ingest: bool,
) -> None:
    if not is_dataset_readable_by_earthscale(dataset):
        logger.warning(
            f"Dataset {dataset.name} is not readable by Earthscale backend."
            + (
                "Not ingesting dataset as --ingest flag was not provided."
                if not ingest
                else "Ingesting dataset to Earthscale's shared storage..."
            )
        )
        if not ingest:
            return
        validate_if_dataset_is_ingestable(dataset)
        dataset = ingest_dataset_to_earthscale(dataset)
        logger.info("Dataset ingested successfully.")
    dataset_repo.add(dataset)


@cli.command()
@click.argument("module")
@click.option(
    "--domain",
    type=DatasetDomain,
    default=DatasetDomain.WORKSPACE,
    help="Domain of the dataset. Either 'WORKSPACE' or 'ORGANIZATION'. Defaults to "
    "'WORKSPACE'.",
)
@click.option(
    "--ingest",
    is_flag=True,
    help="Ingest any datasets that are not already in Earthscale's shared storage.",
)
def register(
    module: str,
    domain: DatasetDomain,
    ingest: bool,
) -> None:
    # Add cwd to sys.path
    sys.path.insert(0, os.getcwd())

    # Look for all Dataset instances in the module
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        logger.error(f"Error importing module {module}: {e}")
        return
    datasets = find_datasets_for_module(mod)

    client = get_supabase_client()

    dataset_repo = DatasetRepository(
        client,
    )
    registered_datasets = []
    logger.info("Registering datasets...")
    for dataset in datasets:
        if not dataset._explicit_name:
            continue
        logger.info(f"     {dataset.name}")

        if dataset_repo.exists(dataset.name):
            logger.warning(f"Dataset {dataset.name} already exist, overwriting...")

        # TODO: for now the vector data processing POST is blocking, so we
        try:
            _register_dataset(dataset, dataset_repo, ingest)
            registered_datasets.append(dataset)
        except Exception as e:
            logger.error(f"Error registering dataset {dataset.name}: {e}")
            continue

    dset_strs = []
    for i, dataset in enumerate(registered_datasets):
        dset_strs.append(f"     {i+1}. {dataset.name} | {type(dataset).__name__}")

    deploy_summary_msg = (
        f"Registered {len(registered_datasets)} dataset(s) from module `{module}`"
    )
    if len(registered_datasets) == 0:
        logger.info("(Hint: did you remember to add a `name` to each dataset?)")
    else:
        logger.info(deploy_summary_msg)
        logger.info("Datasets:")
    for dset in dset_strs:
        logger.info(dset)


@cli.command()
def authenticate() -> None:
    run_auth()


if __name__ == "__main__":
    cli()
