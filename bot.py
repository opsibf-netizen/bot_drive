import os
import io
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# ===== CONFIGURAÇÃO =====
TELEGRAM_TOKEN = "8805755933:AAHCALbeCLkR2UIc9dz6G51XhsJ2AAqM3K0"
GEMINI_API_KEY = "AIzaSyA2trd_yE_dkRH7BvDVAobf6wACkN04OUI"

# Configura o Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ===== COMANDOS DO BOT =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Olá! Sou seu bot com Gemini.\n\n"
        "Envie qualquer texto e eu responderei com a IA.\n"
        "Ex: 'Me explique o que é Python'"
    )

async def conversar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("🧠 Pensando...")
    
    try:
        resposta = model.generate_content(user_text)
        texto = resposta.text
        
        # Divide mensagens longas
        if len(texto) > 4000:
            for i in range(0, len(texto), 4000):
                await update.message.reply_text(texto[i:i+4000])
        else:
            await update.message.reply_text(texto)
            
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")

# ===== MAIN =====
if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, conversar))
    print("Bot rodando...")
    app.run_polling()
