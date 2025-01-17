# Fjaelllada firmware overview

> For convenience you can use the [justfile](https://github.com/casey/just)
> to run commands.  
> Run `just --list` for an command overview.

## Developing

1. Install [poetry](https://python-poetry.org/) on your machine
2. Install sytem dependencies: `apt install python3-pyscard libpcsclite-dev pcscd` 
3. Depending on your system it might be necessary to install the `swig` package for building the python dependencies
4. Install all python dependencies with `poetry install` or `just install`
5. Start developing

**Launching the project:** take a look at the [justfile](justfile).
Run `just seil-locker` to run the application for the upper locker locally
with an emulated card reader and gpio module.

#### Building
1. Before building: If you're making changes to the firmware, increment the version number
in [pyproject.toml](pyproject.toml) before building ([sematic versioning](https://semver.org/))
2. Run `just build` or `poetry build` to create a wheel. This can be found in the `dist` folder.

When installing the pip wheel, these two entrypoints get installed as scripts:
* `seil-locker`
* `depot-bay`  

Depending on which flavor is required, start one of the two in the `.xsession` file.

### Program settings
The Program is configured with environment variables, which are documented
in the following table:

| Variable                    | Default Value  | Description                                                                                             |
|-----------------------------| -------------- | ------------------------------------------------------------------------------------------------------- |
| SCREEN_RESOLUTION_WIDTH     | 480            | Width in px the UI should have on the screen                                                            |
| SCREEN_RESOLUTION_HEIGHT    | 320            | Height in px the UI should have on the screen                                                           |
| INPUT_PIN                   | 20             | GPIO pin on the RPi that is used to read the state of the door when running in `seil-locker` mode       |
| OUTPUT_PIN                  | 21             | GPIO pin on the RPi that is used to open  the door when running in `seil-locker` mode                   |
| TOTP_ISSUER                 | jdav-locker-v1 | Name of the TOTP issuer, this shows up as service name in the authenticator app. Set to something unique for each locker to avoid overwriting tokens in user's TOTP app when he is registered at both lockers. Right now the bay depot uses `jdav-locker-v1`. Upstairs will be `jdav-seilschrank`          |
| DEBUG_SIMULATE_CARD_READER  | ""             | set to `true` while developing. Fakes an attached card reader, returning the card ID `12345` every 2 seconds |
| DEBUG_SIMULATE_OUTPUT       | ""             | set to `true` while developing to fake GPIO drivers or an fake I²C Bus                                  |

### File and Database structure

##### admin_db.txt
Plain text file, where each line represents one admin:
Each Line is a pyOTP URI, containing Name and Secret of the TOTP access

##### card_db.txt
Plain text file, where each line represents one user:  
Each line has the following format: `<card_id>;<user_name>`  
`<card>` is an uppercase hexadecimal 8-digit string without leading `0x`.
The length might change with different cards.  
Example: valid: `ABCDEF12`, invalid: `0xabcdef12`  
`<user_name` is a string chosen when activating a card, used for identifaction in logs.
