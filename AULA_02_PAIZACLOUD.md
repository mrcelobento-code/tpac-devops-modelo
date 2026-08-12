# AULA 02 — Implantando o TPaC no PaizaCloud

## Por que estamos usando este ambiente

O computador do laboratório não será alterado. Nada será instalado no Windows.

O PaizaCloud fornece um servidor Linux temporário dentro do navegador. É nele que vamos trabalhar com terminal, Python e MySQL.

> IMPORTANTE: no plano gratuito, trate este servidor como temporário. O código-base continua guardado no GitHub.

---

## ETAPA 1 — Criar sua conta

1. Abra o navegador.
2. Entre em `paiza.cloud`.
3. Clique em **Sign up for FREE**.
4. Informe seu e-mail, escolha um nome de usuário e crie uma senha.
5. Conclua o cadastro.
6. Entre na sua conta.

Não instale programa nenhum no computador.

---

## ETAPA 2 — Criar o servidor Linux

1. Dentro do PaizaCloud, escolha a opção para criar um novo servidor.
2. Use o plano gratuito.
3. Aguarde o ambiente abrir.
4. Localize o **Terminal**.

Quando o terminal estiver aberto, pare e confira com o professor antes de continuar.

---

## ETAPA 3 — Descobrir onde você está

Digite um comando por vez e pressione Enter depois de cada linha:

```bash
pwd
```

O comando mostra em qual pasta do Linux você está.

Agora:

```bash
ls
```

O comando mostra o que existe nessa pasta.

Agora confirme o Python:

```bash
python3 --version
```

Depois confirme o MySQL:

```bash
mysql --version
```

Se algum desses dois últimos comandos disser `command not found`, pare e chame o professor.

---

## ETAPA 4 — Trazer o TPaC do GitHub

Digite:

```bash
git clone https://github.com/mrcelobento-code/tpac-devops-modelo.git
```

Aguarde voltar para a linha de comando.

Entre na pasta do projeto:

```bash
cd tpac-devops-modelo
```

Confira:

```bash
ls
```

Você deverá encontrar arquivos como:

```text
main.py
database.sql
requirements.txt
requirements-paiza.txt
core
data
ui
scripts
```

---

## ETAPA 5 — Entender a missão antes de executar

Neste momento você TEM o código do TPaC, mas isso não significa que o sistema já está implantado.

Ainda precisamos verificar e preparar:

```text
Python
+
bibliotecas do projeto
+
MySQL
+
banco tpac_db
+
configuração da conexão
=
TPaC funcionando
```

---

## ETAPA 6 — Preparação assistida

Para a primeira execução da turma, use o roteiro de recuperação preparado pelo professor:

```bash
bash scripts/preparar_paiza.sh
```

Leia o que aparece na tela. O script verifica o ambiente remoto, prepara o banco didático, instala as bibliotecas Python necessárias dentro do servidor remoto, cria o `.env` e importa `database.sql`.

Nada disso é instalado no Windows do laboratório.

Se aparecer `PREPARAÇÃO CONCLUÍDA`, continue.

Se aparecer `ERRO`, não tente comandos aleatórios. Mostre a mensagem ao professor.

---

## ETAPA 7 — Executar o TPaC

Digite:

```bash
python3 main.py
```

O menu do sistema deve aparecer no terminal.

Entre com o perfil de exemplo `Matheus` e confira a tarefa existente.

---

## ETAPA 8 — Comprovar que Python e MySQL estão conversando

Dentro do TPaC:

1. crie uma tarefa;
2. marque ou altere uma tarefa;
3. saia do sistema;
4. execute novamente:

```bash
python3 main.py
```

Se a alteração continuar lá, o sistema conseguiu salvar no banco.

---

## ETAPA 9 — Diagnóstico de falha

Agora o professor indicará UMA configuração para alterar de propósito.

O objetivo não é simplesmente quebrar o sistema. O objetivo é observar:

1. qual mensagem apareceu;
2. qual componente deixou de funcionar;
3. onde estava a configuração incorreta;
4. qual correção fez o sistema voltar.

Depois da correção, execute novamente:

```bash
python3 main.py
```

---

## ENTREGA DA AULA

Registre:

- nome;
- versão do Python mostrada pelo terminal;
- versão do MySQL mostrada pelo terminal;
- evidência do TPaC funcionando;
- erro provocado;
- mensagem de erro observada;
- correção realizada;
- evidência final do TPaC funcionando novamente.

Não é necessário instalar nada no computador do laboratório.
