-- ============================================================
-- BANCO DE DADOS DO TPAC - LABORATÓRIO DEVOPS
-- O serviço MySQL do Codespaces já cria o banco vazio tpac_db.
-- Este arquivo cria/recria as tabelas e os dados de exemplo.
-- ATENÇÃO: executar novamente apaga os dados anteriores da aula.
-- ============================================================

USE tpac_db;

DROP TABLE IF EXISTS passos;
DROP TABLE IF EXISTS tarefas;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    estilo_instrucao ENUM('direto', 'detalhado') NOT NULL DEFAULT 'direto',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tarefas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tipo ENUM('tarefas_diarias', 'tarefas_educacionais') NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    concluida BOOLEAN NOT NULL DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_tarefas_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE passos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tarefa_id INT NOT NULL,
    texto TEXT NOT NULL,
    concluido BOOLEAN NOT NULL DEFAULT FALSE,
    ordem INT NOT NULL DEFAULT 1,

    CONSTRAINT fk_passos_tarefa
        FOREIGN KEY (tarefa_id)
        REFERENCES tarefas(id)
        ON DELETE CASCADE
);

-- Dados de exemplo para o primeiro teste da turma
INSERT INTO usuarios (nome, estilo_instrucao)
VALUES ('Matheus', 'direto');

INSERT INTO tarefas (usuario_id, tipo, titulo, concluida)
VALUES (1, 'tarefas_educacionais', 'Revisar atividade do curso', FALSE);

INSERT INTO passos (tarefa_id, texto, concluido, ordem)
VALUES
    (1, 'Ler o enunciado com atenção.', FALSE, 1),
    (1, 'Separar o que precisa ser entregue.', FALSE, 2),
    (1, 'Executar a primeira parte.', FALSE, 3),
    (1, 'Revisar antes de finalizar.', FALSE, 4);
