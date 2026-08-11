# AULA 02 — Implantando o TPaC em um ambiente Linux remoto

## Missão da aula

Hoje você não vai construir um sistema novo.

O TPaC já existe. Sua missão é fazer esse sistema funcionar em **outro ambiente**, no GitHub Codespaces.

Ao final, você deverá conseguir explicar este caminho:

```text
CÓDIGO DO TPAC
      ↓
AMBIENTE LINUX REMOTO
      ↓
PYTHON + DEPENDÊNCIAS
      ↓
CONFIGURAÇÃO .env
      ↓
MYSQL + tpac_db
      ↓
python main.py
      ↓
TPAC FUNCIONANDO
```

> Não pule etapas. Se alguma etapa não der o resultado esperado, pare nela e resolva antes de avançar.

---

# PARTE 1 — Criar sua cópia do projeto

## Passo 1 — Entre na sua conta do GitHub

1. Abra o navegador.
2. Entre no GitHub.
3. Confirme se seu nome ou foto aparece no canto superior direito.

**Só avance se você estiver logado na sua própria conta.**

## Passo 2 — Abra o repositório-modelo do professor

Use o link fornecido pelo professor.

Você deve estar vendo um repositório chamado:

```text
tpac-devops-modelo
```

## Passo 3 — Crie sua própria cópia

1. Localize o botão **Use this template**.
2. Clique nele.
3. Clique em **Create a new repository**.
4. Em **Owner**, confirme que aparece sua conta.
5. Em **Repository name**, use:

```text
tpac-devops-seunome
```

Exemplo:

```text
tpac-devops-maria
```

6. Clique em **Create repository**.

### Como saber se deu certo?

No alto da página deve aparecer algo parecido com:

```text
seu-usuario / tpac-devops-seunome
```

Se ainda aparece o usuário do professor, você ainda está no projeto original.

---

# PARTE 2 — Abrir o computador Linux remoto

## Passo 4 — Abra o Codespaces

Dentro da SUA cópia:

1. Clique no botão verde **Code**.
2. Clique na aba **Codespaces**.
3. Clique em **Create codespace on main**.
4. Aguarde.

Na primeira abertura o GitHub precisa montar o ambiente. Isso pode levar alguns minutos.

### Não faça

- não instale VS Code no Windows;
- não instale Python no Windows;
- não instale MySQL no Windows;
- não instale Docker no Windows.

Tudo isso foi preparado no ambiente remoto.

## Passo 5 — Reconheça a tela

Quando terminar de carregar, você verá uma tela parecida com o VS Code.

Observe apenas três regiões:

```text
ESQUERDA   → arquivos do projeto
CENTRO     → arquivo que você abriu
EMBAIXO    → terminal
```

Se o terminal não estiver aberto:

**Terminal → New Terminal**.

---

# PARTE 3 — Conhecer o servidor antes de mexer nele

## Passo 6 — Descubra onde você está

No terminal, digite:

```bash
pwd
```

`pwd` significa: **mostre em qual diretório eu estou**.

Resultado esperado: um caminho terminado em algo relacionado ao projeto.

Agora digite:

```bash
ls
```

`ls` significa: **liste o que existe neste diretório**.

Você deve encontrar nomes como:

```text
main.py
requirements.txt
database.sql
core
data
ui
```

### Se main.py não aparecer

Pare. Você provavelmente não está no diretório do projeto.

Não execute `python main.py` enquanto esse arquivo não aparecer no resultado de `ls`.

## Passo 7 — Verifique o Python

Digite:

```bash
python --version
```

Você deverá receber uma resposta começando com:

```text
Python 3
```

### O que acabamos de provar?

O sistema é feito em Python. Antes de tentar executá-lo, comprovamos que o ambiente remoto possui Python.

---

# PARTE 4 — Preparar o Python para o TPaC

## Passo 8 — Crie o ambiente virtual

Digite:

```bash
python -m venv .venv
```

Aguarde o terminal voltar.

Agora ative:

```bash
source .venv/bin/activate
```

### Como saber se ativou?

Normalmente aparece isto no começo da linha:

```text
(.venv)
```

### O que é isso?

É um espaço separado para as bibliotecas deste projeto. As instalações que faremos agora ficam no ambiente remoto e não modificam o Windows da escola.

## Passo 9 — Veja do que o projeto depende

No explorador de arquivos, clique em:

```text
requirements.txt
```

Você encontrará:

```text
mysql-connector-python==9.1.0
python-dotenv==1.0.1
```

Tradução:

- `mysql-connector-python`: permite que o Python converse com o MySQL;
- `python-dotenv`: permite que o Python leia o arquivo `.env`.

Agora instale:

```bash
python -m pip install -r requirements.txt
```

Espere o comando terminar.

### Se aparecer texto vermelho

Não execute o próximo passo imediatamente. Leia as últimas linhas do erro e mostre ao professor.

---

# PARTE 5 — Preparar a configuração do TPaC

## Passo 10 — Crie o arquivo .env

O repositório não traz uma senha real em `.env`. Ele traz somente um modelo chamado:

```text
.env.example
```

Crie sua cópia:

```bash
cp .env.example .env
```

Confira:

```bash
cat .env
```

Você deverá enxergar:

```text
DB_HOST=db
DB_PORT=3306
DB_USER=tpac
DB_PASSWORD=tpac
DB_NAME=tpac_db
```

### Entenda linha por linha

`DB_HOST=db`  
O banco não está no mesmo contêiner do Python. O nome `db` identifica o serviço MySQL do nosso laboratório.

`DB_PORT=3306`  
É a porta padrão usada pelo MySQL.

`DB_USER=tpac`  
É o usuário que a aplicação usará para acessar o banco.

`DB_PASSWORD=tpac`  
É uma senha simples criada exclusivamente para este laboratório.

`DB_NAME=tpac_db`  
É o banco que o TPaC espera encontrar.

---

# PARTE 6 — Verificar o servidor MySQL

## Passo 11 — Pergunte se o MySQL está vivo

Digite:

```bash
mysqladmin -h db -u root -proot ping
```

Resultado esperado:

```text
mysqld is alive
```

### O que esse teste significa?

Ainda não estamos testando o TPaC.

Estamos testando somente isto:

```text
terminal → consegue encontrar → servidor MySQL
```

Se aparecer `mysqld is alive`, o servidor de banco está respondendo.

### Se falhar

Espere aproximadamente 20 segundos e execute novamente.

Se continuar falhando, chame o professor antes de alterar qualquer arquivo.

---

# PARTE 7 — Criar o banco do sistema

## Passo 12 — Leia o database.sql antes de executar

No explorador, abra:

```text
database.sql
```

Procure estas três tabelas:

```text
usuarios
tarefas
passos
```

O arquivo também cria um perfil de teste chamado `Matheus`.

## Passo 13 — Importe o banco

Volte ao terminal.

Digite exatamente:

```bash
mysql -h db -u root -proot < database.sql
```

O terminal pode simplesmente voltar para uma nova linha sem mostrar mensagem.

Isso não significa que nada aconteceu.

Agora vamos comprovar.

## Passo 14 — Liste as tabelas

Digite:

```bash
mysql -h db -u tpac -ptpac -D tpac_db -e "SHOW TABLES;"
```

Resultado esperado:

```text
Tables_in_tpac_db
passos
tarefas
usuarios
```

### Pare e confira

Só avance para executar o TPaC se as três tabelas aparecerem.

---

# PARTE 8 — Executar o TPaC

## Passo 15 — Rode o sistema

Digite:

```bash
python main.py
```

Você deverá ver um menu semelhante a:

```text
SISTEMA TPAC ACESSIBLE

1. Entrar com perfil existente
2. Criar novo perfil customizado
3. Encerrar
```

### O que conseguimos até aqui?

Antes:

```text
arquivos do TPaC
```

Agora:

```text
Linux remoto
+ Python
+ bibliotecas
+ configuração
+ servidor MySQL
+ banco tpac_db
= TPaC executando
```

Isso é a implantação que estamos estudando.

---

# PARTE 9 — Testar a persistência

## Passo 16 — Entre com o perfil de teste

1. Digite `1`.
2. Quando pedir o nome do perfil, digite:

```text
Matheus
```

3. Entre em **Atividades Educacionais**.
4. Confirme que existe uma tarefa de exemplo.

## Passo 17 — Crie uma informação nova

Crie uma tarefa com um nome fácil de reconhecer, por exemplo:

```text
Teste de implantação
```

Volte ao menu e encerre o programa.

## Passo 18 — Execute novamente

```bash
python main.py
```

Entre novamente com `Matheus`.

### Pergunta de validação

A tarefa `Teste de implantação` continua aparecendo?

**Se sim:** o sistema salvou no MySQL e recuperou depois de reiniciar.

**Se não:** existe algum problema de persistência que precisa ser investigado.

---

# PARTE 10 — Verificação automática

## Passo 19 — Saia do TPaC

Volte até o menu inicial e escolha **Encerrar**.

Agora execute:

```bash
bash scripts/verificar_ambiente.sh
```

A meta é chegar a uma tela sem itens marcados com `❌`.

---

# PARTE 11 — Desafio de diagnóstico

O professor poderá indicar uma alteração proposital para fazer o sistema parar de funcionar.

Quando isso acontecer, não saia alterando arquivos aleatoriamente.

Siga esta ordem:

```text
1. LEIA A MENSAGEM DE ERRO
2. IDENTIFIQUE EM QUAL ETAPA OCORREU
3. CONFIRA O ARQUIVO RELACIONADO
4. ALTERE UMA COISA
5. TESTE NOVAMENTE
```

Perguntas úteis:

- O Python está funcionando?
- As dependências foram instaladas?
- O `.env` existe?
- `DB_HOST` está correto?
- O MySQL está respondendo?
- O banco `tpac_db` existe?
- As tabelas foram criadas?
- Você está na pasta onde existe `main.py`?

---

# PARTE 12 — Registre sua evidência

Antes de terminar, registre:

```text
Nome do aluno:
Nome do repositório:

Ambiente usado: GitHub Codespaces
Sistema operacional: Linux remoto
Python encontrado: __________________
Banco: MySQL
Nome do banco: tpac_db
Porta: 3306
Arquivo inicial: main.py

Problema encontrado durante a implantação:
____________________________________________________

Como foi resolvido:
____________________________________________________

Evidência final:
print do terminal com o TPaC funcionando
```

---

# PARTE 13 — Salve seu trabalho

## Passo 20 — Faça o commit

Na barra lateral esquerda, clique em **Source Control**.

Você verá os arquivos alterados.

Na caixa de mensagem escreva:

```text
Implantação inicial do TPaC
```

Clique em **Commit**.

Depois clique em **Sync Changes**.

### O que isso faz?

O Codespace é o local onde você está trabalhando agora.

O repositório GitHub é onde queremos manter o código registrado.

---

# PARTE 14 — Pare o Codespace

Fechar apenas a aba do navegador não é o mesmo que parar o ambiente.

Ao terminar:

1. volte ao GitHub;
2. abra a área **Codespaces**;
3. encontre seu Codespace;
4. clique nos três pontos `...`;
5. clique em **Stop codespace**.

---

# O que você precisa conseguir explicar no final

Sem decorar uma frase, explique com suas palavras:

> Por que apenas copiar os arquivos do TPaC para outro computador não é suficiente para o sistema funcionar?

Sua resposta deve citar pelo menos:

```text
Python
bibliotecas
configuração
MySQL
banco de dados
execução
```
