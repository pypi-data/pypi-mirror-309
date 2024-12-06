import logging
import subprocess
import sys

import click
from click import prompt

from models import Servers, UsbPorts
from . import handle_work, Group

logger = logging.getLogger(__name__)

#@handle_work
@click.group(name="group")
@click.argument("group_name")
@click.pass_context
def group_cli(ctx, group_name):
    """Группа команд для работы с группами."""
    ctx.obj['NAME'] = group_name  # Сохраняем значение параметра `name` в контексте




@handle_work
@group_cli.command()
@click.option('--name', help="Название группы.")
def start(name):
    """Приветствие пользователя с учетом возраста."""
    try:
        subprocess.run([ "HUB-CORE", "-b", "-c", "/usr/local/etc/virtualhere/groups/Test.ini"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Приветствие отправлено для пользователя: {name}, возраст: ")
        sys.exit()
    except Exception as e:
        logger.critical(e)
        sys.exit(1)


@group_cli.command()
@click.confirmation_option(prompt="Are you sure? Group will be reconfigured with selected params and restarted.")
@handle_work
@click.option('--usb', '-u', type=click.STRING, multiple=True, help="Virtual USB-порт. Может задаваться несколько раз.")
@click.option('--usb-action', type=click.Choice(['set','add','remove']), default='add', show_default=True, help="TCP-порт для подключения к базе данных.")
def conf(ctx, session, usb, usb_action):
    """Crонфигурировать сервер"""
    name = ctx.obj.get('NAME')  # Получаем значение `name` из контекста

    server = session.query(Servers).filter_by(name=name).first()
    if server is None:
        raise FileNotFoundError(f"Группа '{name}' не найдена.")


    if usb_action == "remove":
        for virtual_port in usb:
            port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
            if port is None:
                raise ValueError(f"USB with virtual port '{virtual_port}' doesnt exist ")
            if port.server_id == server.id:
                server.usb_ports.remove(port)
            else:
                raise ValueError(f"Server '{name}' doesnt have usb with virtual port {virtual_port}.'")
    elif usb_action == "add":
        for virtual_port in usb:
            port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
            if port is None:
                raise ValueError(f"USB with virtual port '{virtual_port}' doesnt exist ")
            if port.server_id is None or port.server_id == server.id:
                server.usb_ports.append(port)
            else:
                raise ValueError(f"USB with virtual port '{virtual_port}' already claimed.")
    elif usb_action == "set":
        new_ports = []
        for virtual_port in usb:
            port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
            if port is None:
                raise ValueError(f"USB with virtual port '{virtual_port}' doesnt exist ")
            if port.server_id is None or port.server_id == server.id:
                new_ports.append(port)
            else:
                raise ValueError(f"USB with virtual port '{virtual_port}' already claimed.")
        server.usb_ports = new_ports


    group = Group(server.name, server.tcp_port, server.usb_ports)
    click.secho(group)



@group_cli.command()
@handle_work
def show(ctx, session):
    """Текущая конфигурация сервера"""
    name = ctx.obj.get('NAME')  # Получаем значение `name` из контекста

    server = session.query(Servers).filter_by(name=name).first()
    if server is None:
        raise FileNotFoundError(f"Сервер '{name}' не найден.")

    group = Group(server.name, server.tcp_port, server.usb_ports)
    click.secho(group)
