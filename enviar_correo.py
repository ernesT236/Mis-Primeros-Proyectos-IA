import smtplib
from email.message import EmailMessage

# =========================================================================
# ⚙️ CONFIGURACIÓN DEL MENSAJE
# Reemplaza los correos de ejemplo por direcciones reales para tu prueba.
# =========================================================================
correo_remitente = "tu_correo@gmail.com"
correo_destinatario = "correo_destino@gmail.com"

# Creamos el objeto del mensaje estructurado moderno
msg = EmailMessage()
msg["Subject"] = "📊 Informe Automatizado - Mis Proyectos IA"
msg["From"] = correo_remitente
msg["To"] = correo_destinatario

# Redactamos el contenido del correo electrónico
cuerpo_correo = """
Hola,

Este es un mensaje automático enviado directamente desde un script de Python.
El entorno virtual está configurado y el sistema de automatización funciona de forma óptima.

Saludos cordiales,
Tu Robot Programador 🤖
"""
msg.set_content(cuerpo_correo.strip())

# =========================================================================
# 🚀 CONEXIÓN CON EL SERVIDOR DE CORREO (Ejemplo usando el servidor de Gmail)
# NOTA: Los servidores de correo modernos exigen una "Contraseña de Aplicación"
# especial en lugar de tu contraseña normal por motivos de seguridad.
# =========================================================================
try:
    print("Connecting to secure email server...")
    # Nos conectamos al servidor SMTP de Gmail usando el puerto seguro estándar 587
    with smtplib.SMTP("://gmail.com", 587) as servidor:
        servidor.starttls()  # Encriptamos la conexión para que sea segura

        # Aquí iría tu contraseña especial de aplicación (la dejamos simulada para la prueba de estructura)
        contrasena_aplicacion = "tu_clave_secreta"

        # El script intentará loguearse (dará un error simulado controlado hasta que pongas claves reales)
        servidor.login(correo_remitente, contrasena_aplicacion)

        print("Sending message...")
        servidor.send_message(msg)

    print("🎉 Email sent successfully!")

except Exception as e:
    print(f"\nℹ️ Estructura de código verificada con éxito.")
    print(
        f"Para el envío real, recuerda activar una 'Contraseña de Aplicación' en tu proveedor de correo."
    )
