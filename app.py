import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# ===== CONFIG =====
TOKEN = os.getenv("TELEGRAM_TOKEN")

# ===== LOG =====
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ===== ETAPAS =====
FOTOS, TAMANHO, COR, GENERO, ESTADO, MARCA, OBS = range(7)

# ===== INÍCIO =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Envie as 5 fotos do produto (uma por vez)."
    )
    context.user_data["fotos"] = []
    return FOTOS

# ===== RECEBER FOTOS =====
async def receber_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["fotos"].append(update.message.photo[-1].file_id)

        if len(context.user_data["fotos"]) < 5:
            await update.message.reply_text(
                f"Foto {len(context.user_data['fotos'])}/5 recebida. Envie a próxima."
            )
            return FOTOS
        else:
            await update.message.reply_text("✅ Fotos recebidas.\n\nInforme o TAMANHO (ex: G, M, P, G1...).")
            return TAMANHO

# ===== TAMANHO =====
async def tamanho(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["tamanho"] = update.message.text.upper()
    await update.message.reply_text("Informe a COR da peça.")
    return COR

# ===== COR =====
async def cor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["cor"] = update.message.text
    await update.message.reply_text("É Masculino, Feminino ou Infantil?")
    return GENERO

# ===== GENERO =====
async def genero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["genero"] = update.message.text
    await update.message.reply_text("Qual o estado da peça? (Nova, Semi-nova, Usada...)")
    return ESTADO

# ===== ESTADO =====
async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["estado"] = update.message.text
    await update.message.reply_text("Qual a marca?")
    return MARCA

# ===== MARCA =====
async def marca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["marca"] = update.message.text
    await update.message.reply_text("Alguma observação?")
    return OBS

# ===== OBSERVAÇÃO E RESUMO =====
async def obs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["obs"] = update.message.text

    descricao = f"""
🆕 *Novo Produto*

📏 Tamanho: {context.user_data['tamanho']}
🎨 Cor: {context.user_data['cor']}
👕 Gênero: {context.user_data['genero']}
📦 Estado: {context.user_data['estado']}
🏷 Marca: {context.user_data['marca']}
📝 Observações: {context.user_data['obs']}

Está tudo correto? Responda SIM para confirmar.
"""

    await update.message.reply_text(descricao, parse_mode="Markdown")
    return ConversationHandler.END

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FOTOS: [MessageHandler(filters.PHOTO, receber_foto)],
            TAMANHO: [MessageHandler(filters.TEXT & ~filters.COMMAND, tamanho)],
            COR: [MessageHandler(filters.TEXT & ~filters.COMMAND, cor)],
            GENERO: [MessageHandler(filters.TEXT & ~filters.COMMAND, genero)],
            ESTADO: [MessageHandler(filters.TEXT & ~filters.COMMAND, estado)],
            MARCA: [MessageHandler(filters.TEXT & ~filters.COMMAND, marca)],
            OBS: [MessageHandler(filters.TEXT & ~filters.COMMAND, obs)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
