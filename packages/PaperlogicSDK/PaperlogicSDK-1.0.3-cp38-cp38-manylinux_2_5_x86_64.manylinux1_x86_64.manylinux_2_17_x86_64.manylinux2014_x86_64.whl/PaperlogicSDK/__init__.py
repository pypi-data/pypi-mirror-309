import click
from .sign import sign_pplg, sign_test
from .timestamp import timestamp_pplg, timestamp_test

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-tk', '--api_token', type=str, help='API Token', required=True)
@click.option('-t', '--tenant_id', type=int, help='TenantID', required=True)
@click.option('-pki', '--pki', type=int, help='Certificate Type', required=True, default=0)
@click.option('-hsm', '--hsm', type=int, help='Use HSM', required=True, default=0)
@click.option('-uid', '--user_id', type=int, help='UserID')
@click.option('-e', '--email', type=str, help='Email')
def sign(input_file, output_file, api_token, tenant_id, pki, hsm=0, user_id=None, email=None):
    """Sign document"""
    logo = """
    +------------------------------+
    | Sign document by Paperlogic  |
    +------------------------------+
    """
    click.echo(f"Start Signing")
    sign_pplg(input_file, output_file, api_token, tenant_id, pki, hsm, user_id, email)
    click.echo(f"Complete Signing")
    click.echo(logo)

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-tk', '--api_token', type=str, help='API Token', required=True)
@click.option('-t', '--tenant_id', type=int, help='TenantID', required=True)
def timestamp(input_file, output_file, api_token, tenant_id):
    """Timestamp document"""
    logo = """
    +-----------------------------------+
    | Timestamp document by Paperlogic  |
    +-----------------------------------+
    """
    click.echo(f"Start Timestamp")
    timestamp_pplg(input_file, output_file, api_token, tenant_id)
    click.echo(f"Complete Timestamp")
    click.echo(logo)

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-tk', '--api_token', type=str, help='API Token', required=True)
@click.option('-t', '--tenant_id', type=int, help='TenantID', required=True)
@click.option('-pki', '--pki', type=int, help='Certificate Type', required=True, default=0)
@click.option('-uid', '--user_id', type=int, help='UserID')
@click.option('-e', '--email', type=str, help='Email')
def testsign(input_file, output_file, api_token, tenant_id, pki, user_id=None, email=None):
    """Test sign document"""
    logo = """
    +-----------------------------------+
    | Test sign document by Paperlogic  |
    +-----------------------------------+
    """
    click.echo(f"Start Signing")
    sign_test(input_file, output_file, api_token, tenant_id, pki, user_id, email)
    click.echo(f"Complete Signing")
    click.echo(logo)

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-tk', '--api_token', type=str, help='API Token', required=True)
@click.option('-t', '--tenant_id', type=int, help='TenantID', required=True)
def testtimestamp(input_file, output_file, api_token, tenant_id):
    """Test timestamp document"""
    logo = """
    +----------------------------------------+
    | Test timestamp document by Paperlogic  |
    +----------------------------------------+
    """
    click.echo(f"Start Timestamp")
    timestamp_test(input_file, output_file, api_token, tenant_id)
    click.echo(f"Complete Timestamp")
    click.echo(logo)