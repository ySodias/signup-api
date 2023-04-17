BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 76930ac03bbc

CREATE TABLE tb_dominio (
    id SERIAL NOT NULL, 
    nome_dominio VARCHAR NOT NULL, 
    tipo_dominio VARCHAR, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by VARCHAR, 
    updated_by VARCHAR, 
    PRIMARY KEY (id), 
    UNIQUE (nome_dominio)
);

CREATE TABLE tb_usuario (
    id SERIAL NOT NULL, 
    cpf VARCHAR NOT NULL, 
    nome_cliente VARCHAR NOT NULL, 
    data_nascimento VARCHAR, 
    endereco VARCHAR, 
    forma_pagamento INTEGER, 
    telefone VARCHAR, 
    ativo BOOLEAN, 
    plano INTEGER, 
    tipo_usuario INTEGER, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by VARCHAR, 
    updated_by VARCHAR, 
    PRIMARY KEY (id), 
    FOREIGN KEY(forma_pagamento) REFERENCES tb_dominio (id), 
    FOREIGN KEY(plano) REFERENCES tb_dominio (id), 
    FOREIGN KEY(tipo_usuario) REFERENCES tb_dominio (id), 
    UNIQUE (nome_cliente), 
    UNIQUE (cpf)
);

INSERT INTO alembic_version (version_num) VALUES ('76930ac03bbc') RETURNING alembic_version.version_num;

-- Running upgrade 76930ac03bbc -> 3982e1f1e746

CREATE TABLE tb_pagamento (
    id SERIAL NOT NULL, 
    cpf_usuario VARCHAR NOT NULL, 
    data_vencimento VARCHAR, 
    forma_pagamento INTEGER NOT NULL, 
    valor_pagamento BIGINT, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by VARCHAR, 
    updated_by VARCHAR, 
    PRIMARY KEY (id), 
    FOREIGN KEY(forma_pagamento) REFERENCES tb_dominio (id), 
    FOREIGN KEY(cpf_usuario) REFERENCES tb_usuario (cpf)
);

CREATE TABLE tb_politicas_pagamentos (
    id SERIAL NOT NULL, 
    taxa_juros BIGINT NOT NULL, 
    dias_vencidos VARCHAR, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by VARCHAR, 
    updated_by VARCHAR, 
    PRIMARY KEY (id)
);

CREATE TABLE tb_treino (
    id SERIAL NOT NULL, 
    cpf_usuario VARCHAR NOT NULL, 
    nome_exercicio VARCHAR, 
    series INTEGER NOT NULL, 
    repeticoes INTEGER, 
    data_fim TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    modalidade INTEGER, 
    frequencia INTEGER NOT NULL, 
    carga INTEGER, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by VARCHAR, 
    updated_by VARCHAR, 
    PRIMARY KEY (id), 
    FOREIGN KEY(modalidade) REFERENCES tb_dominio (id), 
    FOREIGN KEY(cpf_usuario) REFERENCES tb_usuario (cpf)
);

UPDATE alembic_version SET version_num='3982e1f1e746' WHERE alembic_version.version_num = '76930ac03bbc';

-- Running upgrade 3982e1f1e746 -> 01644e998b19

CREATE TABLE tb_administrador (
    id SERIAL NOT NULL, 
    nome VARCHAR NOT NULL, 
    data_nascimento VARCHAR NOT NULL, 
    endereco VARCHAR NOT NULL, 
    telefone VARCHAR NOT NULL, 
    ativo BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by VARCHAR, 
    updated_by VARCHAR, 
    PRIMARY KEY (id)
);

ALTER TABLE tb_usuario ALTER COLUMN cpf DROP NOT NULL;

UPDATE alembic_version SET version_num='01644e998b19' WHERE alembic_version.version_num = '3982e1f1e746';

-- Running upgrade 01644e998b19 -> e599d04496de

ALTER TABLE tb_administrador ADD COLUMN password VARCHAR;

UPDATE alembic_version SET version_num='e599d04496de' WHERE alembic_version.version_num = '01644e998b19';

-- Running upgrade e599d04496de -> 77a208ca6759

ALTER TABLE tb_administrador ADD COLUMN email VARCHAR;

ALTER TABLE tb_administrador ADD UNIQUE (email);

UPDATE alembic_version SET version_num='77a208ca6759' WHERE alembic_version.version_num = 'e599d04496de';

-- Running upgrade 77a208ca6759 -> 09171ae068e7

ALTER TABLE tb_dominio ALTER COLUMN tipo_dominio SET NOT NULL;

ALTER TABLE tb_usuario ALTER COLUMN cpf SET NOT NULL;

ALTER TABLE tb_usuario ALTER COLUMN data_nascimento SET NOT NULL;

ALTER TABLE tb_usuario ALTER COLUMN endereco SET NOT NULL;

ALTER TABLE tb_usuario ALTER COLUMN forma_pagamento SET NOT NULL;

ALTER TABLE tb_usuario ALTER COLUMN telefone SET NOT NULL;

ALTER TABLE tb_usuario ALTER COLUMN ativo SET NOT NULL;

ALTER TABLE tb_usuario ALTER COLUMN plano SET NOT NULL;

ALTER TABLE tb_usuario DROP CONSTRAINT tb_usuario_tipo_usuario_fkey;

ALTER TABLE tb_usuario DROP COLUMN tipo_usuario;

UPDATE alembic_version SET version_num='09171ae068e7' WHERE alembic_version.version_num = '77a208ca6759';

-- Running upgrade 09171ae068e7 -> fb05451280f9

ALTER TABLE tb_administrador ADD COLUMN nivel_permissao INTEGER;

UPDATE alembic_version SET version_num='fb05451280f9' WHERE alembic_version.version_num = '09171ae068e7';

-- Running upgrade fb05451280f9 -> ec24b1ea1b87

ALTER TABLE tb_pagamento DROP COLUMN valor_pagamento;

UPDATE alembic_version SET version_num='ec24b1ea1b87' WHERE alembic_version.version_num = 'fb05451280f9';

COMMIT;

CREATE OR REPLACE VIEW public.vw_pagamento
AS SELECT tu.id,
    tu.nome_cliente AS nome,
    tu.ativo AS estado_matricula,
    tu.created_at AS cadastrado_em,
        CASE
            WHEN tp.data_vencimento::timestamp without time zone < CURRENT_TIMESTAMP::date AND tu.ativo IS TRUE THEN 'PENDENTE'::text
            WHEN tu.ativo IS FALSE THEN 'INATIVO'::text
            ELSE 'ATIVA'::text
        END AS status_matricula,
    tp.updated_at AS ultima_mensalidade_paga,
    tp.data_vencimento AS vencimento_mensalidade,
    td.nome_dominio AS valor
   FROM tb_pagamento tp
     JOIN tb_usuario tu ON tp.cpf_usuario::text = tu.cpf::text
     JOIN tb_dominio td ON tu.plano = td.id
  ORDER BY tp.data_vencimento DESC;

 CREATE OR REPLACE VIEW public.vw_treino
AS SELECT tt.id,
    tt.nome_exercicio,
    tt.repeticoes,
    tt.carga,
    tt.frequencia,
    tu.nome_cliente,
    to_char(tt.created_at::date::timestamp with time zone, 'yyyy-mm-dd'::text) AS data_inicio,
    to_char(tt.data_fim::date::timestamp with time zone, 'yyyy-mm-dd'::text) AS data_troca,
    tt.series
   FROM tb_treino tt
     JOIN tb_usuario tu ON tt.cpf_usuario::text = tu.cpf::text;