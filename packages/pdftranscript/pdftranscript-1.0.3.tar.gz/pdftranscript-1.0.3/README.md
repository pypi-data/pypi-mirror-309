# PDF to semantic HTML conversion

Transcript contains Python programs whose job is to transcribe PDF into
sematic HTML.

[pdftranscript](pdftranscript/transcript.py)

:   Get semantic HTML from PDFs converted by pdf2htmlEX.

[pdfttf](pdftranscript/ttf.py)

:   Recover lost text from PDFs where true type font characters are nothing more than
    images of themselves.

[pdf2html](pdftranscript/pdf2html.py)

:   Batch process a folder full of PDFs ready for pdftranscript

Read the docstrings for more information.

## Example

[PDF before](https://fmalina.github.io/PDFtranscript/tests/PDF/report-1967329.pdf)
and [semantic HTML after](https://fmalina.github.io/PDFtranscript/tests/HTM/report-1967329.htm)

## Installation
    
    pip install pdftranscript

Get Python installed along with latest pdf2htmlEX. 
on OS X with Homebrew:

    brew install python3 pdf2htmlEX

or on Ubuntu/Debian

    sudo apt update && sudo apt install -y libfontconfig1 libcairo2 libjpeg-turbo8 ttfautohint
    wget -o pdf2htmlEX.deb https://github.com/pdf2htmlEX/pdf2htmlEX/releases/download/v0.18.8.rc1/pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb

Check `sha256sum pdf2htmlEX.deb` matches `4ef2698cbeb6995189ac...`

    sudo apt install ./pdf2htmlEX.deb
    pdf2htmlEX -v

Docker install of pdf2htmlEX is also supported (brew one started failing
as of late). This particular image is tested and used in the default
config via `DOCKER_IMG_TAG`.

    docker pull
    pdf2htmlex/pdf2htmlex:0.18.8.rc2-master-20200820-ubuntu-20.04-x86_64

`pip install pdftranscript` should install `lxml` and `freetype-py` too.

## Configure

Configure your project path in your `.env` file and `config.py` **most
importantly the DATA_DIR**. This can be any folder let\'s say
`DATA_DIR=/path/to/pdf-transcript/tests`. If you use a docker install
of pdf2htmlEX, you\'ll need to set `DOCKER_INSTALL=1` This will mount
your data dir to Docker path. `DOCKER_IMG_TAG` is also
[configurable](pdftranscript/config.py). Go ahead create your `.env` file and add
`DATA_DIR=...`

Your DATA_DIR should end up containing 3 folders: PDF, HTML and HTM if
you otherwise stick with default configuration. Create a 'PDF' folder
inside and drop your PDFs there.

-   PDF is a folder where your PDFs are.
-   HTML is where pdf2htmlEX output (non-semantic HTML) ends up after
    running `./pdf2html.py`, which just runs pdf2htmlEX with suitable
    options.
-   HTM is the final destination where semantic HTML gets born after
    running `./transcript.py`.

## Run

`pdf2html` or `./pdftranscript/pdf2html.py` in a cloned repo.

`pdftranscript` or `./pdftranscript/transcript.py`

When you change configuration within `transcript.py` or tweak some
code. You only need to run `./pdftranscript/transcript.py`

## Development process

Set expected (hand-adjusted) output to aim for and improve codebase to
get transcript output closer to the ideal semantic output. Make sure
your changes don't make output worse for other tests. Use
`ruff check`.
