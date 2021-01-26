# Colony CLI

[![Coverage Status](https://coveralls.io/repos/github/QualiSystemsLab/colony-cli/badge.svg?branch=master)](https://coveralls.io/github/QualiSystemsLab/colony-cli?branch=master)
[![CI](https://github.com/QualiSystemsLab/colony-cli/workflows/CI/badge.svg)](https://github.com/QualiSystemsLab/colony-cli/actions?query=workflow%3ACI)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![PyPI version](https://badge.fury.io/py/colony-cli.svg)](https://badge.fury.io/py/colony-cli)
[![Maintainability](https://api.codeclimate.com/v1/badges/5a9f730163de9b6231e6/maintainability)](https://codeclimate.com/github/QualiSystemsLab/colony-cli/maintainability)


---

![quali](quali.png)

## Cloudshell Colony CLI

Colony CLI is a command line interface tool for CloudShell Colony.

The main functionality this tool currently provides is validation of Colony blueprints and launching sandbox environments from main and development branches.

## Why use Colony CLI

When developing blueprints for Colony, it can be very helpful to immediately check your work for errors.

Let's assume you are currently working in *development* branch, and you also have a main branch which is connected
to a Colony space. You would like to be sure that your latest committed changes haven't broken anything before merging them to
the main branch.

This is where this tool might be handy for you. Instead of reconnecting Colony to your development branch in UI or "merge and pray" you can
use Colony CLI to validate your current blueprints state and even launch sandboxes from them.

## Installing

You can install Colony CLI with [pip](https://pip.pypa.io/en/stable/):

`$ python -m pip install colony-cli`

Or if you want to install it for your user:

`$ python -m pip install --user colony-cli`

### Configuration

First of all you need to generate an access token. In the Colony UI navigate to Settings (in your space) -> Integrations -> click “Connect” under any of the CI tools -> click “New Token” to get an API token.
Then, you need to configure Colony CLI with the generated token and the colony space you are going to access.
There are three ways how to do it:

* Create a configuration file ~/.colony/config where you can have several profiles:

```bash
[default]
token = xxxyyyzzz
space = DemoSpace

[user]
token = aaabbbccc
space = TestSpace
```


* Set environment variables:

```bash
export COLONY_TOKEN = xxxzzzyyy
export COLONY_SPACE = demo_space
```

* Specify _--space_ and _--token_ options as part of the command:

`$ colony --space=trial --token=xxxyyyzzz <command>`



## Basic Usage

Colony CLI currently allows you to make two actions:

- validate blueprint (using `colony bp validate` command)
- start sandbox (via `colony sb start`)

In order to get help run:

`$ colony --help`

It will give you detailed output with usage:

```bash
$ colony --help
Usage: colony ( [(--space=<space> --token=<token>)] | [--profile=<profile>] ) [--help] [--debug]
              <command> [<args>...]

Options:
  -h --help             Show this screen.
  --space=<space>       Colony Space name
  --token=<token>       Specify token generated by Colony
  --profile=<profile>   Profile indicates a section in config file.
                        If set neither --token or --space must not be specified.

Commands:
    bp, blueprint       validate colony blueprints
    sb, sandbox         start sandbox
```

You can get additional help information for a particular command by specifying *--help* flag after command name, like:

```colony sb --help
    usage:
        colony (sb | sandbox) start <blueprint_name> [options]
        colony (sb | sandbox) status <sandbox_id>
        colony (sb | sandbox) end <sandbox_id>
        colony (sb | sandbox) [--help]

    options:
       -h --help                        Show this message
       -d, --duration <minutes>         Sandbox will automatically deprovision at the end of the provided duration
       -n, --name <sandbox_name>        Provide name of Sandbox. If not set, the name will be generated using timestamp

       -i, --inputs <input_params>      Comma separated list of input parameters. Example: key1=value1, key2=value2.
                                        By default Colony CLI will try to take default values for inputs from blueprint
                                        definition yaml file (if you are inside a git-enabled folder of blueprint repo).
                                        Use this option to override them.

       -a, --artifacts <artifacts>      Comma separated list of artifacts with paths where artifacts are defined per
                                        application. The artifact name is the name of the application.
                                        Example: appName1=path1, appName2=path2.
                                        By default Colony CLI will try to take artifacts from blueprint definition yaml
                                        file (if you are inside a git-enabled folder of blueprint repo).
                                        Use this option to override them.

       -b, --branch <branch>            Specify the name of remote git branch. If not provided, we will try to
                                        automatically detect the current working branch if the command is used in a
                                        git enabled folder.

       -c, --commit <commitId>          Specify commit ID. It's required to run sandbox from a blueprint from an
                                        historic commit. Must be used together with the branch option.
                                        If not specified then the latest commit will be used

       -w, --wait <timeout>             Set the timeout in minutes for the sandbox to become active. If not set, command
                                        will not block terminal and just return the ID of started sandbox
```

### Blueprint validation

* If you are currently inside a git-enabled folder containing your blueprint, commit and push your latest changes and run (Colony CLI will automatically detect the current working branch):

    `$ colony bp validate MyBlueprint`

* If you want to validate a blueprint from another branch you can specify _--branch_ argument or even check validation in a
specific point in time by setting _--commit_:

    `$ colony bp validate MyBlueprint --branch dev --commit fb88a5e3275q5d54697cff82a160a29885dfed24`

---
**NOTE**

If you are not it git-enabled folder of your blueprint repo and haven't set --branch/--commit arguments tool will
validate blueprint with name "MyBlueprint" from branch currently attached to your Colony space.

---

If blueprint is valid you will get output with "Valid" message. If no, it will print you a table with found errors.

**Example:**

```bash
$colony blueprint validate Jenkins -b master

ERROR - colony.commands - Validation failed
message                                                                      name
---------------------------------------------------------------------------  -------------------------------
Cloud account: AWS is not recognized as a valid cloud account in this space  Blueprint unknown cloud account
```

### Launching sandbox

* Similar to the previous command you can omit *--branch/--commit* arguments if you are in a git-enabled folder of your
  blueprint repo:

    `$ colony sb start MyBlueprint`

* This will create a sandbox from the specified blueprint

* If you want to start a sandbox from a blueprint in a specific state, specify _--branch_ and _--commit_ arguments:

    `$ colony sb start MyBlueprint --branch dev --commit fb88a5e3275q5d54697cff82a160a29885dfed24`

* Additional optional options that you can provide here are:
  * `-d, --duration <minutes>` - you can specify duration for the sandbox environment in minutes. Default is 120 minutes
  * `-n, --name <sandbox_name>` - the name of sandbox you want to create. By default it will generate name using blueprint name + current timestamp
  * `-i, --inputs <input_params>` - comma-separated list of input parameters for sandbox, like: _"param1=val1, param2=val2_"
  * `-a, --artifacts <artifacts>` - comma-separated list of sandbox artifacts, like: "_app1=path1, app2=path2_"
  * `-w, --wait <timeout>` - <timeout> is a number of minutes. If set, you Colony CLI will wait for sandbox to become active and lock your terminal.
---
**NOTE**

1. If you are not it git-enabled folder of your blueprint repo and haven't set --branch/--commit arguments tool will
start sandbox using blueprint with name "MyBlueprint" from branch currently attached to your Colony space.

2. If you omit artifacts and inputs options, you are inside a git enabled folder and the local is in sync with remote,
then Colony Cli will try to get default values for artifacts and inputs from the blueprint yaml.
---

Result of the command is a Sandbox ID.

**Example**:

```bash
colony sb start MyBlueprint --inputs "CS_COLONY_TOKEN=ABCD, IAM_ROLE=s3access-profile, BUCKET_NAME=abc"

ybufpamyok03c11
```

### Other functionality

You can also end colony sandbox knowing its Id with command:

`$ colony sb end <sandbox> id`

To get current sandbox status run:

`$ colony sb status <sandbox> id`


## Troubleshooting and Help

To troubleshoot what Colony CLI is doing you can add _--debug_ to get additional information.

For questions, bug reports or feature requests, please refer to the [Issue Tracker](https://github.com/QualiSystemsLab/colony-cli/issues).


## Contributing


All your contributions are welcomed and encouraged. We've compiled detailed information about:

* [Contributing](.github/contributing.md)


## License
[Apache License 2.0](https://github.com/QualiSystems/shellfoundry/blob/master/LICENSE)
