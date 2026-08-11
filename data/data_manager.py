import os
from typing import Any, Dict

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def conectar():
    """Abre a conexão com o MySQL usando as variáveis do arquivo .env."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "tpac_db"),
        port=int(os.getenv("DB_PORT", "3306"))
    )


def carregar_dados() -> Dict[str, Any]:
    """Carrega usuários, tarefas e passos do MySQL para um dicionário Python."""
    dados: Dict[str, Any] = {}
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, nome, estilo_instrucao
            FROM usuarios
            ORDER BY nome
        """)
        usuarios = cursor.fetchall()

        for usuario in usuarios:
            nome = usuario["nome"]
            dados[nome] = {
                "preferencias": {
                    "estilo_instrucao": usuario["estilo_instrucao"]
                },
                "tarefas_diarias": [],
                "tarefas_educacionais": []
            }

            cursor.execute("""
                SELECT id, titulo, concluida, tipo
                FROM tarefas
                WHERE usuario_id = %s
                ORDER BY id
            """, (usuario["id"],))
            tarefas = cursor.fetchall()

            for tarefa in tarefas:
                tarefa_dict = {
                    "titulo": tarefa["titulo"],
                    "concluida": bool(tarefa["concluida"]),
                    "passos": []
                }

                cursor.execute("""
                    SELECT texto, concluido
                    FROM passos
                    WHERE tarefa_id = %s
                    ORDER BY ordem, id
                """, (tarefa["id"],))

                for passo in cursor.fetchall():
                    tarefa_dict["passos"].append({
                        "texto": passo["texto"],
                        "concluido": bool(passo["concluido"])
                    })

                dados[nome][tarefa["tipo"]].append(tarefa_dict)

        return dados

    finally:
        cursor.close()
        conexao.close()


def salvar_dados(dados: Dict[str, Any]) -> None:
    """Salva o dicionário completo no MySQL.

    A estratégia de apagar e recriar os dados é propositalmente simples e
    didática para o projeto base. Em sistemas maiores usaríamos operações
    INSERT, UPDATE e DELETE específicas.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE passos")
        cursor.execute("TRUNCATE TABLE tarefas")
        cursor.execute("TRUNCATE TABLE usuarios")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        for nome, info_usuario in dados.items():
            estilo = info_usuario.get("preferencias", {}).get(
                "estilo_instrucao", "direto"
            )

            cursor.execute("""
                INSERT INTO usuarios (nome, estilo_instrucao)
                VALUES (%s, %s)
            """, (nome, estilo))
            usuario_id = cursor.lastrowid

            for tipo in ["tarefas_diarias", "tarefas_educacionais"]:
                for tarefa in info_usuario.get(tipo, []):
                    cursor.execute("""
                        INSERT INTO tarefas (usuario_id, tipo, titulo, concluida)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        usuario_id,
                        tipo,
                        tarefa.get("titulo", ""),
                        bool(tarefa.get("concluida", False))
                    ))
                    tarefa_id = cursor.lastrowid

                    for ordem, passo in enumerate(
                        tarefa.get("passos", []), start=1
                    ):
                        cursor.execute("""
                            INSERT INTO passos (tarefa_id, texto, concluido, ordem)
                            VALUES (%s, %s, %s, %s)
                        """, (
                            tarefa_id,
                            passo.get("texto", ""),
                            bool(passo.get("concluido", False)),
                            ordem
                        ))

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()
