from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os

SCOPES = ["https://www.googleapis.com/auth/drive"]

# 📌 Caminho da pasta atual (autenticacoes)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 📌 Subpasta onde estão os JSONs
JSON_DIR = os.path.join(BASE_DIR, "arquivos_json")

# 📌 Caminhos completos
TOKEN_PATH = os.path.join(JSON_DIR, "token.json")
CREDENCIAIS_PATH = os.path.join(JSON_DIR, "google_credenciais.json")


def get_credenciais():
    creds = None

    try:
        # 🔹 Carrega token salvo
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        # 🔹 Se não existir ou estiver inválido
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENCIAIS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

            # 🔹 Garante que a pasta existe
            os.makedirs(JSON_DIR, exist_ok=True)

            # 🔹 Salva o token
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())

        return creds

    except Exception as e:
        print(f"Erro em autenticacoes no google_drive.py: {e}")
