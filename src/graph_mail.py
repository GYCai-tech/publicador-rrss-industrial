"""
Módulo para envío de correos usando Microsoft Graph API.
Ideal para organizaciones con Microsoft 365 que tienen SMTP AUTH deshabilitado.
"""

import os
import requests
from typing import List, Optional
from dotenv import load_dotenv

try:
    from msal import ConfidentialClientApplication
except ImportError:
    ConfidentialClientApplication = None
    print("Advertencia: msal no está instalado. Ejecuta: pip install msal")

# Cargar variables de entorno
load_dotenv()


def get_graph_config() -> dict:
    """
    Obtiene la configuración de Microsoft Graph API desde variables de entorno.

    Returns:
        dict: Configuración con client_id, tenant_id, client_secret, sender_email
              None si no hay configuración.
    """
    client_id = os.getenv("MICROSOFT_CLIENT_ID")
    tenant_id = os.getenv("MICROSOFT_TENANT_ID")
    client_secret = os.getenv("MICROSOFT_CLIENT_SECRET")
    sender_email = os.getenv("MICROSOFT_SENDER_EMAIL")

    if not all([client_id, tenant_id, client_secret, sender_email]):
        return None

    return {
        "client_id": client_id,
        "tenant_id": tenant_id,
        "client_secret": client_secret,
        "sender_email": sender_email
    }


def get_access_token() -> str:
    """
    Obtiene un token de acceso para Microsoft Graph API.

    Returns:
        str: Token de acceso o None si falla.
    """
    if ConfidentialClientApplication is None:
        print("Error: msal no está instalado. Ejecuta: pip install msal")
        return None

    config = get_graph_config()
    if not config:
        print("Error: Configuración de Microsoft Graph incompleta.")
        return None

    authority = f"https://login.microsoftonline.com/{config['tenant_id']}"

    app = ConfidentialClientApplication(
        config['client_id'],
        authority=authority,
        client_credential=config['client_secret']
    )

    # Obtener token para Microsoft Graph
    scopes = ["https://graph.microsoft.com/.default"]

    result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        return result["access_token"]
    else:
        error = result.get("error", "Unknown error")
        error_description = result.get("error_description", "")
        print(f"Error obteniendo token: {error}")
        print(f"Descripción: {error_description}")
        return None


def send_mail_graph(
    receivers: List[str],
    subject: str,
    content_text: str,
    content_html: Optional[str] = None,
    attachments: Optional[List[str]] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None
) -> bool:
    """
    Envía un correo usando Microsoft Graph API.

    Args:
        receivers: Lista de direcciones de correo destinatarias
        subject: Asunto del correo
        content_text: Contenido en texto plano
        content_html: Contenido en HTML (opcional)
        attachments: Lista de rutas a archivos adjuntos (opcional)
        cc: Lista de correos en copia (opcional)
        bcc: Lista de correos en copia oculta (opcional)

    Returns:
        bool: True si el envío fue exitoso, False en caso contrario.
    """
    config = get_graph_config()
    if not config:
        print("Error: Configuración de Microsoft Graph incompleta.")
        print("Variables requeridas en .env:")
        print("  MICROSOFT_CLIENT_ID")
        print("  MICROSOFT_TENANT_ID")
        print("  MICROSOFT_CLIENT_SECRET")
        print("  MICROSOFT_SENDER_EMAIL")
        return False

    if not receivers:
        print("Advertencia: No hay destinatarios para enviar el correo.")
        return False

    # Obtener token de acceso
    access_token = get_access_token()
    if not access_token:
        return False

    # Construir el mensaje
    message = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML" if content_html else "Text",
                "content": content_html if content_html else content_text
            },
            "toRecipients": [
                {"emailAddress": {"address": email}} for email in receivers
            ]
        },
        "saveToSentItems": "true"
    }

    # Añadir CC si existe
    if cc:
        message["message"]["ccRecipients"] = [
            {"emailAddress": {"address": email}} for email in cc
        ]

    # Añadir BCC si existe
    if bcc:
        message["message"]["bccRecipients"] = [
            {"emailAddress": {"address": email}} for email in bcc
        ]

    # Añadir adjuntos si existen
    if attachments:
        message["message"]["attachments"] = []
        for filepath in attachments:
            if not os.path.exists(filepath):
                print(f"Advertencia: Archivo no encontrado: {filepath}")
                continue

            import base64
            with open(filepath, "rb") as f:
                content = base64.b64encode(f.read()).decode("utf-8")

            filename = os.path.basename(filepath)
            message["message"]["attachments"].append({
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": filename,
                "contentBytes": content
            })
            print(f"Archivo adjuntado: {filename}")

    # Enviar el correo
    sender_email = config['sender_email']
    endpoint = f"https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(endpoint, json=message, headers=headers)

        if response.status_code == 202:
            print(f"Correo enviado exitosamente via Graph API a: {', '.join(receivers)}")
            return True
        else:
            print(f"Error al enviar correo: {response.status_code}")
            print(f"Respuesta: {response.text}")

            # Errores comunes
            if response.status_code == 401:
                print("\nPosible solución: Verifica que el Client Secret no haya expirado.")
            elif response.status_code == 403:
                print("\nPosible solución: Verifica que la app tenga el permiso 'Mail.Send' en Azure.")
                print("También asegúrate de que sea un permiso de APLICACIÓN, no delegado.")
            elif response.status_code == 404:
                print(f"\nPosible solución: Verifica que el email '{sender_email}' exista y sea válido.")

            return False

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return False


def test_graph_connection() -> bool:
    """
    Prueba la conexión con Microsoft Graph API.

    Returns:
        bool: True si la conexión es exitosa, False en caso contrario.
    """
    config = get_graph_config()
    if not config:
        print("Error: Configuración de Microsoft Graph incompleta.")
        return False

    print(f"Probando conexión con Microsoft Graph API...")
    print(f"  Client ID: {config['client_id'][:8]}...")
    print(f"  Tenant ID: {config['tenant_id'][:8]}...")
    print(f"  Sender: {config['sender_email']}")

    token = get_access_token()
    if token:
        print("Conexión exitosa con Microsoft Graph API")
        return True
    else:
        print("Error: No se pudo obtener el token de acceso")
        return False


if __name__ == "__main__":
    print("Test del módulo Microsoft Graph API")
    print("=" * 50)

    if get_graph_config():
        test_graph_connection()
    else:
        print("Configura las siguientes variables en tu .env:")
        print("  MICROSOFT_CLIENT_ID=tu-client-id")
        print("  MICROSOFT_TENANT_ID=tu-tenant-id")
        print("  MICROSOFT_CLIENT_SECRET=tu-client-secret")
        print("  MICROSOFT_SENDER_EMAIL=correo@tudominio.com")
