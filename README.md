# Nephele

[![releases](https://img.shields.io/github/v/release/george-lim/nephele)](https://github.com/george-lim/nephele/releases)
[![ci](https://github.com/george-lim/nephele/workflows/CI/badge.svg)](https://github.com/george-lim/nephele/actions)
[![license](https://img.shields.io/github/license/george-lim/nephele)](https://github.com/george-lim/nephele/blob/main/LICENSE)

[![banner](https://user-images.githubusercontent.com/21700768/110575939-cabfa200-812d-11eb-9e68-60fbfd0116fa.png)](https://t.me/NepheleBot)

## [Usage](#usage) | [Features](#features)

Nephele is an AWS serverless application that hosts George's cloud-compatible side projects.

## Usage

Nephele is accessible through the [Telegram bot](https://t.me/NepheleBot).
Use the `/help` command to get the command list.

### Dependencies

```bash
npm install -g serverless
npm install
```

This installs Nephele and its dependencies.

### Serverless Framework Pro

1. Create a Serverless Framework Pro account
2. Create a `serverless framework` app and link it with this project
3. Add the following parameter to each stage:

```yaml
telegramBotApiToken: <token>
```

### Deployment

```bash
sls login
sls deploy
```

This deploys Nephele on AWS.

## Features

Nephele allows you to receive notifications for offers on Epic Games Store, schedule an event to periodically repost Kijiji ads, or schedule an event to periodically send a SMS message.
