# Nephele

[![releases](https://img.shields.io/github/v/release/george-lim/nephele)](https://github.com/george-lim/nephele/releases)
[![ci](https://github.com/george-lim/nephele/workflows/CI/badge.svg)](https://github.com/george-lim/nephele/actions)
[![codecov](https://codecov.io/gh/george-lim/nephele/branch/main/graph/badge.svg)](https://codecov.io/gh/george-lim/nephele)
[![license](https://img.shields.io/github/license/george-lim/nephele)](https://github.com/george-lim/nephele/blob/main/LICENSE)

## [Usage](#usage) | [Features](#features) | [CI/CD](#cicd)

Nephele is an AWS serverless application that hosts George's cloud-compatible side projects.

## Usage

Nephele is accessible through the [Telegram bot](https://t.me/NepheleBot).
Use the `/help` command to get the command list.

### Dependencies

```bash
npm install -g serverless
npm install
python3 -m pip install -r requirements-dev.txt
```

This installs Nephele and its dependencies. You will also need [Docker Desktop](https://www.docker.com/products/docker-desktop).

### Serverless Framework Pro

1. Create a Serverless Framework Pro account
2. Create a `serverless framework` app and link it with this project
3. Add the following parameter to each stage:

```yaml
TELEGRAM_BOT_API_TOKEN: <Telegram Bot API token>
```

### Deployment

```bash
sls login
sls deploy
```

This deploys Nephele on AWS. Ensure that Docker Desktop is running first before deploying.

## Features

[Epic Games Bot](https://github.com/george-lim/epic-games-bot-python), [Kijiji Bot](https://github.com/george-lim/kijiji-bot), and [TextNow Bot](https://github.com/george-lim/textnow-bot-python) are all integrated with Nephele. For automation, Nephele supports command scheduling so that any service can have its action performed periodically.

## CI/CD

### Codecov

You will need to authorize Codecov with your GitHub account in order to upload code coverage reports.

Follow the [Codecov GitHub Action](https://github.com/codecov/codecov-action) to see how to configure the action for private repositories.
