#!/usr/bin/env bash
set -u

printf '\n============================================================\n'
printf ' TPAC DEVOPS — PREPARAÇÃO DO PAIZACLOUD\n'
printf '============================================================\n'
printf 'Este script atua SOMENTE no servidor Linux remoto do PaizaCloud.\n'
printf 'Ele não instala nada no computador do laboratório.\n\n'

if ! command -v python3 >/dev/null 2>&1; then
  echo 'ERRO: python3 não foi encontrado neste servidor.'
  exit 1
fi

if ! command -v mysql >/dev/null 2>&1; then
  echo 'ERRO: o cliente MySQL não foi encontrado neste servidor.'
  exit 1
fi

echo '[1/7] Python encontrado:'
python3 --version

echo '\n[2/7] MySQL encontrado:'
mysql --version

echo '\n[3/7] Tentando iniciar o banco de dados...'
if command -v service >/dev/null 2>&1; then
  sudo service mysql start >/dev/null 2>&1 || sudo service mariadb start >/dev/null 2>&1 || true
fi

ADMIN_MODE=''
if sudo mysql -e 'SELECT 1;' >/dev/null 2>&1; then
  ADMIN_MODE='sudo mysql'
elif mysql -uroot -e 'SELECT 1;' >/dev/null 2>&1; then
  ADMIN_MODE='mysql -uroot'
fi

if [ -z "$ADMIN_MODE" ]; then
  echo 'ERRO: o MySQL existe, mas não consegui entrar como administrador.'
  echo 'Mostre esta mensagem ao professor antes de continuar.'
  exit 2
fi

echo 'Banco iniciado e acesso administrativo confirmado.'

echo '\n[4/7] Criando banco e usuário didático...'
$ADMIN_MODE <<'SQL'
CREATE DATABASE IF NOT EXISTS tpac_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'tpac'@'localhost' IDENTIFIED BY 'tpac';
ALTER USER 'tpac'@'localhost' IDENTIFIED BY 'tpac';
GRANT ALL PRIVILEGES ON tpac_db.* TO 'tpac'@'localhost';
FLUSH PRIVILEGES;
SQL

echo '\n[5/7] Instalando apenas as bibliotecas Python do projeto...'
python3 -m pip install --user -r requirements-paiza.txt

echo '\n[6/7] Criando o arquivo .env do laboratório...'
cp aula02/paiza.env .env

echo '\n[7/7] Importando a estrutura do TPaC...'
$ADMIN_MODE < database.sql

printf '\n============================================================\n'
printf ' PREPARAÇÃO CONCLUÍDA\n'
printf '============================================================\n'
printf 'Agora execute:\n\n'
printf '  python3 main.py\n\n'
printf 'Se o menu do TPaC aparecer, a implantação funcionou.\n'
printf '============================================================\n\n'
