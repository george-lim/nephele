const axios = require('axios');

module.exports.handler = async (outputs, serverless) => {
  const telegramConstants = serverless.service.custom.telegram;
  const telegramWebhookUrl = `${outputs.ServiceEndpoint}/${telegramConstants.webhookPath}`;
  await axios.post(`${telegramConstants.requestBaseUrl}/setWebhook`, { url: telegramWebhookUrl });
  console.log(`Successfully set Telegram webhook: ${telegramWebhookUrl}`);
};
