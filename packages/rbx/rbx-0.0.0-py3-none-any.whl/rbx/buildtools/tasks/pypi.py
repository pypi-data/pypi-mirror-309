import subprocess
import click


@click.command()
def check():
    """Check Python package distribution manifest."""
    cmd = "check-manifest -v"
    subprocess.run(cmd, shell=True)


@click.command()
def build():
    """Build Python package distribution locally."""
    cmd = "python setup.py sdist bdist_wheel"
    subprocess.run(cmd, shell=True)


@click.command()
def upload():
    """Check, build, and upload Python package distribution to local PyPI."""
    cmd = "twine upload dist/* -r scoota-pypi"
    subprocess.run(cmd, shell=True)
