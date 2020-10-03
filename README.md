# Nephele

<!-- [START badges] -->
[![framework](https://img.shields.io/badge/framework-Serverless-brightgreen)](https://serverless.com)
[![provider](https://img.shields.io/badge/provider-AWS-brightgreen)](#)
[![nodejs](https://img.shields.io/badge/nodejs-12.x-blue)](#)
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

```
TELEGRAM_BOT_API_TOKEN: <Telegram Bot API token>
```

### Deployment
Execute script on the command line:

```bash
# Install dependencies
yarn global add serverless
yarn install

# Deploy application
sls login
sls deploy # -s prod
```

### Known Bugs
During deployment, you may encounter a configuration validation warning caused by a bug in the Safeguards plugin JSON Schema:

```bash
Configuration warning at 'custom.safeguards': should be object
```

**It is safe to ignore this warning** as the provided configuration for the Safeguards plugin is valid, according to the [plugin documentation](https://github.com/serverless/safeguards-plugin/#defining-policies).
<!-- [END getstarted] -->
