def gerar_passos_tarefa(titulo_tarefa: str) -> list:
    """IA simulada usada no projeto base.

    Nesta UC o objetivo é implantar e manter o sistema. Por isso a atividade
    não depende de chave externa nem de internet adicional para funcionar.
    """
    titulo = titulo_tarefa.strip() or "a tarefa"
    return [
        f"Ler com atenção o que precisa ser feito em: {titulo}.",
        "Separar o que precisa ser entregue.",
        "Executar a primeira parte da atividade.",
        "Conferir o resultado antes de finalizar."
    ]


def obter_resposta_ia(pergunta: str, estilo: str = "direto") -> list:
    pergunta = pergunta.strip()
    if estilo == "detalhado":
        return [
            f"Vamos organizar sua dúvida: {pergunta}",
            "Primeiro identifique o objetivo principal.",
            "Depois divida o problema em partes menores.",
            "Execute uma parte de cada vez e confira o resultado."
        ]

    return [
        f"Objetivo identificado: {pergunta}",
        "Faça uma etapa por vez.",
        "Teste antes de avançar."
    ]
