const { replyMessage, replyPhoto } = require('../common/actions');
const { SCREENSHOT_PATH, execute } = require('../common/puppeteer');

const { TEST_TIMEOUT } = process.env;

module.exports.handler = async event => {
  const interface = event.interface;
  let testResultUrl = null;

  await replyMessage(interface, 'Running global broadband speed test...');

  try {
    const bot = async page => {
      await Promise.all([
        page.goto('https://www.speedtest.net'),
        page.waitForNavigation({ waitUntil: 'networkidle2' })
      ]);

      const startButton = await page.waitForSelector('.js-start-test');
      await Promise.all([
        startButton.click(),
        page.waitForNavigation({ timeout: TEST_TIMEOUT }),
      ]);

      return page.url();
    };

    testResultUrl = await execute(bot);
  }
  catch (error) {
    await replyPhoto(interface, SCREENSHOT_PATH);
    await replyMessage(interface, 'Failed to run test.');
    throw error;
  }

  await replyMessage(interface, testResultUrl);
};
