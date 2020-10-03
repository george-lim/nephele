const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const { TELEGRAM_REQUEST_BASE_URL } = process.env;

module.exports.sendMessage = (chatId, text) => {
  return axios.post(`${TELEGRAM_REQUEST_BASE_URL}/sendMessage`, {
    chat_id: chatId,
    text
  });
};

module.exports.sendPhoto = (chatId, photoPath) => {
  const data = new FormData();
  data.append('chat_id', chatId);
  data.append('photo', fs.createReadStream(photoPath));

  return axios.post(`${TELEGRAM_REQUEST_BASE_URL}/sendPhoto`, data, {
    headers: {
      'Content-Type': 'multipart/form-data',
      ...data.getHeaders()
    }
  });
};
