# Geler

Help convert dynamic websites to static ones.

## Install

    pip install geler-CERTIC

## Usage

As a library in your own program:

    from geler import freeze
    result = freeze("https://acme.tld/", "/path/to/local/dir/", thread_pool_size=1, http_get_timeout=30)
    for err in result.http_errors:
        logger.error(
            f'status {err.get("status_code")} on URL  {err.get("url")}. Contents below:\n{err.get("content")}'
        )

As a CLI tool:

    $> geler --help
    usage: geler [-h] [-t THREAD_POOL_SIZE] [--http-get-timeout HTTP_GET_TIMEOUT] start-from-url save-to-path
    
    positional arguments:
      start-from-url        -
      save-to-path          -
    
    optional arguments:
      -h, --help            show this help message and exit
      -t THREAD_POOL_SIZE, --thread-pool-size THREAD_POOL_SIZE
                            1
      --http-get-timeout HTTP_GET_TIMEOUT
                            30


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
- only patches URLs in `*.html` files and `*.css` files, not `*.js` files.
- does not throttle requests
- does not respect `robots.txt`