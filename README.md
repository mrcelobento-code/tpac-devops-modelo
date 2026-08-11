# TPaC DevOps — Repositório-modelo da turma

Este repositório foi preparado para a UC **Práticas DevOps em Projetos Web** usando o TPaC como sistema central da aula.

> **Importante:** o aluno não precisa instalar Python, MySQL, VS Code ou Docker no computador do SENAC/SENAI. O trabalho acontece dentro do **GitHub Codespaces**, no navegador.

## O que existe neste projeto

```text
tpac-devops-modelo/
├── .devcontainer/        ambiente remoto do Codespaces
├── core/                 regras das tarefas e apoio simulado
├── data/                 conexão Python ↔ MySQL
├── ui/                   menus do terminal
├── scripts/              verificação do laboratório
├── database.sql          cria o banco e as tabelas
├── main.py               inicia o TPaC
├── requirements.txt      bibliotecas Python
├── .env.example          modelo da configuração do banco
├── AULA_02_ALUNO.md      roteiro passo a passo do estudante
└── GUIA_PROFESSOR.md     roteiro de condução da aula
```

## Para o aluno: como começar

### 1. Faça sua própria cópia

Na página deste repositório, clique em **Use this template** → **Create a new repository**.

Nome sugerido:

```text
tpac-devops-seunome
```

### 2. Abra o computador remoto

Dentro da sua cópia:

**Code** → **Codespaces** → **Create codespace on main**.

Aguarde até abrir uma tela parecida com o VS Code. Essa tela está no navegador; nada está sendo instalado no Windows da escola.

### 3. Abra o terminal

No menu superior do Codespaces:

**Terminal** → **New Terminal**.

Você deverá ver um terminal na parte inferior da tela.

### 4. Confirme onde você está

Digite, uma linha de cada vez:

```bash
pwd
ls
python --version
```

Você deve enxergar os arquivos deste projeto e uma versão do Python 3.

### 5. Crie um ambiente Python para o projeto

```bash
python -m venv .venv
source .venv/bin/activate
```

Quando funcionar, o terminal normalmente passa a mostrar `(.venv)` no começo da linha.

### 6. Instale as dependências DO PROJETO

```bash
python -m pip install -r requirements.txt
```

Isso instala as bibliotecas **dentro do computador remoto do Codespaces**, não no computador da escola.

### 7. Crie sua configuração local

```bash
cp .env.example .env
```

Depois confira:

```bash
cat .env
```

Neste laboratório o banco está em outro serviço do mesmo Codespace. Por isso `DB_HOST=db` e não `localhost`.

### 8. Confirme que o MySQL remoto está ligado

```bash
mysqladmin -h db -u root -proot ping
```

Resultado esperado:

```text
mysqld is alive
```

### 9. Importe o banco do TPaC

```bash
mysql -h db -u root -proot < database.sql
```

Se o comando voltar para o terminal sem mensagem de erro, prossiga.

### 10. Veja se as tabelas foram criadas

```bash
mysql -h db -u tpac -ptpac -D tpac_db -e "SHOW TABLES;"
```

Você deverá ver:

```text
passos
tarefas
usuarios
```

### 11. Execute o sistema

```bash
python main.py
```

O menu inicial do TPaC deverá aparecer no próprio terminal.

### 12. Faça o teste mínimo

1. Entre com o perfil de exemplo `Matheus`.
2. Visualize a tarefa existente.
3. Crie uma nova tarefa.
4. Marque uma tarefa como concluída.
5. Saia do programa.
6. Execute novamente `python main.py`.
7. Confirme se a alteração continuou salva.

Se continuou salva, o Python está conversando corretamente com o MySQL.

## Verificação rápida do laboratório

Depois de concluir a implantação, saia do programa e execute:

```bash
bash scripts/verificar_ambiente.sh
```

O script verifica Python, dependências, arquivo `.env`, MySQL, banco e estrutura principal do projeto.

## Credenciais do laboratório

Estas credenciais existem **somente para esta atividade didática**:

```text
Servidor do banco: db
Porta: 3306
Banco: tpac_db
Usuário da aplicação: tpac
Senha da aplicação: tpac
Usuário administrador do laboratório: root
Senha do administrador do laboratório: root
```

Em um sistema de produção, senhas não devem ficar publicadas no repositório. Aqui elas são deliberadamente simples porque cada aluno recebe um ambiente isolado e descartável para aprendizagem.

## Ao terminar a aula

Salve o código no GitHub usando **Source Control → Commit → Sync Changes**.

Depois pare o Codespace para não consumir sua franquia enquanto não estiver usando:

**GitHub → Codespaces → ... → Stop codespace**.

---

**Professor:** consulte `GUIA_PROFESSOR.md` antes da aula.  
**Aluno:** siga `AULA_02_ALUNO.md` sem pular etapas.
