const chromium = require('chrome-aws-lambda');

module.exports.SCREENSHOT_PATH = '/tmp/puppeteer_screenshot.png';

module.exports.execute = async (bot, cookies) => {
  let browser = null;
  let page = null;

  try {
    browser = await chromium.puppeteer.launch({
      args: chromium.args,
      defaultViewport: chromium.defaultViewport,
      executablePath: await chromium.executablePath,
      headless: chromium.headless,
      ignoreHTTPSErrors: true
    });

    page = await browser.newPage();
    const client = await page.target().createCDPSession();

    cookies = cookies || [];
    await page.setCookie(...cookies);
    const result = await bot(page, client);

    await browser.close();
    return result;
  }
  catch (error) {
    console.error(error);

    if (page) {
      await page.screenshot({ path: this.SCREENSHOT_PATH });
    }

    if (browser) {
      await browser.close();
    }

    throw error;
  }
};
