import logging
import subprocess
import time

import click
from typing import TYPE_CHECKING, Literal

from models import UsbPorts

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from commands import handle_work

logger = logging.getLogger(__name__)


@click.group(name="usb")
def usb_cli():
    """Группа команд для работы с USB-портами"""
    pass

@usb_cli.group(name="port")
@click.argument('virtual_port')
@click.pass_context
def port_cli(ctx, virtual_port):
    """Группа команд для работы с USB-портом"""
    ctx.obj['PORT'] = virtual_port

@port_cli.command()
@handle_work
def show(ctx, session):
    """Показать информацию о USB-порте"""
    virtual_port = ctx.obj.get('PORT')
    click.echo(virtual_port)

@port_cli.command()
@handle_work
def conf(ctx, session):
    """Настроить USB-порт"""
    virtual_port = ctx.obj.get('PORT')
    click.echo(virtual_port)

@port_cli.command()
@handle_work
def delete(ctx, session):
    """Удалить USB-порт"""
    virtual_port = ctx.obj.get('PORT')
    click.echo(virtual_port)

@port_cli.command()
@handle_work
def add(ctx, session):
    """Добавить USB-порт"""
    virtual_port = ctx.obj.get('PORT')
    click.echo(virtual_port)

@port_cli.group(name='power')
def port_cli_power():
    """Управление питанием USB-порта"""
    pass

@port_cli_power.command(name='on')
@handle_work
def port_cli_power_on(ctx, session: 'Session'):
    virtual_port = ctx.obj.get('PORT')
    usb_port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
    if usb_port:
        change_usb_power("on", usb_port.bus)
        click.echo(f"Питание {virtual_port} включено")
    else:
        raise FileNotFoundError(f"USB-port {virtual_port} doesnt exist!")

@port_cli_power.command(name='off')
@handle_work
def port_cli_power_off(ctx, session: 'Session'):
    virtual_port = ctx.obj.get('PORT')
    usb_port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
    if usb_port:
        change_usb_power("off", usb_port.bus)
        try:
            subprocess.run(
                [ "udevadm", "trigger", "--action=remove", f"/sys/bus/usb/devices/{usb_port.bus}/" ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        except:
            click.secho(f"Ошибка при очистке старой информации модулем udevadm. Вероятнее всего порт уже выключен.", fg="red")
        click.echo(f"Питание {virtual_port} включено")
    else:
        raise FileNotFoundError(f"USB-port {virtual_port} doesnt exist!")

@port_cli_power.command(name='restart')
@handle_work
def port_cli_power_restart(ctx, session: 'Session'):
    virtual_port = ctx.obj.get('PORT')
    usb_port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
    if usb_port:
        change_usb_power("off", usb_port.bus)
        try:
            subprocess.run(
                [ "udevadm", "trigger", "--action=remove", f"/sys/bus/usb/devices/{usb_port.bus}/" ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        except:
            click.secho(f"Ошибка при очистке старой информации модулем udevadm. Вероятнее всего порт уже выключен.",
                        fg="red")

        time.sleep(2)
        change_usb_power("on", usb_port.bus)
        click.echo(f"Питание {virtual_port} включено")
    else:
        raise FileNotFoundError(f"USB-port {virtual_port} doesnt exist!")


def change_usb_power(state: Literal["on", "off", "cycle"], bus):
    location, port = bus.rsplit('.', 1)[ 0 ], bus.rsplit('.', 1)[ 1 ]

    result = subprocess.run(
        [ "uhubctl", "-f", "-l", location, "-p", port, "-a", str(state) ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    click.echo(f"Результат для {location}, порт {port}:\n{result.stdout}")

@usb_cli.group(name="show")
@handle_work
def global_show(ctx, session):
    """Show all USB-ports"""
    pass

@usb_cli.group(name="conf")
@click.pass_context
def global_conf(ctx):
    """Global configuration"""
    pass
