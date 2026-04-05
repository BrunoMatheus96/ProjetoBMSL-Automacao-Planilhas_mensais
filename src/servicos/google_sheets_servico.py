import os
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleSheetsServico:

    def __init__(self):
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            ROOT_DIR = os.path.dirname(BASE_DIR)

            JSON_DIR = os.path.join(ROOT_DIR, "autenticacoes", "arquivos_json")

            CREDENCIAIS_PATH = os.path.join(JSON_DIR, "google_sheets_credenciais.json")
            TOKEN_PATH = os.path.join(JSON_DIR, "token.json")

            SCOPES = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ]

            if not os.path.exists(CREDENCIAIS_PATH):
                raise Exception(f"Arquivo não encontrado: {CREDENCIAIS_PATH}")

            creds = None

            # 🔹 Carrega token
            if os.path.exists(TOKEN_PATH):
                creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

            # 🔹 Se inválido, autentica
            if not creds or not creds.valid:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENCIAIS_PATH, SCOPES
                )
                creds = flow.run_local_server(port=0)

                with open(TOKEN_PATH, "w") as token:
                    token.write(creds.to_json())

            # 🔹 cria client do gspread usando OAuth
            self.client = gspread.authorize(creds)

        except Exception as e:
            print(f"Erro no __init__ em google_sheets_servico.py: {e}")

    def ler_aba(self, spreadsheet_id, nome_aba):
        try:
            if not self.client:
                raise Exception("Client não inicializado")

            # 🔹 abre pelo ID (mais seguro)
            planilha = self.client.open_by_key(spreadsheet_id)

            aba = planilha.worksheet(nome_aba)

            dados = aba.get_all_values()

            if not dados or len(dados) < 2:
                raise Exception("Planilha vazia ou sem dados")

            header = dados[0]
            linhas = dados[1:]

            resultado = []
            for linha in linhas:
                if any(linha):
                    registro = dict(zip(header, linha))
                    resultado.append(registro)

            return resultado

        except Exception as e:
            print(f"Erro no ler_aba em google_sheets_servico.py: {e}")
