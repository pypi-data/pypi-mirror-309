import argh
from geler import Freezer


def freeze(start_url: str, destination_path: str):
    """
    Freeze given site at start-url to directory at destination-path
    """
    f = Freezer(start_url, destination_path)
    f.freeze()


def run_cli():
    # parser = argh.ArghParser()
    # parser.add_commands([freeze])
    # parser.dispatch()
    argh.dispatch_command(freeze)


if __name__ == "__main__":
    run_cli()
