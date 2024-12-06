import click

from .tasks import apprunner, ec2, image, misc, pypi


from rbx import __version__


@click.group(
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
    add_help_option=True,
)
@click.version_option(message=__version__)
def cli():
    """Scoota (a.k.a. RBX) buildtools."""


cli.add_command(ec2.deploy)


@cli.group(name="apprunner")
def apprunner_group():
    """Manage AppRunner Applications."""


apprunner_group.add_command(apprunner.submit)
apprunner_group.add_command(apprunner.deploy)


@cli.group(name="image")
def image_group():
    """Manage images on Amazon Container Registry."""


image_group.add_command(image.login)
image_group.add_command(image.build)
image_group.add_command(image.upload)


@cli.group(name="misc")
def misc_group():
    """Miscellaneous tools."""


misc_group.add_command(misc.clean)
misc_group.add_command(misc.get_next_tag)
misc_group.add_command(misc.get_merge_desc)
misc_group.add_command(misc.get_npm_version)


@cli.group(name="pypi")
def pypi_group():
    """PyPI tools."""


pypi_group.add_command(pypi.check)
pypi_group.add_command(pypi.build)
pypi_group.add_command(pypi.upload)
