const shlex = require('shlex');
const textnow = require('textnow-bot');
const { replyMessage, replyPhoto } = require('../../common/actions');
const { SCREENSHOT_PATH, execute } = require('../../common/puppeteer');

module.exports.handler = async event => {
  const interface = event.interface;
  const user = event.dynamodb.Item;
  let args = null;

  try {
    args = shlex.split(event.command).slice(1);
  }
  catch (error) {
    await replyMessage(interface, 'Failed to parse input.');
    throw error;
  }

  if (!user.cookies) {
    await replyMessage(interface, 'Please log into TextNow first.');
    throw new Error('Missing login cookies');
  }

  if (args.length < 2) {
    await replyMessage(interface, 'Please provide a recipient and message.');
    throw new Error('Missing recipient / message info');
  }

  await replyMessage(interface, 'Sending message...');

  try {
    const [recipient, ...messageArgs] = args;
    const message = messageArgs.join(' ');

    const bot = async (page, client) => {
      await textnow.logIn(page, client);
      await textnow.selectConversation(page, recipient);
      await textnow.sendMessage(page, message);

      const cookies = (await client.send('Network.getAllCookies')).cookies;
      return cookies;
    };

    user.cookies = await execute(bot, user.cookies);
  }
  catch (error) {
    await replyPhoto(interface, SCREENSHOT_PATH);
    await replyMessage(interface, 'Failed to send message - input may be invalid.');
    throw error;
  }

  await replyMessage(interface, 'Successfully sent message!');
  return user;
};
