from data.data_manager import salvar_dados


def adicionar_tarefa(dados: dict, usuario: str, chave: str, titulo: str):
    if not titulo.strip():
        return

    dados[usuario][chave].append({
        "titulo": titulo.strip(),
        "concluida": False,
        "passos": []
    })
    salvar_dados(dados)


def alternar_status_tarefa(dados: dict, usuario: str, chave: str, idx: int):
    tarefas = dados[usuario][chave]
    if 0 <= idx < len(tarefas):
        tarefas[idx]["concluida"] = not tarefas[idx]["concluida"]
        salvar_dados(dados)


def injetar_passos_ia(dados: dict, usuario: str, chave: str, idx: int, passos: list):
    tarefas = dados[usuario][chave]
    if 0 <= idx < len(tarefas):
        tarefas[idx]["passos"] = [
            {"texto": passo, "concluido": False}
            for passo in passos
        ]
        salvar_dados(dados)


def alternar_status_passo(dados: dict, usuario: str, chave: str, idx_tarefa: int, idx_passo: int):
    tarefas = dados[usuario][chave]
    if not (0 <= idx_tarefa < len(tarefas)):
        return

    passos = tarefas[idx_tarefa].get("passos", [])
    if 0 <= idx_passo < len(passos):
        passos[idx_passo]["concluido"] = not passos[idx_passo]["concluido"]
        salvar_dados(dados)
