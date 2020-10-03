const telegram = require('./telegram');

const { TELEGRAM_INTERFACE_NAME } = process.env;

module.exports.replyMessage = (interface, message) => {
  if (interface.name == TELEGRAM_INTERFACE_NAME) {
    return telegram.sendMessage(interface.chatId, message);
  }

  throw new Error('Unknown interface name');
};

module.exports.replyPhoto = (interface, photoPath) => {
  if (interface.name == TELEGRAM_INTERFACE_NAME) {
    return telegram.sendPhoto(interface.chatId, photoPath);
  }

  throw new Error('Unknown interface name');
};
