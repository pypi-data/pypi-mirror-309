import logging
import argh
from geler import Freezer

logger = logging.getLogger(__name__)


def freeze(
    start_from_url: str,
    save_to_path: str,
    thread_pool_size: int = 1,
    http_get_timeout: int = 30,
):
    f = Freezer(
        start_from_url,
        save_to_path,
        thread_pool_size=thread_pool_size,
        http_get_timeout=http_get_timeout,
    )
    f.freeze()
    for err in f.http_errors:
        logger.error(
            f'status {err.get("status_code")} on URL  {err.get("url")}. Contents below:\n{err.get("content")}'
        )


def run_cli():
    argh.dispatch_command(freeze)


if __name__ == "__main__":
    run_cli()
