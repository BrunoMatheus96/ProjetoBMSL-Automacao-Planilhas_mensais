from src.tarefas import listar_arquivos
from src.tarefas.baixar_arquivo import baixar_alunos
from src.tarefas.duplicar_planilha import duplicar_mes
from src.tarefas.processar_excel import ler_arquivo_alunos
from src.tarefas.listar_arquivos import listar_arquivos
from src.tarefas.sincronizar_google_sheet import sincronizar


def rodar_automacao_mensal():
    try:
        print("🚀 Iniciando automação...")

        baixar_alunos()
        ler_arquivo_alunos()
        duplicar_mes()

        # 🔥 pega os IDs dinamicamente
        sheet_id_mes, sheet_id_controle = listar_arquivos()

        # 🔥 passa os IDs para a função
        sincronizar(sheet_id_mes, sheet_id_controle)

        print("Finalizado ✅")
    except Exception as e:
        print(f"Erro em no workflow planilha_mensal_workflow: {e}")
