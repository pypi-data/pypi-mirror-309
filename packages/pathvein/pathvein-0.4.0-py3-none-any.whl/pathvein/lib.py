import logging
from pathlib import Path
from typing import Annotated, Iterable
from .pattern import FileStructurePattern

logger = logging.getLogger(__name__)


def set_logger_level(verbosity: int, default: int = logging.ERROR) -> None:
    """
    Set the logger level based on the level of verbosity

    level = default - 10*verbosity

    verbosity = # of -v flags passed

    default = 30 = logging.ERROR

    level with -v   = 30 = logging.WARNING
    level with -vv  = 20 = logging.INFO
    level with -vvv = 10 = logging.DEBUG
    """
    logger.setLevel(default - 10 * verbosity)


def scan(
    path: Path,
    pattern_spec_paths: Iterable[Path],
) -> set[tuple[Path, FileStructurePattern]]:
    """Recursively scan a directory path for directory structures that match the requirements"""

    logger.info("Beginning scan of %s", path.as_posix())

    # Resolve to real paths to ensure that things like .exist() and .is_dir() work correctly
    path = path.resolve()

    requirements = [FileStructurePattern.load_json(path) for path in pattern_spec_paths]

    for structure in requirements:
        logger.debug("Scanning for paths that match structure: %s", structure)

    matches = set()
    for dirpath, dirnames, filenames in path.walk():
        logger.debug("Path.walk: (%s, %s, %s)", dirpath, dirnames, filenames)
        for structure in requirements:
            if structure.matches((dirpath, dirnames, filenames)):
                logger.debug("Matched structure %s in %s", structure, dirpath)
                matches.add((dirpath, structure))

    logger.debug("Matching paths: %s", matches)

    return matches


def shuffle(
    source: Path,
    destination: Path,
    pattern_spec_paths: Iterable[Path],
    overwrite: bool = False,
    dryrun: bool = False,
) -> None:
    """Recursively scan a source path for mission-like directory structures and copy them to the destination."""
    matches = scan(source, pattern_spec_paths)

    logger.info("Beginning shuffle organization of %s to %s", source, destination)

    # Resolve to real paths to ensure that things like .exist() and .is_dir() work correctly
    source = source.resolve()
    destination = destination.resolve()

    # Side effect time!
    copied_count = 0
    for path, pattern in matches:
        destination_path = destination / path.name
        try:
            pattern.copy(path, destination_path, overwrite=overwrite, dryrun=dryrun)
            logger.debug("%s copied to %s", path, destination_path)
            copied_count += 1
        except FileExistsError:
            logger.error(
                "Destination folder exists already: %s. Skipping: %s",
                destination_path,
                path.name,
            )

    logger.info("Finished shuffle organization of %s to %s", source, destination)
    logger.info("Copied %s missions", copied_count)
