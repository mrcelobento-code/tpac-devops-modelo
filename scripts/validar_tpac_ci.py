import os
import sys
from pathlib import Path

from dotenv import load_dotenv

RAIZ_PROJETO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

CONFIG = RAIZ_PROJETO / "aula02" / "configuracao.env"

print("=" * 64)
print("TPAC DEVOPS — VALIDAÇÃO DA IMPLANTAÇÃO REMOTA")
print("=" * 64)

if not CONFIG.exists():
    print("ERRO: não encontrei aula02/configuracao.env")
    sys.exit(1)

load_dotenv(CONFIG, override=True)

campos = ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME"]
faltando = [campo for campo in campos if not os.getenv(campo)]
if faltando:
    print("ERRO: faltam valores de configuração:", ", ".join(faltando))
    sys.exit(1)

print("1/5 Configuração encontrada.")
print(f"    servidor: {os.getenv('DB_HOST')}")
print(f"    porta:    {os.getenv('DB_PORT')}")
print(f"    banco:    {os.getenv('DB_NAME')}")
print(f"    usuário:  {os.getenv('DB_USER')}")
print("    senha:    [oculta]")

try:
    import mysql.connector
except Exception as exc:
    print("ERRO: biblioteca mysql-connector-python não está disponível.")
    print(exc)
    sys.exit(1)

print("2/5 Biblioteca Python do MySQL disponível.")

try:
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        connection_timeout=10,
    )
except Exception as exc:
    print("\nERRO: o Python não conseguiu conectar ao MySQL.")
    print("Confira principalmente DB_HOST, DB_USER, DB_PASSWORD e DB_NAME.")
    print(f"Detalhe técnico: {exc}")
    sys.exit(1)

print("3/5 Python conseguiu conectar ao MySQL.")

cursor = conexao.cursor()
try:
    cursor.execute("SHOW TABLES")
    tabelas = {linha[0] for linha in cursor.fetchall()}
    esperadas = {"usuarios", "tarefas", "passos"}
    ausentes = esperadas - tabelas
    if ausentes:
        print("ERRO: o banco existe, mas faltam tabelas:", ", ".join(sorted(ausentes)))
        sys.exit(1)

    print("4/5 Estrutura do banco encontrada: usuarios, tarefas e passos.")

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    usuarios = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tarefas")
    tarefas = cursor.fetchone()[0]
    print(f"    usuários cadastrados: {usuarios}")
    print(f"    tarefas cadastradas:  {tarefas}")
finally:
    cursor.close()
    conexao.close()

try:
    from data.data_manager import carregar_dados
    dados = carregar_dados()
except Exception as exc:
    print("ERRO: o banco funciona, mas o TPaC não conseguiu carregar os dados.")
    print(f"Detalhe técnico: {exc}")
    sys.exit(1)

if not dados:
    print("ERRO: o TPaC conectou, mas não encontrou os dados de exemplo.")
    sys.exit(1)

print("5/5 O próprio TPaC carregou os dados pelo data_manager.py.")
print()
print("SUCESSO: IMPLANTAÇÃO VALIDADA.")
print("O ambiente remoto possui Python, dependências, MySQL, banco e conexão funcionando.")
print("=" * 64)
