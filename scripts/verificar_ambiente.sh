#!/usr/bin/env bash

# Verificação didática do laboratório TPaC.
# Não altera o projeto: apenas confere o que já foi preparado.

OK=0
ERRO=0

passou() {
  printf '✅ %s\n' "$1"
  OK=$((OK + 1))
}

falhou() {
  printf '❌ %s\n' "$1"
  ERRO=$((ERRO + 1))
}

printf '\n============================================================\n'
printf ' VERIFICAÇÃO DO AMBIENTE TPAC\n'
printf '============================================================\n'

if command -v python >/dev/null 2>&1; then
  passou "Python disponível: $(python --version 2>&1)"
else
  falhou "Python não foi encontrado."
fi

if [ -f .env ]; then
  passou "Arquivo .env existe."
else
  falhou "Arquivo .env não existe. Execute: cp .env.example .env"
fi

if python -c "import mysql.connector, dotenv" >/dev/null 2>&1; then
  passou "Dependências Python instaladas."
else
  falhou "Dependências ausentes. Ative .venv e execute: python -m pip install -r requirements.txt"
fi

if mysqladmin -h db -u root -proot ping >/dev/null 2>&1; then
  passou "Servidor MySQL está respondendo."
else
  falhou "Servidor MySQL não respondeu. Aguarde um pouco e teste novamente."
fi

if mysql -h db -u tpac -ptpac -D tpac_db -N -e "SHOW TABLES LIKE 'usuarios';" 2>/dev/null | grep -q usuarios; then
  passou "Banco tpac_db foi importado e possui a tabela usuarios."
else
  falhou "Banco ainda não está preparado. Execute: mysql -h db -u root -proot < database.sql"
fi

if python -m py_compile main.py core/tarefas.py core/ia_service.py data/data_manager.py ui/menus.py ui/utils.py >/dev/null 2>&1; then
  passou "Arquivos Python passaram pela verificação de sintaxe."
else
  falhou "Existe erro de sintaxe em algum arquivo Python."
fi

printf '\n------------------------------------------------------------\n'
printf 'Itens corretos: %s\n' "$OK"
printf 'Itens com problema: %s\n' "$ERRO"
printf '------------------------------------------------------------\n'

if [ "$ERRO" -eq 0 ]; then
  printf 'AMBIENTE PRONTO. Agora execute: python main.py\n\n'
  exit 0
fi

printf 'Corrija os itens marcados com ❌ e execute este script novamente.\n\n'
exit 1
