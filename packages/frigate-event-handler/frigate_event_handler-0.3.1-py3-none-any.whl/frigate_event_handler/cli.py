import argparse
import asyncio
import logging
import os
from pathlib import Path

from frigate_event_handler.config import Config, parse_config
from frigate_event_handler.daemon import Daemon
from frigate_event_handler.version import __version__


def is_valid_writable_dir(parser, x):
    """Check if directory exists and is writable."""
    if not Path(x).is_dir():
        parser.error(f"{x} is not a valid directory.")
    if not os.access(x, os.W_OK | os.X_OK):
        parser.error(f"{x} is not writable.")
    return Path(x).absolute()


def main_parser() -> argparse.ArgumentParser:
    """Create the ArgumentParser with all relevant subparsers."""
    parser = argparse.ArgumentParser(description="Frigate event handler.")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s v{__version__}")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Logging verbosity level")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--debug-dir",
        help="Directory to output debug files to.",
        metavar="DEBUG_DIR",
        type=lambda x: is_valid_writable_dir(parser, x),
    )
    parser.add_argument(
        "-c", "--config", type=argparse.FileType("r"), default="config.yaml", help="Configuration file"
    )

    parser.set_defaults(func=start)

    return parser


async def start(config: Config):
    """Start the daemon."""
    daemon = Daemon.from_config(config)
    await daemon.run()


def main():
    """Run."""
    parser = main_parser()
    args = parser.parse_args()

    if args.verbose:
        logging_level = 50 - (args.verbose * 10)
        if logging_level <= 0:
            logging_level = logging.NOTSET
    else:
        logging_level = logging.ERROR

    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s [%(name)-25.25s] [%(levelname)-8.8s]  %(message)s",
        handlers=[logging.StreamHandler()],
    )

    config = parse_config(args.config.read())
    if args.debug:
        config.debug = True
    if args.debug_dir:
        config.debug_dir = str(args.debug_dir)
    asyncio.run(args.func(config))


if __name__ == "__main__":
    main()
