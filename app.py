import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler

# Token do Telegram
TOKEN = os.environ.get('TELEGRAM_TOKEN')

# Dicionário para armazenar produtos temporários
produtos_temp = {}

# Função de start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Envie até 5 fotos do produto para começar o cadastro.")

# Função para receber fotos
async def fotos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in produtos_temp:
        produtos_temp[user_id] = {"fotos": [], "info": {}}
    produtos_temp[user_id]["fotos"].append(update.message.photo[-1].file_id)
    
    if len(produtos_temp[user_id]["fotos"]) < 5:
        await update.message.reply_text(f"Foto recebida! Envie mais {5 - len(produtos_temp[user_id]['fotos'])} fotos.")
    else:
        await update.message.reply_text("Fotos recebidas! Agora me informe o tamanho (G, M, P, etc).")

# Função para receber informações textuais
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in produtos_temp or len(produtos_temp[user_id]["fotos"]) < 5:
        await update.message.reply_text("Por favor, envie primeiro as 5 fotos do produto.")
        return
    
    info = produtos_temp[user_id]["info"]
    if "tamanho" not in info:
        info["tamanho"] = update.message.text.upper()
        await update.message.reply_text("Qual a cor da peça?")
    elif "cor" not in info:
        info["cor"] = update.message.text
        await update.message.reply_text("Masculino, Feminino ou Infantil?")
    elif "publico" not in info:
        info["publico"] = update.message.text
        await update.message.reply_text("Qual o estado da peça?")
    elif "estado" not in info:
        info["estado"] = update.message.text
        await update.message.reply_text("Qual a marca?")
    elif "marca" not in info:
        info["marca"] = update.message.text
        await update.message.reply_text("Observações adicionais?")
    elif "observacoes" not in info:
        info["observacoes"] = update.message.text
        resumo = f"Tamanho: {info['tamanho']}\nCor: {info['cor']}\nPúblico: {info['publico']}\nEstado: {info['estado']}\nMarca: {info['marca']}\nObservações: {info['observacoes']}"
        await update.message.reply_text(f"Confirme os dados do produto:\n{resumo}\n\nSe estiver ok, responda 'OK' para subir ao catálogo.")
    elif update.message.text.upper() == "OK":
        await update.message.reply_text("Produto cadastrado com sucesso! 🎉")
        # Aqui você pode adicionar lógica de salvar em banco ou site
        produtos_temp.pop(user_id)

# Main
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, fotos))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, info))

    print("Bot rodando...")
    app.run_polling()
