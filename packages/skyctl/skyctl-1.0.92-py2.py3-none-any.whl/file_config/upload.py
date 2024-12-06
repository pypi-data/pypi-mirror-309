#!/usr/bin/env python3
import os
import tarfile

import click
import requests
import configparser

home = os.path.expanduser('~').replace('\\', '/')

current_path = os.path.abspath(os.path.dirname(__file__))
upload_config = configparser.ConfigParser()
upload_config.read(current_path + '/file.ini')

aws = home + upload_config['file_path']['aws']
lam = home + upload_config['file_path']['lambda']
azure = home + upload_config['file_path']['azure']
# gcp = home + upload_config['file_path']['gcp']
ibm = home + upload_config['file_path']['ibm']
kube = home + upload_config['file_path']['kube']
oci = home + upload_config['file_path']['oci']
scp = home + upload_config['file_path']['scp']

dirs_to_tar = [aws, lam, azure, ibm, kube, oci, scp]

config_file = upload_config['file']['file_name']


def execute(pat, upload_url, namespace):
    headers = {
        "X-UserId": pat
    }
    up_success_file = []
    target_path = home + config_file
    with tarfile.open(target_path, 'w') as tar:
        for dir_name in dirs_to_tar:
            if os.path.exists(dir_name) and os.path.isdir(dir_name):
                items = os.listdir(dir_name)
                for item in items:
                    file_path = os.path.join(dir_name, item)
                    tar.add(file_path)
            else:
                up_success_file.append(dir_name)
    if len(up_success_file) == len(dirs_to_tar):
        click.echo('Configuration file does not exist, upload failed')
        return

    data = {'nameSpace': namespace}
    files = {'file': open(target_path, 'rb')}
    response = requests.post(upload_url, headers=headers, files=files, data=data)
    http_code = response.status_code
    if http_code == 404:
        click.echo("Code 404, this server is not alive, please login a effective server")
        return
    elif http_code != 200 and response.text == 'Invalid user ID':
        click.echo(
            f"Please check your config file `~/.skyctl/pat.ini` : \"code\": \"{str(http_code)}\", \"msg\": \"{response.text}\"")
        return
    elif http_code != 200 and response.text == 'User namespace does not exist':
        click.echo(f"Please create namespace: '{namespace}'")
        return
    elif http_code != 200:
        click.echo(f"Server error, \"code\": \"{str(http_code)}\", \"msg\": \"{response.text}\"")
        return
    else:
        click.echo('Upload success!')
