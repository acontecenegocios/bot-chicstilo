import TelegramBot from "node-telegram-bot-api";

const token = "SEU_TOKEN_AQUI";

const bot = new TelegramBot(token, {
  polling: true
});

console.log("Bot está rodando...");

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(
    msg.chat.id,
    "Olá! O bot ChicStilo está funcionando corretamente."
  );
});
