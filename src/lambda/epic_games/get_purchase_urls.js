const epicGames = require('epic-games-bot');
const { replyMessage, replyPhoto } = require('../../common/actions');
const { SCREENSHOT_PATH, execute } = require('../../common/puppeteer');

module.exports.handler = async event => {
  const interface = event.interface;
  let purchaseUrls = null;

  await replyMessage(interface, 'Getting purchase URLs...');

  try {
    const bot = async (page, client) => await epicGames.getPurchaseUrls(page, client);
    purchaseUrls = await execute(bot);
  }
  catch (error) {
    await replyPhoto(interface, SCREENSHOT_PATH);
    await replyMessage(interface, 'Failed to get URLs.');
    throw error;
  }

  if (!purchaseUrls.length) {
    await replyMessage(interface, 'No purchase URLs available!');
    return;
  }

  for (let i = 0; i < purchaseUrls.length; ++i) {
    await replyMessage(interface, purchaseUrls[i]);
  }
};
