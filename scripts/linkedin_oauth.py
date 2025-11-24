# -*- coding: utf-8 -*-
"""
Script para obtener Access Token de LinkedIn OAuth 2.0
"""

import requests
import urllib.parse
import secrets
import os
from dotenv import load_dotenv

load_dotenv()

# ========== CONFIGURACIÓN ==========
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost:3000/auth/linkedin/callback"
SCOPES = "openid profile w_member_social"

# ========== PASO 1: Generar URL de Autorización ==========
def generate_auth_url():
    if not CLIENT_ID:
        print("ERROR: LINKEDIN_CLIENT_ID no está configurado en .env")
        return None

    state = secrets.token_urlsafe(16)

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "scope": SCOPES
    }

    auth_url = "https://www.linkedin.com/oauth/v2/authorization?" + urllib.parse.urlencode(params)

    print("=" * 60)
    print("PASO 1: Autorización de LinkedIn")
    print("=" * 60)
    print("
1. Abre este enlace en tu navegador:
")
    print(auth_url)
    print("
2. Inicia sesión y autoriza la aplicación")
    print("
3. Serás redirigido a una URL como:")
    print(f"   {REDIRECT_URI}?code=XXXXXX&state=XXXXXX")
    print("
4. Copia el valor del parámetro code de la URL")
    print("=" * 60)

    return state

# ========== PASO 2: Intercambiar Código por Token ==========
def exchange_code_for_token(auth_code):
    if not CLIENT_SECRET:
        print("ERROR: LINKEDIN_CLIENT_SECRET no está configurado en .env")
        return None

    print("
" + "=" * 60)
    print("PASO 2: Obteniendo Access Token...")
    print("=" * 60)

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(token_url, data=data, headers=headers)
        response.raise_for_status()

        token_data = response.json()
        access_token = token_data.get("access_token")
        expires_in = token_data.get("expires_in", 0)

        print("
TOKEN OBTENIDO CON ÉXITO!")
        print("=" * 60)
        print(f"
Access Token:
{access_token}")
        print(f"
Expira en: {expires_in // 86400} días ({expires_in} segundos)")
        print("
" + "=" * 60)
        print("SIGUIENTE PASO:")
        print("=" * 60)
        print("
Agrega esto a tu archivo .env:
")
        print(f"ACCESS_TOKEN_LINKEDIN="{access_token}"")
        print("POST_VISIBILITY="PUBLIC"")
        print("
" + "=" * 60)

        return access_token

    except requests.exceptions.HTTPError as e:
        print(f"
ERROR: {e.response.status_code}")
        print(f"Respuesta: {e.response.text}")
        return None

# ========== EJECUCIÓN ==========
if __name__ == "__main__":
    print("
LinkedIn OAuth 2.0 - Obtener Access Token
")

    # Generar URL
    state = generate_auth_url()

    if state is None:
        exit(1)

    # Esperar código del usuario
    print("
")
    auth_code = input("Pega aquí el código de autorización: ").strip()

    if auth_code:
        exchange_code_for_token(auth_code)
    else:
        print("No se proporcionó código")
