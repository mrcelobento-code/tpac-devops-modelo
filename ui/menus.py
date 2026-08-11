from ui.utils import exibir_cabecalho
from data.data_manager import salvar_dados
import core.tarefas as core_tarefas
import core.ia_service as ia_service


def criar_usuario_menu(dados: dict):
    exibir_cabecalho("CRIAR PERFIL CUSTOMIZADO")
    nome = input("Digite o nome do usuário: ").strip()

    if not nome:
        input("\nO nome não pode ficar vazio. Pressione Enter.")
        return

    if nome in dados:
        input("\nEsse perfil já existe. Pressione Enter.")
        return

    print("\nComo você prefere receber instruções?")
    print("1. Curtas e diretas")
    print("2. Detalhadas e explicativas")
    escolha = input("Escolha: ").strip()
    estilo = "detalhado" if escolha == "2" else "direto"

    dados[nome] = {
        "preferencias": {"estilo_instrucao": estilo},
        "tarefas_diarias": [],
        "tarefas_educacionais": []
    }

    salvar_dados(dados)
    input(f"\nPerfil [{nome}] criado com sucesso. Pressione Enter.")


def _mostrar_tarefas(tarefas: list):
    if not tarefas:
        print("[Nenhuma tarefa cadastrada.]\n")
        return

    for indice, tarefa in enumerate(tarefas, start=1):
        status = "[X]" if tarefa.get("concluida") else "[ ]"
        print(f"{indice}. {status} {tarefa.get('titulo', '')}")

        for numero_passo, passo in enumerate(tarefa.get("passos", []), start=1):
            simbolo = "✓" if passo.get("concluido") else "○"
            print(f"   {numero_passo}. {simbolo} {passo.get('texto', '')}")
        print()


def gerenciar_tarefas_menu(dados: dict, usuario: str, chave: str, titulo: str):
    while True:
        exibir_cabecalho(titulo)
        tarefas = dados[usuario][chave]
        _mostrar_tarefas(tarefas)

        print("1. Criar tarefa")
        print("2. Alternar status da tarefa")
        print("3. Desmembrar tarefa com apoio simulado")
        print("4. Alternar status de um passo")
        print("5. Voltar")

        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            nome_tarefa = input("Título da tarefa: ").strip()
            if nome_tarefa:
                core_tarefas.adicionar_tarefa(
                    dados, usuario, chave, nome_tarefa
                )
                input("\nTarefa criada e salva no MySQL. Pressione Enter.")
            else:
                input("\nTítulo vazio. Nada foi salvo. Pressione Enter.")

        elif opcao == "2":
            if not tarefas:
                input("\nNão há tarefas para alterar. Pressione Enter.")
                continue
            try:
                indice = int(input("Número da tarefa: ")) - 1
                core_tarefas.alternar_status_tarefa(
                    dados, usuario, chave, indice
                )
                input("\nStatus atualizado. Pressione Enter.")
            except ValueError:
                input("\nDigite somente o número da tarefa. Pressione Enter.")

        elif opcao == "3":
            if not tarefas:
                input("\nNão há tarefas para desmembrar. Pressione Enter.")
                continue
            try:
                indice = int(input("Número da tarefa: ")) - 1
                if 0 <= indice < len(tarefas):
                    passos = ia_service.gerar_passos_tarefa(
                        tarefas[indice]["titulo"]
                    )
                    print("\nPassos sugeridos:")
                    for numero, passo in enumerate(passos, start=1):
                        print(f"{numero}. {passo}")
                    confirmar = input("\nSalvar estes passos? (s/n): ").lower()
                    if confirmar == "s":
                        core_tarefas.injetar_passos_ia(
                            dados, usuario, chave, indice, passos
                        )
                        input("\nPassos salvos no MySQL. Pressione Enter.")
            except ValueError:
                input("\nDigite somente o número da tarefa. Pressione Enter.")

        elif opcao == "4":
            if not tarefas:
                input("\nNão há tarefas. Pressione Enter.")
                continue
            try:
                indice_tarefa = int(input("Número da tarefa: ")) - 1
                indice_passo = int(input("Número do passo: ")) - 1
                core_tarefas.alternar_status_passo(
                    dados, usuario, chave, indice_tarefa, indice_passo
                )
                input("\nStatus do passo atualizado. Pressione Enter.")
            except ValueError:
                input("\nDigite somente números. Pressione Enter.")

        elif opcao == "5":
            break

        else:
            input("\nOpção inválida. Pressione Enter.")


def painel_ia_menu(dados: dict, usuario: str):
    exibir_cabecalho("CENTRAL DE IA — MODO SIMULADO")
    print("Nesta UC a função é simulada para não depender de chave externa.")
    print("Digite 'sair' para voltar.\n")

    estilo = dados[usuario]["preferencias"]["estilo_instrucao"]

    while True:
        pergunta = input("Você: ").strip()
        if pergunta.lower() == "sair":
            break
        if not pergunta:
            continue

        respostas = ia_service.obter_resposta_ia(pergunta, estilo)
        print("\nApoio:")
        for linha in respostas:
            print(f"- {linha}")
        print()


def painel_principal_menu(dados: dict, usuario: str):
    while True:
        exibir_cabecalho(f"PAINEL DO USUÁRIO: {usuario}")
        print("1. Atividades Diárias")
        print("2. Atividades Educacionais")
        print("3. Central de IA")
        print("4. Logout")

        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            gerenciar_tarefas_menu(
                dados, usuario, "tarefas_diarias", "ATIVIDADES DIÁRIAS"
            )
        elif opcao == "2":
            gerenciar_tarefas_menu(
                dados,
                usuario,
                "tarefas_educacionais",
                "ATIVIDADES EDUCACIONAIS"
            )
        elif opcao == "3":
            painel_ia_menu(dados, usuario)
        elif opcao == "4":
            break
        else:
            input("\nOpção inválida. Pressione Enter.")
