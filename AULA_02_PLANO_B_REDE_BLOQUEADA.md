# AULA 02 — PLANO B QUANDO O CODESPACES É BLOQUEADO

Use este roteiro quando o navegador mostrar **“Oh no, it looks like you are offline!”** ao abrir o Codespace.

Neste plano, o aluno continua usando apenas o navegador. Nada é instalado no computador da escola.

## O que muda

Em vez de o aluno entrar num terminal remoto interativo, o próprio GitHub cria por alguns minutos uma máquina Linux de laboratório, instala Python, inicia MySQL, importa o banco e testa o TPaC. O aluno acompanha cada etapa pela aba **Actions**.

O objetivo da aula continua sendo entender o que um sistema precisa para funcionar em outro ambiente:

```text
código
  ↓
Python
  ↓
dependências
  ↓
MySQL
  ↓
banco tpac_db
  ↓
configuração
  ↓
conexão
  ↓
validação
```

---

# PARTE 1 — CRIAR A CÓPIA DO ALUNO

1. Abra o repositório-modelo do professor.
2. Clique em **Use this template**.
3. Clique em **Create a new repository**.
4. Em **Repository name**, use `tpac-devops-seunome`.
5. Para esta atividade, prefira **Public**, pois não há dados reais nem senhas reais neste laboratório.
6. Clique em **Create repository**.
7. Espere abrir a cópia do seu próprio repositório.

Confirme no topo da tela que aparece o seu repositório, e não `tpac-devops-modelo`.

---

# PARTE 2 — PRIMEIRA IMPLANTAÇÃO SEM CODESPACES

## Passo 1 — Abra Actions

Na barra superior do seu repositório, clique em **Actions**.

Na coluna esquerda procure:

**Aula 02 - Implantação TPaC sem Codespaces**

Clique nesse nome.

## Passo 2 — Execute o laboratório

No lado direito da tela, clique em **Run workflow**.

Mantenha a branch `main`.

Clique novamente no botão verde **Run workflow**.

Aguarde alguns segundos e atualize a página se necessário.

Vai aparecer uma execução na lista.

### O que significam as cores

- bolinha amarela: ainda está executando;
- marca verde: terminou corretamente;
- X vermelho: alguma etapa falhou.

## Passo 3 — Abra a execução

Clique no nome da execução.

Depois clique no bloco chamado:

**validar-implantacao**

Você verá uma lista de etapas.

O GitHub estará fazendo, sozinho, em uma máquina Linux temporária:

1. baixar os arquivos do TPaC;
2. preparar Python;
3. iniciar um servidor MySQL;
4. instalar `mysql-connector-python` e `python-dotenv`;
5. importar `database.sql`;
6. testar a configuração;
7. testar se o Python conecta ao banco;
8. testar se existem as tabelas `usuarios`, `tarefas` e `passos`;
9. chamar o próprio `data_manager.py` do TPaC;
10. informar se a implantação funcionou.

Se tudo estiver correto, no final aparecerá:

```text
SUCESSO: IMPLANTAÇÃO VALIDADA.
```

---

# PARTE 3 — ENTENDA A CONFIGURAÇÃO

Volte para a aba **Code** do repositório.

Abra a pasta:

`aula02`

Depois clique em:

`configuracao.env`

Você verá:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=tpac
DB_PASSWORD=tpac
DB_NAME=tpac_db
```

Leia linha por linha:

- `DB_HOST`: onde está o banco;
- `DB_PORT`: porta usada pelo MySQL;
- `DB_USER`: usuário que o Python usará;
- `DB_PASSWORD`: senha desse usuário;
- `DB_NAME`: nome do banco que o TPaC procura.

Não é necessário decorar. O importante é entender que o Python precisa dessas informações para chegar ao banco certo.

---

# PARTE 4 — PROVOQUE UM ERRO DE VERDADE

Agora vamos quebrar a implantação de propósito.

## Passo 1 — Abra `aula02/configuracao.env`

Clique no ícone de lápis **Edit this file**.

Localize:

```env
DB_NAME=tpac_db
```

Troque somente essa linha para:

```env
DB_NAME=tpac_db_errado
```

Não mude mais nada.

## Passo 2 — Salve

Clique em **Commit changes...**.

Na mensagem, escreva:

```text
teste: simula banco configurado incorretamente
```

Clique em **Commit changes**.

Esse commit dispara automaticamente um novo laboratório.

## Passo 3 — Veja o erro

Clique em **Actions**.

Abra a execução mais nova.

Ela deverá terminar com X vermelho.

Abra `validar-implantacao` e procure a etapa de validação.

A mensagem deverá indicar que o Python não conseguiu conectar ao banco configurado.

Pergunta para responder:

> O MySQL deixou de existir ou foi a configuração do sistema que apontou para o lugar errado?

Resposta esperada: o servidor continua existindo; a aplicação foi configurada para procurar um banco com nome incorreto.

---

# PARTE 5 — CORRIJA

Volte para:

`Code → aula02 → configuracao.env → Edit this file`

Corrija:

```env
DB_NAME=tpac_db
```

Clique em **Commit changes...**.

Mensagem:

```text
fix: corrige nome do banco do TPaC
```

Clique em **Commit changes**.

Depois abra **Actions** novamente.

A nova execução deve terminar verde.

Quando aparecer:

```text
SUCESSO: IMPLANTAÇÃO VALIDADA.
```

você comprovou que uma configuração errada derruba a aplicação e que a correção devolve o funcionamento.

---

# ENTREGA DA AULA

Entregue:

1. link do seu repositório;
2. print da execução com X vermelho;
3. print da execução verde depois da correção;
4. resposta curta: **qual configuração estava errada e por que o TPaC não conseguia acessar o banco?**

---

# IMPORTANTE

Este plano não substitui para sempre um terminal Linux interativo. Ele é a alternativa segura quando a rede da instituição bloqueia a conexão em tempo real usada pelo Codespaces.

A vantagem pedagógica é que o aluno ainda consegue observar uma implantação real executada em Linux na nuvem, com Python e MySQL reais, além de provocar, diagnosticar e corrigir uma falha de configuração.
