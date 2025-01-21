import logging

from rich.logging import RichHandler


def setup_logging():
    """Setup logging"""

    # Replace the basic logging config with Rich handler
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)],
    )
    logger = logging.getLogger(__name__)
    logging.getLogger("httpx").setLevel(logging.WARNING)
