import click
import hcs_ext_hoc as hoc
import hcs_core.sglib.cli_options as cli


@click.command()
@cli.org_id
@click.option("--template", "-t", required=False)
@click.option("--vm", "-v", required=False)
def inspect(org: str, template: str, vm: str):
    return hoc.inspect(org, template, vm)
