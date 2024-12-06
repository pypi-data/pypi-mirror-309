import argh
from geler import freeze


def run_cli():
    # parser = argh.ArghParser()
    # parser.add_commands([freeze])
    # parser.dispatch()
    argh.dispatch_command(freeze)


if __name__ == "__main__":
    run_cli()
