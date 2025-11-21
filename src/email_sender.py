"""
Módulo mejorado para envío de correos electrónicos
Soporta: Gmail, Microsoft 365/Outlook, y servidores SMTP personalizados
"""
import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


def send_mail(receivers: List[str], subject: str, content_text: str, content_html: Optional[str] = None, attachments: Optional[List[str]] = None) -> bool:
    """
    Envía un correo con adjuntos.

    Soporta múltiples proveedores:
    - Gmail (smtp.gmail.com:465 con SSL)
    - Microsoft 365/Outlook (smtp.office365.com:587 con STARTTLS)
    - Servidores SMTP personalizados

    Args:
        receivers: Lista de correos destinatarios
        subject: Asunto del correo
        content_text: Contenido en texto plano
        content_html: Contenido en HTML (opcional)
        attachments: Lista de rutas a archivos adjuntos (opcional)

    Returns:
        bool: True si el envío fue exitoso, False en caso contrario
    """
    # Cargar credenciales desde variables de entorno
    # Primero busca SMTP_* (nuevo estándar), si no, usa GMAIL_* (retrocompatibilidad)
    sender_email = os.getenv("SMTP_USERNAME") or os.getenv("GMAIL_USERNAME")
    app_password = os.getenv("SMTP_PASSWORD") or os.getenv("GMAIL_APP_PASSWORD")

    # Configuración SMTP (valores por defecto para Gmail si no se especifican)
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_use_tls = os.getenv("SMTP_USE_TLS", "false").lower() == "true"
    smtp_use_ssl = os.getenv("SMTP_USE_SSL", "true").lower() == "true"

    # Validar credenciales
    if not sender_email or not app_password:
        print("❌ Error: No se encontraron las credenciales SMTP")
        print("Variables requeridas:")
        print("  - SMTP_USERNAME + SMTP_PASSWORD (recomendado)")
        print("  - O GMAIL_USERNAME + GMAIL_APP_PASSWORD (retrocompatibilidad)")
        return False

    if not receivers:
        print("⚠️  Advertencia: No hay destinatarios para enviar el correo.")
        return False

    try:
        # Crear mensaje MIME
        msg = MIMEMultipart('mixed')
        msg['From'] = sender_email
        msg['Subject'] = subject
        msg['To'] = ", ".join(receivers)

        # Crear contenedor para el cuerpo del mensaje
        body_part = MIMEMultipart('alternative')
        body_part.attach(MIMEText(content_text, 'plain'))

        if content_html:
            body_part.attach(MIMEText(content_html, 'html'))

        msg.attach(body_part)

        # Adjuntar archivos
        if attachments:
            for filepath in attachments:
                if not os.path.exists(filepath):
                    print(f"⚠️  Advertencia: Archivo no encontrado: {filepath}")
                    continue

                with open(filepath, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())

                encoders.encode_base64(part)
                filename = os.path.basename(filepath)
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(part)
                print(f"📎 Archivo adjuntado: {filename}")

        # Configurar contexto SSL
        context = ssl.create_default_context()

        # Conectar según el tipo de conexión
        if smtp_use_ssl:
            # SSL directo (puerto 465) - Gmail
            print(f"🔐 Conectando a {smtp_server}:{smtp_port} usando SSL...")
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(sender_email, app_password)
                server.sendmail(sender_email, receivers, msg.as_string())
        else:
            # STARTTLS (puerto 587) - Microsoft 365, Outlook
            print(f"🔐 Conectando a {smtp_server}:{smtp_port} usando STARTTLS...")
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()
                if smtp_use_tls:
                    server.starttls(context=context)
                    server.ehlo()
                server.login(sender_email, app_password)
                server.sendmail(sender_email, receivers, msg.as_string())

        print(f"✅ Correo enviado exitosamente a: {', '.join(receivers)}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Error de autenticación SMTP: {e}")
        print("\n🔍 Posibles soluciones:")
        print("1. Verifica que el usuario y contraseña sean correctos")
        print("2. Si usas Microsoft 365:")
        print("   - Necesitas una 'Contraseña de aplicación'")
        print("   - Genera una en: https://account.microsoft.com/security")
        print("3. Si usas Gmail:")
        print("   - Necesitas una 'Contraseña de aplicación'")
        print("   - Activa 2FA y genera una en: https://myaccount.google.com/apppasswords")
        return False

    except smtplib.SMTPServerDisconnected as e:
        print(f"❌ Servidor desconectado: {e}")
        print("Verifica que el servidor y puerto sean correctos")
        return False

    except smtplib.SMTPException as e:
        print(f"❌ Error SMTP: {e}")
        return False

    except Exception as e:
        print(f"❌ Error inesperado al enviar el correo: {e}")
        import traceback
        traceback.print_exc()
        return False


# Función de compatibilidad con el código antiguo
def send_gmail(*args, **kwargs):
    """Alias para mantener compatibilidad con código antiguo"""
    return send_mail(*args, **kwargs)


if __name__ == "__main__":
    # Test básico
    print("🧪 Test del módulo de envío de correos")
    print("=" * 50)

    if not os.getenv("SMTP_USERNAME") and not os.getenv("GMAIL_USERNAME"):
        print("⚠️  Configura las variables de entorno primero")
        print("Ejemplo para Microsoft 365:")
        print("  SMTP_SERVER=smtp.office365.com")
        print("  SMTP_PORT=587")
        print("  SMTP_USE_TLS=true")
        print("  SMTP_USE_SSL=false")
        print("  SMTP_USERNAME=tu_email@gomezycrespo.com")
        print("  SMTP_PASSWORD=tu_contraseña_de_aplicación")
    else:
        print("✅ Credenciales encontradas")
        print(f"Servidor: {os.getenv('SMTP_SERVER', 'smtp.gmail.com')}")
        print(f"Puerto: {os.getenv('SMTP_PORT', '465')}")
        print(f"Usuario: {os.getenv('SMTP_USERNAME') or os.getenv('GMAIL_USERNAME')}")
