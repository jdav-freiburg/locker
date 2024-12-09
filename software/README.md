# Fjaelllada firmware overview

> For convenience you can use the [justfile](https://github.com/casey/just)
> to run commands.  
> Run `just --list` for an command overview.

## Developing

1. Install [poetry](https://python-poetry.org/) on your machine
2. Install sytem dependencies: `apt install python3-pyscard libpcsclite-dev pcscd` 
3. Install all python dependencies with `poetry install` or `just install`

Launching the project: take a look at the [justfile](justfile).
Run `just run-seil` to run the application for the upper locker locally
with an emulated card reader and gpio module.

## Deploying
0. Install sytem dependencies: `apt install python3-pyscard libpcsclite-dev pcscd` 
1. run `just build` or `poetry build`
2. copy the wheel file to the raspberry pi
3. Install the wheel using `pip`
4. Copy `.xsession` over. This does autostarting the script

### Programm settings
_todo_: Document all relevant CLI flasgs or env variables

### File and Database structure
_todo_: Document how the database files are stored, locked and backupped
