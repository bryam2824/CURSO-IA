# apis/Conexion_telebot.py

# -- coding: utf-8 --

import telebot
from telebot import types

from apis.db import (
    obtener_id_paciente_por_documento
)

from Resultado import (
    obtener_resultado
)


TOKEN = "TU_TOKEN"

bot = telebot.TeleBot(TOKEN)


# ====================================
# MENU PRINCIPAL
# ====================================

@bot.message_handler(commands=["start"])
def inicio(message):

    teclado = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    teclado.add(
        types.KeyboardButton(
            "🏥 Consultar diagnóstico"
        )
    )

    bot.send_message(
        message.chat.id,
        (
            "Bienvenido a Analizis Dengue V1.0\n\n"
            "Seleccione una opción:"
        ),
        reply_markup=teclado
    )


# ====================================
# CONSULTA DE DIAGNOSTICO
# ====================================

@bot.message_handler(
    func=lambda mensaje:
    mensaje.text == "🏥 Consultar diagnóstico"
)
def pedir_documento(message):

    bot.send_message(
        message.chat.id,
        "Ingrese su documento:"
    )

    bot.register_next_step_handler(
        message,
        buscar_paciente
    )


def buscar_paciente(message):

    documento = message.text.strip()

    id_paciente = (
        obtener_id_paciente_por_documento(
            documento
        )
    )

    if not id_paciente:

        bot.send_message(
            message.chat.id,
            (
                "No existe un paciente "
                "registrado con ese documento."
            )
        )

        return

    resultado = obtener_resultado(
        id_paciente
    )

    enviar_resultado(
        message.chat.id,
        resultado
    )


# ====================================
# PRESENTACION
# ====================================

def enviar_resultado(
    chat_id,
    resultado
):

    mensaje = f"""
ID Paciente: {resultado['id_paciente']}

Variable:
{resultado['variable']}

Riesgo:
{resultado['riesgo']}

Nivel:
{resultado['nivel']}
"""

    bot.send_message(
        chat_id,
        mensaje
    )


# ====================================
# INICIO BOT
# ====================================

print(
    "🤖 Conexion_telebot.py iniciado"
)

bot.infinity_polling()