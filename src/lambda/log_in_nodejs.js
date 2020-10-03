const epicGames = require('epic-games-bot');
const shlex = require('shlex');
const textnow = require('textnow-bot');
const { replyMessage, replyPhoto } = require('../common/actions');
const { SCREENSHOT_PATH, execute } = require('../common/puppeteer');

const { EPIC_GAMES_SERVICE_NAME, TEXTNOW_SERVICE_NAME } = process.env;

module.exports.handler = async event => {
  const interface = event.interface;
  let args = null;
  let serviceLogIn = null;
  let user = {};

  try {
    args = shlex.split(event.command).slice(1);
  }
  catch (error) {
    await replyMessage(interface, 'Failed to parse input.');
    throw error;
  }

  if (event.serviceName == EPIC_GAMES_SERVICE_NAME) {
    serviceLogIn = epicGames.logIn;
  }
  else if (event.serviceName == TEXTNOW_SERVICE_NAME) {
    serviceLogIn = textnow.logIn;
  }
  else {
    throw new Error('Unknown service name');
  }

  if (args.length < 2) {
    await replyMessage(interface, 'Please provide a username, password, and 2FA code (if required).');
    throw new Error('Missing account info');
  }

  await replyMessage(interface, 'Logging in...');

  try {
    const bot = async (page, client) => await serviceLogIn(page, client, ...args);
    user.cookies = await execute(bot);
  }
  catch (error) {
    await replyPhoto(interface, SCREENSHOT_PATH);
    await replyMessage(interface, 'Failed to log in - input may be invalid.');
    throw error;
  }

  await replyMessage(interface, 'Successfully logged in!');
  return user;
};
