import sys
import tomllib
import click
from flask import Flask
from flask.cli import FlaskGroup
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from flask_sqlalchemy import SQLAlchemy
import os


title = '''


    ███████╗██████╗  ██████╗ ██╗     ██╗ ██████╗     ██████╗██╗     ██╗
    ██╔════╝██╔══██╗██╔═══██╗██║     ██║██╔════╝    ██╔════╝██║     ██║
    █████╗  ██████╔╝██║   ██║██║     ██║██║         ██║     ██║     ██║
    ██╔══╝  ██╔══██╗██║   ██║██║     ██║██║         ██║     ██║     ██║
    ██║     ██║  ██║╚██████╔╝███████╗██║╚██████╗    ╚██████╗███████╗██║
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝     ╚═════╝╚══════╝╚═╝
                                                                       

''' 


class Base(MappedAsDataclass, DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)


def ensure_configuration_availability(instance_path: str) -> str:
    """Ensure the availability of configuration file optionally set fron environment variable PROFILE at given path."""
    if not os.path.exists(instance_path):
        try:
            os.makedirs(instance_path)
        except Exception as e:
            click.echo(click.style(f"Cannot create instance directory.\n{str(e)}", fg='red', bold=True))
            sys.exit()
    profile = os.getenv('PROFILE', 'Deployment')
    abs_config_path = os.path.join(instance_path, profile+'.toml')
    if not os.path.exists(abs_config_path):
        click.echo(click.style(f"The configuration file '{profile}.toml' is missing at {instance_path}. ", fg='red', bold=True), nl=False)
        click.echo(click.style("Provide explicit configuration file to run application.", underline=True, fg='red', bold=True))
        sys.exit()
    return profile+'.toml'


def make_app() -> Flask:
    application = Flask(__name__, instance_relative_config=True)
    config_file = ensure_configuration_availability(application.instance_path)
    application.config.from_file(config_file, load=tomllib.load, text=False)

    import frolicapp.cli as cli
    application.cli.add_command(cli.test)
    application.cli.add_command(cli.create)
    application.cli.add_command(cli.clean)
    application.cli.add_command(cli.mock)

    db.init_app(application)

    from .blueprints import admin
    application.register_blueprint(admin.bp)

    click.echo(click.style(title, fg='bright_cyan'))
    return application


@click.group(cls=FlaskGroup, create_app=make_app)
def cli() -> None:
    """The CLI to manage frolic webserver."""