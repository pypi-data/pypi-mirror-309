# Geler

Help convert dynamic websites to static ones.

## Install

    pip install geler-CERTIC

## Usage

As a library in your own program:

    from geler import freeze
    freeze("https://acme.tld/", "/path/to/local/dir/")

As a CLI tool:
    
    $> geler --help
    usage: geler [-h] start-url destination-path
    
    Freeze given site at start_url to directory at destination_path
    
    positional arguments:
      start-url         -
      destination-path  -
    
    optional arguments:
      -h, --help        show this help message and exit


## Why ?

For [MaX](https://git.unicaen.fr/pdn-certic/MaX) and associated tools, 
we needed a lightweight, portable, pure Python solution to convert 
small dynamic websites to static ones.

## Alternatives

This tool has a narrow scope, on purpose. Please turn to these solutions if you need more:

- [wget](https://www.gnu.org/software/wget/)
- [pywebcopy](https://pypi.org/project/pywebcopy/)
- [HTTrack](https://www.httrack.com)

## Limitations

- only works with HTTP GET
- does not submit forms (even with GET method)
- only considers URLs in `src` or `href` attributes
- only considers URLs with `http` or `https` schemes
- only downloads what is in the same [netloc](https://docs.python.org/3/library/urllib.parse.html) (same domain, same port) as the start URL
- only patches URLs in `*.html` files, not in `*.js`, not in `*.css` (watch out for those `url(...)` in your CSS)