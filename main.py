from data.data_manager import carregar_dados
from ui.menus import criar_usuario_menu, painel_principal_menu
from ui.utils import exibir_cabecalho


def executar_sistema():
    while True:
        dados = carregar_dados()
        exibir_cabecalho("SISTEMA TPAC ACESSIBLE")
        print("1. Entrar com perfil existente")
        print("2. Criar novo perfil customizado")
        print("3. Encerrar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            if not dados:
                input("\nNenhum perfil salvo. Crie um primeiro! Pressione Enter.")
                continue

            print("\nPerfis disponíveis:")
            for nome in dados:
                print(f"- {nome}")

            nome = input("\nDigite o nome do perfil: ").strip()
            if nome in dados:
                painel_principal_menu(dados, nome)
            else:
                input("\nPerfil não encontrado. Pressione Enter.")

        elif opcao == "2":
            criar_usuario_menu(dados)

        elif opcao == "3":
            print("\nSistema encerrado.")
            break

        else:
            input("\nOpção inválida. Pressione Enter para tentar novamente.")


if __name__ == "__main__":
    executar_sistema()
