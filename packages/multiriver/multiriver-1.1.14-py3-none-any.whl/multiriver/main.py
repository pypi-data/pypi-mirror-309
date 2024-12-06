# azure_cli.py

import click
from .azure_blob_session import (
    get_blob_service_client,
    list_blobs_in_container
)
from .utils import process_data, liberal_format
from .click_utils import (
    save_credentials,
    save_source_configuration
)

from .rivery_session import RiverySession
from .click_utils import load_credentials, load_source_configuration
from copy import deepcopy
from . import utils  # Assuming utils.py contains generate_rivers_template
from rich.table import Table
from rich.live import Live

RETRY_MAPPING_MAX = 5

DONE_STATUS = "Done"

SAVING_THE_RIVER_STATUS = "Saving the river..."

GENERATING_MAPPING_STATUS = "Generating mapping..."

RETRYING_MAPPING_STATUS = "Retrying to generate mapping..."

MAPPING_ERRORS_STATUS = "Mapping failed with error: {errors}"


@click.group()
def cli():
    """CLI tool to interact with Azure Blob Storage."""
    pass

@cli.command()
def show_creds_config():
    """
    Show the current credentials configuration.
    """
    creds = load_credentials()
    if not creds:
        click.echo("No credentials found. Please configure the credentials.")
        return

    click.echo("\nCurrent Credentials Configuration:")
    for key, value in creds.items():
        click.echo(f"  {key}: {value}")
    click.echo()

@cli.command()
@click.option('--account-name', required=False, help='Azure Storage account name')
@click.option('--account-key', required=False, help='Azure Storage account key')
@click.option('--connection-string', required=False, help='Azure Storage connection string')
@click.option('--sas-token', required=False, help='Shared Access Signature (SAS) token')
@click.option('--rivery-api-token', required=False, help='Rivery API token')
@click.option('--rivery-host', required=False, help='Rivery host to use. The default value is: https://console.rivery.io',
              default='https://console.rivery.io')
def configure_creds(account_name, account_key, connection_string, sas_token, rivery_api_token, rivery_host):
    """
    Configure and store Azure Storage and Rivery API credentials.
    """
    if not any([account_name, account_key, connection_string, sas_token, rivery_api_token, rivery_host]):
        click.echo("Error: Please provide at least one credential option to configure.")
        return

    save_credentials(account_name, account_key, connection_string, sas_token, rivery_api_token, rivery_host)

@cli.command()
@click.option('--container-name', required=False, help='Container name') # todo can be taken from the template river
@click.option('--prefix', required=False, help='Prefix to filter blobs')
@click.option('--template-river-id', required=False, help='The base template river to populate rivers')
@click.option('--filename-template', required=False, help='The template used in populated river')
@click.option('--group-id', required=True, help='The id of the group to attach the rivers to')
@click.option('--cron-schedule', required=False, help='The cron config to schedule new river')
@click.option('--merge-keys', required=False,
              help='The merge keys to use in the river. Comma separated list (e.g. "key1,key2").')
def configure_source(container_name, prefix, template_river_id, filename_template, group_id, cron_schedule, merge_keys):
    """
    Configure and store source settings for Azure Blob Storage.
    If 'filename-template' is provided, generate river templates based on the blob names.
    """

    if not any([container_name, prefix, template_river_id, filename_template, cron_schedule, merge_keys]):
        click.echo("Please provide at least one config with the group.")

    source_config = {
        'container_name': container_name,
        'prefix': prefix,
        'template_river_id': template_river_id,
        'filename_template': filename_template,
        'group_id': group_id,
        'cron_schedule': cron_schedule,
        'merge_keys': merge_keys.split(',') if merge_keys else []
    }
    save_source_configuration(**source_config)

    # If filename_template is provided, generate river templates
    if filename_template:
        # Get the BlobServiceClient
        blob_service_client = get_blob_service_client()
        if not blob_service_client:
            return

        # List blobs with the specified prefix
        source_config = load_source_configuration(group_id)
        blob_names = list_blobs_in_container(
            blob_service_client,
            source_config.get('container_name'),
            source_config.get('prefix')
        )
        if not blob_names:
            click.echo("No blobs found to generate river templates.")
            return

        # Generate river templates using utils.generate_rivers_template
        generated_templates = utils.generate_rivers_template(filename_template, blob_names)

        # Log the first 10 generated templates
        click.echo("\nGenerated River Templates (showing up to 10):")
        for i, template in enumerate(generated_templates[:10], start=1):
            click.echo(f"{i}. {template}")

        total_templates = len(generated_templates)
        if total_templates > 10:
            click.echo(f"...and {total_templates - 10} more templates.")
        click.echo(f"\nTotal number of templates generated: {total_templates}")
        save_source_configuration(**{'generated_templates': generated_templates, 'group_id': group_id})

    # Save the source configuration (including generated templates if any)

def generate_table(group_id: str, table_data: list):
    """
    Generate a rich table with the provided data.
    """
    table = Table(title=f"Generating Rivers for Group ID: {group_id}.")
    table.add_column("River Name", style="cyan", no_wrap=True)
    table.add_column("Target Table Name", style="green")
    table.add_column("Status", style="magenta")
    table.add_column("River URL", style="green")

    for row in table_data:
        table.add_row(row["new_river_name"], row["target_table_name"], row["status"], row["river_url"])

    return table

@cli.command()
@click.option('--group-id', required=True, help='The id of the group to attach the rivers to')
def populate_rivers(group_id):
    """
    Populate rivers based on the source configuration.
    """
    creds = load_credentials()
    source_config = load_source_configuration(group_id)
    if not source_config:
        click.echo(f"The source is not configured for the provided group id: {group_id}.")
        return

    rivery_token = creds.get('rivery_api_token')
    rivery_host = creds.get('rivery_host')

    template_river_id = source_config.get('template_river_id')
    generated_templates = source_config.get('generated_templates')
    cron_schedule = source_config.get('cron_schedule')
    merge_keys = source_config.get('merge_keys')

    if not rivery_token:
        click.echo("Error: Rivery API token is missing. Please configure the credentials.")
        return

    if not template_river_id:
        click.echo("Error: Template river ID is missing. Please configure the source settings.")
        return

    if not generated_templates:
        click.echo("Error: No generated templates found. Please configure the source settings.")
        return

    if not cron_schedule:
        click.echo("Cron schedule is missing. Rivers will be created but not scheduled.")

    rivery_session = RiverySession(token=rivery_token, host=rivery_host)
    template_river = rivery_session.get_river(
        **{"river_id": template_river_id}
    )
    template_river = process_data(
        template_river,
        convert_to_oi=['connection_id', 'fz_connection', 'env_id'],
        to_delete=['river_date_updated', 'version_id', 'river_date_inserted', 'cross_id'],
        to_date=['start_date'],
    )

    table_data = []
    new_river_objects = _generate_new_rivers_objects(generated_templates, group_id,
                                                     table_data, template_river)

    with Live(generate_table(group_id, table_data), refresh_per_second=4) as live:
        initiate_mapping_objects = {}
        river_title_id_map = {}

        for table_row in table_data:
            current_river_name = table_row["new_river_name"]

            saved_river_data = rivery_session.save_river(data=new_river_objects[current_river_name])
            river_id = str(saved_river_data.get('_id'))
            new_river_objects[current_river_name] = saved_river_data

            table_row['river_url'] = '/'.join(
                [rivery_session.host, 'river', str(saved_river_data['river_definitions']['account']),
                 str(saved_river_data['river_definitions']['env_id']), 'river', river_id]
            ) + '/'

            river_title_id_map[current_river_name] = river_id

            table_row["status"] = GENERATING_MAPPING_STATUS
            live.update(generate_table(group_id, table_data))

            initiate_mapping_objects[current_river_name] = rivery_session.generate_mapping(
                river_id=river_id, data=saved_river_data
            )

        retry_count_per_river = {}
        mapping_done = set()
        while len(mapping_done) < len(table_data):
            for table_row in table_data:
                current_river_name = table_row["new_river_name"]
                river_id = river_title_id_map[current_river_name]
                if river_id in mapping_done:
                    continue

                if table_row['status'] or table_row['status'].startswith(RETRYING_MAPPING_STATUS):

                    mapping, errors = rivery_session.pull_river_mapping(
                        mapping_data=initiate_mapping_objects[current_river_name]
                    )
                    if errors and retry_count_per_river.get(current_river_name, 0) < RETRY_MAPPING_MAX:
                        # error happened for the first time, doing a retry
                        initiate_mapping_objects[current_river_name] = rivery_session.generate_mapping(
                            river_id=river_id, data=new_river_objects[current_river_name]
                        )
                        retry_count_per_river[current_river_name] = retry_count_per_river.get(current_river_name, 0) + 1
                        table_row["status"] = RETRYING_MAPPING_STATUS +  f" Number of retries: {retry_count_per_river.get(current_river_name, 0)}"
                    elif errors:
                        table_row["status"] = MAPPING_ERRORS_STATUS.format(
                            errors=errors
                        ) + f"Number of retries: {retry_count_per_river.get(current_river_name, 0)}"
                        mapping_done.add(river_id)
                    elif mapping:
                        table_row["status"] = SAVING_THE_RIVER_STATUS
                        _save_river_mapping(mapping, new_river_objects[current_river_name],
                                            river_id, rivery_session, merge_keys)
                        table_row["status"] = DONE_STATUS
                        mapping_done.add(river_id)

                live.update(generate_table(group_id, table_data))

    logic_river_name = f"Logic Step {group_id}"
    saved_logic_river = rivery_session.create_logic_river(
        river_ids=list(river_title_id_map.values()),
        group_id=group_id,
        cron_schedule=cron_schedule,
        logic_river_name=logic_river_name
    )
    logic_river_url = '/'.join(
        [rivery_session.host, 'river', str(saved_logic_river['river_definitions']['account']),
         str(saved_logic_river['river_definitions']['env_id']), 'river', river_id]
    ) + '/'
    click.echo(f"Logic river created with the name: {logic_river_name} and the URL: {logic_river_url}")

@cli.command()
@click.option('--group-id', required=True, help='The id of the group to attach the rivers to')
def delete_rivers(group_id):
    """
    Delete all rivers for the provided group id.
    """
    creds = load_credentials()
    source_config = load_source_configuration(group_id)
    if not source_config:
        click.echo(f"The source is not configured for the provided group id: {group_id}.")
        return

    rivery_token = creds.get('rivery_api_token')
    rivery_host = creds.get('rivery_host')
    rivery_session = RiverySession(token=rivery_token, host=rivery_host)

    rivers_list = rivery_session.list_rivers(group_id=group_id)

    with click.progressbar(range(len(rivers_list)), label=f'Deleting rivers for the group {group_id}') as bar:
        for i in bar:
            rivery_session.delete_river(data={"_id": rivers_list[i].get('_id')})

    click.echo(f"Deleted all rivers for group id: {group_id}.")

def _save_river_mapping(mapping: list, new_river_data: dict, river_id: str, rivery_session: RiverySession,
                        merge_keys: list):
    """
    Save the mapping to the river.
    :param mapping: The mapping to save.
    :param new_river_data: The new river data.
    :param river_id: The river id.
    :param rivery_session: The Rivery session.
    """
    for col in mapping['target']:
        if {col.get('name').lower(), col.get('fieldName').lower()} & set(merge_keys):
            col['isKey'] = True

    new_river_data['tasks_definitions'][1]['task_config']["file_columns"] = mapping['target']
    new_river_data['tasks_definitions'][1]['task_config']["source_mapping"] = mapping['source']
    payload = {
        "river_definitions": new_river_data.get("river_definitions"),
        "tasks_definitions": new_river_data.get("tasks_definitions"),
        "cross_id": {"$oid": river_id},
        "_id": {"$oid": river_id}
    }
    rivery_session.save_river(
        river_id=river_id,
        data=payload
    )


def _generate_new_rivers_objects(generated_templates: list, group_id: str, table_data: list, template_river: dict):
    """
    Generate new river objects based on the generated templates.
    :param generated_templates: The generated templates.
    :param group_id: The group id.
    :param table_data: The table data.
    :param template_river: The template river.
    :return: The new river objects.
    """
    new_river_objects = {}

    template_target_table = template_river['tasks_definitions'][1]['task_config']['target_table']
    for i, gen_template in enumerate(generated_templates):
        new_river_name = f'new river {i} - {gen_template["template"]}'
        new_river_target_table = liberal_format(template_target_table, entity_name=gen_template["entity_name"])
        new_river_structure = process_data(
            deepcopy(template_river),
            to_replace={
                'group_id': {"_id": {"$oid":group_id}},
                'file_pattern': gen_template['template'],
                'river_name': new_river_name,
                'target_table': new_river_target_table
            }
        )
        new_river_structure['tasks_definitions'][0]['task_config']["temp_folder_to_run"] = gen_template['template']
        new_river_objects[new_river_name] = {

            'river_definitions': new_river_structure.get('river_definitions'),
            'tasks_definitions': new_river_structure.get('tasks_definitions')

        }
        table_data.append({
            "new_river_name": new_river_name,
            "target_table_name":new_river_target_table,
            "status": "Creating river...",
            "river_url": "N/A"
        })
    return new_river_objects


@cli.command()
def list_source_configs():
    """
    List all source configurations.
    """
    source_configs = load_source_configuration()
    if not source_configs:
        click.echo("No source configurations found.")
        return

    click.echo("\nSource Configurations:")
    for group_id, source_config in source_configs.items():
        click.echo(f"Group ID: {group_id}")
        for key, value in source_config.items():
            click.echo(f"  {key}: {value}")
        click.echo()



def main():
    # populate_rivers("6720e1592f775cb9fcdbf026")
    cli()

if __name__ == '__main__':
    main()