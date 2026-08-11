# GUIA DO PROFESSOR — Aula 02
## Implantando o TPaC no GitHub Codespaces

Este guia foi escrito para conduzir a aula mesmo sem domínio avançado de Linux, MySQL ou DevOps.

A ideia central é simples:

> O aluno recebe o código do TPaC e precisa preparar um ambiente remoto para que o sistema funcione com Python + MySQL.

Nada precisa ser instalado no Windows do laboratório.

---

# 1. O que já está preparado no repositório

Quando o aluno cria o Codespace, o GitHub usa a pasta `.devcontainer` para montar dois serviços:

```text
┌───────────────────────────────┐
│ GitHub Codespaces             │
│                               │
│  app                          │
│  ├─ Linux                     │
│  ├─ Python                    │
│  ├─ cliente MySQL             │
│  └─ arquivos do TPaC          │
│            │                  │
│            │ rede interna     │
│            ▼                  │
│  db                           │
│  └─ MySQL 8.4                 │
│                               │
└───────────────────────────────┘
```

O serviço `db` já inicia o servidor MySQL.

O aluno ainda precisa:

1. verificar o ambiente;
2. criar o `.venv`;
3. instalar `requirements.txt`;
4. criar `.env` a partir do exemplo;
5. comprovar que o MySQL responde;
6. executar `database.sql`;
7. executar `python main.py`;
8. testar persistência.

Isso preserva a aprendizagem de implantação sem exigir permissão de administrador no computador da escola.

---

# 2. Antes da aula — teste obrigatório do professor

Faça isso antes de enviar o link aos alunos.

## 2.1 Abra o repositório

Abra:

```text
mrcelobento-code/tpac-devops-modelo
```

## 2.2 Crie um Codespace de teste

No GitHub:

```text
Code
→ Codespaces
→ Create codespace on main
```

Espere o ambiente carregar completamente.

## 2.3 Teste os comandos exatamente na ordem dos alunos

No terminal:

```bash
pwd
ls
python --version
```

Depois:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Depois:

```bash
cp .env.example .env
cat .env
```

Teste o banco:

```bash
mysqladmin -h db -u root -proot ping
```

Esperado:

```text
mysqld is alive
```

Importe:

```bash
mysql -h db -u root -proot < database.sql
```

Confira:

```bash
mysql -h db -u tpac -ptpac -D tpac_db -e "SHOW TABLES;"
```

Esperado:

```text
passos
tarefas
usuarios
```

Execute:

```bash
python main.py
```

Entre com:

```text
Matheus
```

Crie uma tarefa, encerre o sistema, rode novamente e confirme que a tarefa permaneceu.

Por fim:

```bash
bash scripts/verificar_ambiente.sh
```

A meta é não haver `❌`.

---

# 3. O que explicar aos alunos antes de abrir o GitHub

Não comece com comandos.

Projete a ideia:

```text
ANTES
Computador já preparado
→ TPaC funciona

HOJE
Ambiente novo
→ o que é necessário preparar?
```

Pergunte à turma:

> Se eu copiar somente a pasta do programa para outro computador, ele obrigatoriamente funciona?

Conduza as respostas para:

```text
código
Python
bibliotecas
configuração
banco
execução
```

Depois diga:

> Hoje vamos provar isso usando o TPaC.

---

# 4. Frase que evita a principal dúvida da aula

Diga de forma explícita:

> Tudo que aparecer no terminal do Codespaces está acontecendo no computador remoto do GitHub. Não estamos instalando nada no Windows do laboratório.

Quando o aluno executar:

```bash
python -m pip install -r requirements.txt
```

explique novamente:

> Esse `install` instala bibliotecas no ambiente remoto. Não pede administrador do computador do SENAC/SENAI.

---

# 5. Ordem de condução sugerida — 4 horas

## Bloco 1 — 0:00 até 0:30

Objetivo: conta, cópia e Codespace aberto.

Professor projeta uma tela por vez.

Não mostre cinco passos de uma vez.

Ordem:

```text
1. abrir GitHub
2. abrir repositório-modelo
3. Use this template
4. Create a new repository
5. Code
6. Codespaces
7. Create codespace on main
```

Só continue quando a maioria estiver com o editor aberto.

## Bloco 2 — 0:30 até 1:10

Objetivo: entender Linux apenas no necessário.

Comandos:

```bash
pwd
ls
python --version
```

Explique:

- `pwd`: onde estou;
- `ls`: o que existe aqui;
- `python --version`: este ambiente consegue executar Python?

Não transforme isso em aula de Linux.

## Bloco 3 — 1:10 até 1:50

Objetivo: preparar o Python.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Mostre o `requirements.txt` antes do `pip install`.

Pergunte:

> Por que o Python sozinho não é suficiente?

Resposta esperada: porque o projeto depende de bibliotecas externas.

## Bloco 4 — 1:50 até 2:25

Objetivo: configuração.

```bash
cp .env.example .env
cat .env
```

Explique cada item:

```text
DB_HOST=db       quem é o servidor
DB_PORT=3306     por qual porta
DB_USER=tpac     qual usuário
DB_PASSWORD=tpac qual senha
DB_NAME=tpac_db  qual banco
```

Ponto importante:

> No projeto antigo executado localmente, o banco podia usar `localhost`. Aqui o MySQL está em outro serviço do ambiente; por isso o host é `db`.

## Bloco 5 — 2:25 até 3:00

Objetivo: MySQL e banco.

Primeiro teste somente o servidor:

```bash
mysqladmin -h db -u root -proot ping
```

Pergunte:

> O TPaC já está funcionando?

Resposta: não. Só comprovamos que o servidor MySQL está vivo.

Depois importe:

```bash
mysql -h db -u root -proot < database.sql
```

E comprove:

```bash
mysql -h db -u tpac -ptpac -D tpac_db -e "SHOW TABLES;"
```

## Bloco 6 — 3:00 até 3:30

Objetivo: executar e validar.

```bash
python main.py
```

Entre com `Matheus`.

Crie uma tarefa chamada:

```text
Teste de implantação
```

Encerre e execute novamente.

A pergunta central:

> O dado continuou existindo depois de reiniciar o programa?

Se sim, o aluno comprovou persistência em MySQL.

## Bloco 7 — 3:30 até 3:50

Objetivo: diagnóstico.

Use UM erro proposital, não vários ao mesmo tempo.

Sugestão mais didática:

Abra `.env` e troque:

```text
DB_HOST=db
```

por:

```text
DB_HOST=servidor_errado
```

Salve e execute:

```bash
python main.py
```

Deixe os alunos lerem o erro.

Pergunte:

```text
Python sumiu? Não.
requirements sumiram? Não.
Banco foi apagado? Não.
Qual configuração acabamos de alterar?
```

Depois restaure:

```text
DB_HOST=db
```

Teste novamente.

Isso mostra que um sistema depende não apenas do código, mas também da configuração do ambiente.

## Bloco 8 — 3:50 até 4:00

Execute:

```bash
bash scripts/verificar_ambiente.sh
```

Faça commit e sincronize.

Pare o Codespace.

---

# 6. Erros mais prováveis e exatamente o que fazer

## Erro: `python: command not found`

Isso não deveria acontecer neste ambiente.

Primeiro confirme que o Codespace terminou de carregar.

Não peça para instalar Python no Windows.

## Erro: `No module named mysql`

Causa provável: dependências não instaladas ou `.venv` não ativado.

Faça:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Depois teste:

```bash
python -c "import mysql.connector; print('OK')"
```

## Erro: `No module named dotenv`

Mesma correção:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Erro relacionado a `.env`

Confira se existe:

```bash
ls -a
```

Se não existir:

```bash
cp .env.example .env
```

Depois:

```bash
cat .env
```

## Erro: não consegue encontrar `db`

Confira:

```bash
cat .env
```

A linha precisa ser:

```text
DB_HOST=db
```

Não use `localhost` neste laboratório.

## Erro: `Unknown database 'tpac_db'`

Execute:

```bash
mysql -h db -u root -proot < database.sql
```

Depois confira:

```bash
mysql -h db -u tpac -ptpac -D tpac_db -e "SHOW TABLES;"
```

## Erro: `Access denied`

Confira o `.env`:

```text
DB_USER=tpac
DB_PASSWORD=tpac
```

## Erro: `Can't connect to MySQL server`

Primeiro:

```bash
mysqladmin -h db -u root -proot ping
```

Se acabou de criar o Codespace, espere alguns segundos.

Se continuar falhando, abra o terminal do Codespaces e não altere código Python ainda. O problema está antes da aplicação.

## Erro: `can't open file main.py`

Execute:

```bash
pwd
ls
```

Se `main.py` não aparecer, o terminal está no diretório errado.

---

# 7. O que NÃO ensinar nesta aula

Evite aprofundar agora:

- Docker;
- sintaxe de Docker Compose;
- administração completa de MySQL;
- Nginx;
- Apache;
- AWS;
- redes avançadas;
- permissões Linux avançadas;
- CI/CD.

Essas tecnologias podem aparecer depois.

Para o aluno, o Codespace é simplesmente o **ambiente Linux remoto da prática**.

A infraestrutura `.devcontainer` foi preparada pelo professor para eliminar barreiras do laboratório.

---

# 8. O que o aluno precisa aprender de verdade

Ao final, o aluno deve conseguir dizer:

> Para implantar um sistema não basta copiar código. O ambiente precisa ter o runtime correto, dependências, configurações e serviços necessários, como o banco de dados. Depois precisamos executar e testar se os dados continuam funcionando.

Essa é a evidência conceitual principal da aula.

---

# 9. Checklist do professor antes de liberar a turma

Confirme:

```text
[ ] repositório está público
[ ] repositório está marcado como Template repository
[ ] Codespace do professor abriu
[ ] python --version funcionou
[ ] requirements instalou
[ ] .env.example existe
[ ] MySQL respondeu
[ ] database.sql importou
[ ] tabelas apareceram
[ ] python main.py abriu o menu
[ ] perfil Matheus apareceu
[ ] persistência funcionou
[ ] verificar_ambiente.sh terminou sem erro
```

Não libere a atividade antes desse teste.

---

# 10. Evidência que pode ser solicitada ao aluno

Peça apenas o necessário:

```text
1. link do repositório pessoal
2. print do TPaC funcionando no terminal
3. resultado de bash scripts/verificar_ambiente.sh
4. problema encontrado
5. como resolveu
```

Assim a entrega comprova execução e diagnóstico, não apenas cópia de comandos.
