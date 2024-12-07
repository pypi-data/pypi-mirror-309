import click
import sys
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
@click.option('-uid', '--user_id', type=int, help='UserID')
@click.option('-e', '--email', type=str, help='Email')
@click.option(
    '-env', '--environment',
    type=click.Choice(['dev', 'stg', 'prod'], case_sensitive=False),
    default='stg',
    help='Environment to run the SDK (dev/stg/prod)'
)

def sign(input_file, output_file, api_token, tenant_id, pki, user_id=None, email=None, environment='stg'):
    """Sign document"""
    if environment == 'dev':
        click.echo("Development mode activated")
    elif environment == 'stg':
        click.echo("Staging mode activated")
    elif environment == 'prod':
        click.echo("Production mode activated")

    click.echo("Start Signing")

    res = sign_pplg(input_file, output_file, api_token, tenant_id, pki, user_id, email, environment)

    if res:
        click.echo("Document signed successfully")
        sys.exit(0)
    else:
        click.echo("Error: Failed to sign document", err=True)
        sys.exit(1)

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-tk', '--api_token', type=str, help='API Token', required=True)
@click.option('-t', '--tenant_id', type=int, help='TenantID', required=True)
@click.option(
    '-env', '--environment',
    type=click.Choice(['dev', 'stg', 'prod'], case_sensitive=False),
    default='stg',
    help='Environment to run the SDK (dev/stg/prod)'
)
def timestamp(input_file, output_file, api_token, tenant_id, environment='stg'):
    """Timestamp document"""
    if environment == 'dev':
        click.echo("Development mode activated")
    elif environment == 'stg':
        click.echo("Staging mode activated")
    elif environment == 'prod':
        click.echo("Production mode activated")

    click.echo(f"Start Timestamp")
    res = timestamp_pplg(input_file, output_file, api_token, tenant_id, environment)

    if res:
        click.echo(f"Document timestamp successfully")
        sys.exit(0)
    else:
        click.echo(f"Error: Failed to timestamp document", err=True)
        sys.exit(1)

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-tk', '--api_token', type=str, help='API Token', required=True)
@click.option('-t', '--tenant_id', type=int, help='TenantID', required=True)
@click.option('-pki', '--pki', type=int, help='Certificate Type', required=True, default=0)
@click.option('-uid', '--user_id', type=int, help='UserID')
@click.option('-e', '--email', type=str, help='Email')
@click.option(
    '-env', '--environment',
    type=click.Choice(['dev', 'stg', 'prod'], case_sensitive=False),
    default='stg',
    help='Environment to run the SDK (dev/stg/prod)'
)
def testsign(input_file, output_file, api_token, tenant_id, pki, user_id=None, email=None, environment='stg'):
    """Test sign document"""
    if environment == 'dev':
        click.echo("Development mode activated")
    elif environment == 'stg':
        click.echo("Staging mode activated")
    elif environment == 'prod':
        click.echo("Production mode activated")
    
    click.echo("Start Signing")

    res = sign_test(input_file, output_file, api_token, tenant_id, pki, user_id, email, environment)
    if res:
        click.echo(f"Document signed successfully")
        sys.exit(0)
    else:
        click.echo(f"Error: Failed to sign document", err=True)
        sys.exit(1)

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-tk', '--api_token', type=str, help='API Token', required=True)
@click.option('-t', '--tenant_id', type=int, help='TenantID', required=True)
@click.option(
    '-env', '--environment',
    type=click.Choice(['dev', 'stg', 'prod'], case_sensitive=False),
    default='stg',
    help='Environment to run the SDK (dev/stg/prod)'
)
def testtimestamp(input_file, output_file, api_token, tenant_id, environment='stg'):
    """Test timestamp document"""
    click.echo(f"Start Timestamp")
    
    res = timestamp_test(input_file, output_file, api_token, tenant_id, environment)

    if res:
        click.echo(f"Document timestamp successfully")
        sys.exit(0)
    else:
        click.echo(f"Error: Failed to timestamp document", err=True)
        sys.exit(1)