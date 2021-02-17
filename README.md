# Nephele

<!-- [START badges] -->
[![framework](https://img.shields.io/badge/framework-Serverless-brightgreen)](https://serverless.com)
[![provider](https://img.shields.io/badge/provider-AWS-brightgreen)](#)
[![python](https://img.shields.io/badge/python-3.8-blue)](#)
[![release](https://img.shields.io/github/v/release/george-lim/nephele)](https://github.com/george-lim/nephele/releases)
[![license](https://img.shields.io/github/license/george-lim/nephele)](https://github.com/george-lim/nephele/blob/master/LICENSE)
<!-- [END badges] -->

> Nephele is an AWS serverless application that hosts George's cloud-compatible side projects.

<!-- [START getstarted] -->
## Getting Started

### Serverless Framework Pro

1. Create a [Serverless Framework Pro](https://app.serverless.com) account
2. Add a new app from the dashboard and update the `org` and `app` fields in `serverless.yml`
3. Create a `prod` stage, and connect an AWS account to each stage
4. Add the following parameter to each stage:
```yaml
TELEGRAM_BOT_API_TOKEN: <Telegram Bot API token>
```

### Installation

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Execute script on the command line:
```bash
yarn global add serverless
yarn install
python3 -m pip install -r requirements-dev.txt
```

### Deployment

1. Ensure Docker Desktop is running
2. Execute script on the command line:
```bash
sls login
sls deploy
```

### Clean Up

Layer artifacts and webhook preferences are cached after the first deployment. You will need to clear cache when updating `requirements.txt` dependencies or changing the Telegram Bot API token.

Run `sls clean` to delete the cache directory.
<!-- [END getstarted] -->
