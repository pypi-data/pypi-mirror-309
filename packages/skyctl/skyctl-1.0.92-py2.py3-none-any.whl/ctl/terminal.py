# !/usr/bin/env python3
import configparser
import os
from typing import Optional
import re
import click
import requests
import file_config.upload as upload_file
import file_config.space as name_space


class User:
    def __init__(self, uid, username, password):
        self.uid = uid
        self.username = username
        self.password = password


_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help', '--usage'])


class _CustomClickCommand(click.Command):
    def get_help(self, ctx):
        help_str = ctx.command.help
        ctx.command.help = help_str.replace('.. code-block:: bash\n', '\b')
        return super().get_help(ctx)


# def abort_if_false(ctx, param, value):
#     if not value:
#         ctx.abort()


login_url_path = '/skyctl/namespace/list'
upload_url_path = '/skyctl/upload'
create_url_path = '/skyctl/namespace/create'
list_url_path = '/skyctl/namespace/list'

url_config = configparser.ConfigParser()
home = os.path.expanduser('~').replace('\\', '/')
dir_path = home + '/.skyctl'
current_path = os.path.abspath(os.path.dirname(__file__))
url_config.read(current_path + '/server_config.ini')
login_url = url_config['server']['login_url']
upload_url = url_config['server']['upload_url']
list_url = url_config['server']['list_url']
create_url = url_config['server']['create_url']


@click.group()
def login():
    """SkyCtl Login CLI."""
    pass


@login.command('login', help='Login to a effective server', context_settings=_CONTEXT_SETTINGS)
@click.option('--ip',
              '-i',
              prompt=True,
              help='ip to login')
@click.option('--port',
              '-p',
              prompt=True,
              help='port to login')
def login_server(ip, port):
    pat = check_key()
    if pat is not None:
        if not validate_ip(ip):
            click.echo('Invalid value for IP!')
            return
        if not validate_port(port):
            click.echo('Invalid value for port!')
            return
        url = "http://" + ip + ":" + port + login_url_path
        headers = {
            "X-UserId": pat,
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            click.echo('Login successful!')
            override_config(ip, port)
        elif response.status_code == 500:
            click.echo('The server is exist but something is wrong!')
        else:
            click.echo('Please use a effective server!' + response.text)


@click.group()
def upload():
    """SkyCtl Upload CLI."""
    pass


@upload.command('upload',
                help='Upload skypilot configuration file',
                cls=_CustomClickCommand,
                context_settings=_CONTEXT_SETTINGS)
@click.option('--space',
              '-s',
              help='Namespace for file upload. If omitted, files will be uploaded to the default namespace.',
              default='default',
              show_default=True,
              prompt='Enter the namespace for file upload (or leave blank for default)',
              type=str)
def file(space: Optional[str]):
    if not click.confirm(f'Are you sure want to upload to the "{space}" namespace?'):
        click.echo('Aborted by user.')
        return

    click.echo(f"Uploading files to namespace: '{space}'")
    pat = check_key()
    if pat is not None:
        upload_file.execute(pat, upload_url, space)


@click.group()
def namespace():
    """SkyCtl Namespace CLI."""
    pass


@namespace.command('namespace',
                   help='Operation of namespace',
                   context_settings=_CONTEXT_SETTINGS)
@click.option('--create',
              '-c',
              help='Create a namespace',
              type=str)
@click.option('--ls',
              '-l',
              is_flag=True,
              default=False,
              required=False,
              help='Show the namespace list')
def namespace_operation(create: Optional[str], ls: bool):
    pat = check_key()
    if pat is not None:
        if create:
            ls = False
            name_space.create(create_url, pat, create)

        if ls:
            name_space.get_list(list_url, pat)


def check_key():
    file_path = dir_path + '/pat.ini'
    if not os.path.exists(file_path):
        click.echo('No user authentication profile detected!')
        return None
    try:
        config = configparser.ConfigParser()
        # read `pat.ini`
        config.read(file_path)
        pat = config['CREDENTIALS']['X-UserId']

    except:
        click.echo('User profile error, please check and log in again!')
    else:
        return pat


def override_config(ip, port):
    __url_config = configparser.ConfigParser()
    __current_path = os.path.abspath(os.path.dirname(__file__))
    __url_config.read(__current_path + '/server_config.ini')
    __login_url = 'http://' + ip + ':' + port + login_url_path
    __upload_url = 'http://' + ip + ':' + port + upload_url_path
    __list_url = 'http://' + ip + ':' + port + list_url_path
    __create_url = 'http://' + ip + ':' + port + create_url_path
    __url_config.set('server', 'login_url', __login_url)
    __url_config.set('server', 'upload_url', __upload_url)
    __url_config.set('server', 'create_url', __create_url)
    __url_config.set('server', 'list_url', __list_url)
    with open(__current_path + '/server_config.ini', 'w') as file:
        __url_config.write(file)


def validate_ip(ip):
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if not ip_pattern.match(ip):
        return False
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)


def validate_port(port):
    port_pattern = re.compile(r'^\d+$')
    if not port_pattern.match(port):
        return False
    port_int = int(port)
    return 0 <= port_int <= 65535


cli = click.CommandCollection(sources=[login, upload, namespace])
cli.help = """
     *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *\n
     *  SkyCtl CLI Tool.                                                        *\n
\n
     *  This is the main entry point for the SkyCtl command line interface.     *\n
     *  It provides a set of commands to interact with the Skybackend server.   *\n
\n
     *  Before using any of the commands, you need to prepare a config file     *\n
     *  at `~/.skyctl/pat.ini` with the following format:                       *\n
     *      [CREDENTIALS]                                                       *\n
     *      X-UserId = your_user_id                                             *\n
\n
     *  You can find more information in the official github documentation.     *\n
     *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    """

if __name__ == '__main__':
    cli()
