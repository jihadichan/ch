import hashlib

import click


def exitWithError(errorMessage: str):
    click.secho(f"{errorMessage}", fg="red")
    exit(1)


def exitWithException(errorMessage: str, exception: Exception):
    click.secho(f"{exception}", fg="red")
    click.secho(f"{errorMessage}", fg="red")
    exit(1)


def printInfo(message: str):
    click.secho(f"{message}", fg="yellow")


def hashHanzi(hanziAsString: str, length: int = 3) -> str:
    return hashlib.shake_256(hanziAsString.encode()).hexdigest(length)


def hanziToUnicode(hanzi: str) -> str:
    return hex(ord(hanzi))[2:]
