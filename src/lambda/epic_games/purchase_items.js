const epicGames = require('epic-games-bot');
const { replyMessage, replyPhoto } = require('../../common/actions');
const { SCREENSHOT_PATH, execute } = require('../../common/puppeteer');

module.exports.handler = async event => {
  const interface = event.interface;
  const user = event.dynamodb.Item;
  let successfulPurchaseUrls = null;

  if (!user.cookies) {
    await replyMessage(interface, 'Please log into Epic Games first.');
    throw new Error('Missing login cookies');
  }

  await replyMessage(interface, 'Purchasing items...');

  try {
    const bot = async (page, client) => {
      await epicGames.logIn(page, client);
      const purchaseUrls = await epicGames.getPurchaseUrls(page, client);
      successfulPurchaseUrls = await epicGames.purchaseItems(page, purchaseUrls);

      const cookies = (await client.send('Network.getAllCookies')).cookies;
      return cookies;
    };

    user.cookies = await execute(bot, user.cookies);
  }
  catch (error) {
    await replyPhoto(interface, SCREENSHOT_PATH);
    await replyMessage(interface, 'Failed to purchase items.');
    throw error;
  }

  if (successfulPurchaseUrls.length) {
    for (let i = 0; i < successfulPurchaseUrls.length; ++i) {
      await replyMessage(interface, successfulPurchaseUrls[i]);
    }
  }
  else {
    await replyMessage(interface, 'Already purchased everything!');
  }

  return user;
};
