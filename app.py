from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# ===============================
# PEGA O TOKEN DO TELEGRAM DA VARIÁVEL DE AMBIENTE
# ===============================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("Por favor configure a variável de ambiente TELEGRAM_TOKEN no Render!")

# Lista de produtos cadastrados
produtos = []

# Campos do cadastro
campos_produto = ["tamanho", "cor", "categoria", "estado", "marca", "observacoes"]
perguntas = {
    "tamanho": "Digite o tamanho (G, M, P, Infantil):",
    "cor": "Digite a cor:",
    "categoria": "Masculino, Feminino ou Infantil?",
    "estado": "Qual o estado da peça?",
    "marca": "Qual a marca?",
    "observacoes": "Alguma observação sobre o produto?"
}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Olá! Envie até 5 fotos do produto para começar o cadastro.")

def fotos_handler(update: Update, context: CallbackContext):
    fotos = update.message.photo
    if not fotos:
        update.message.reply_text("Envie uma foto válida.")
        return
    context.user_data.setdefault("fotos", []).append(fotos[-1].file_id)
    update.message.reply_text(f"Foto recebida! Total de fotos enviadas: {len(context.user_data['fotos'])}")

    if len(context.user_data["fotos"]) == 5:
        context.user_data["cadastro"] = {}
        context.user_data["campo_atual"] = 0
        update.message.reply_text(perguntas[campos_produto[0]])

def mensagem_handler(update: Update, context: CallbackContext):
    if "campo_atual" not in context.user_data:
        update.message.reply_text("Envie primeiro as 5 fotos do produto.")
        return

    campo = campos_produto[context.user_data["campo_atual"]]
    context.user_data["cadastro"][campo] = update.message.text
    context.user_data["campo_atual"] += 1

    if context.user_data["campo_atual"] < len(campos_produto):
        proximo_campo = campos_produto[context.user_data["campo_atual"]]
        update.message.reply_text(perguntas[proximo_campo])
    else:
        # Cadastro completo, montar descritivo
        desc = f"✅ Produto cadastrado:\n"
        for c in campos_produto:
            desc += f"{c.capitalize()}: {context.user_data['cadastro'][c]}\n"
        desc += f"Fotos: {len(context.user_data['fotos'])} enviadas"

        # Botões Disponível / Vendido
        teclado = [
            [InlineKeyboardButton("Disponível ✅", callback_data="disponivel"),
             InlineKeyboardButton("Vendido ❌", callback_data="vendido")]
        ]
        markup = InlineKeyboardMarkup(teclado)
        update.message.reply_text(desc, reply_markup=markup)

        # Limpar dados para próximo produto
        context.user_data.clear()

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, fotos_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, mensagem_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
