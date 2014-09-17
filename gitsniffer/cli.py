import click

@click.group()
def cli():
    pass


@cli.command(short_help="Scrape a URL")
@cli.argument("url")
def run(url):
    print url
