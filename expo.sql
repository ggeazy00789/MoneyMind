CREATE database db_moneyMind2;
USE db_moneyMind2;
create table tb_usuario(
	usu_id int auto_increment primary key,
    usu_data_criacao DATE DEFAULT (CURRENT_DATE),
    usu_nome varchar(100) not null,
    usu_email varchar(100) unique not null,
    usu_cpf varchar(14) unique not null,
    usu_senha varchar(100) not null,
    usu_data_de_nascimento date
);

create table tb_categoria(
	cat_id int auto_increment primary key,
    cat_nome varchar(100)not null,
    cat_tipo ENUM('receita', 'despesa') NOT NULL,
     categoria_padrao BOOLEAN DEFAULT TRUE,
     cat_usuario INT null,
    FOREIGN KEY (cat_usuario) REFERENCES tb_usuario(usu_id)
    );

create table tb_receita(
	rec_id int auto_increment primary key,
    rec_data_criacao DATE DEFAULT (CURRENT_DATE),
	rec_descricao text,
	rec_valor_salario decimal (10,2) not null,
	rec_data_salario date not null,
    rec_categoria int,
    rec_usuario int,
    -- chave estrangeira
    foreign key (rec_categoria) references tb_categoria(cat_id),
    foreign key (rec_usuario) references tb_usuario(usu_id)
);

create table tb_despesas(
	des_id int auto_increment primary key,
    des_data_criacao DATE DEFAULT (CURRENT_DATE),
    des_valor decimal(10,2) not null,
    des_descricao text not null,
    des_data date not null,
    des_forma_pagamento enum('Pix','Crédito','Débito','Dinheiro'),
    des_status enum('Pendente','Pago','Atrasado','Cancelado'),
    des_vencimento date, 
    des_data_pagamento date,
    -- chaves estrangeiras
    des_categoria int,
    des_usuario int,
    foreign key ( des_categoria) references tb_categoria (cat_id),
    foreign key ( des_usuario) references tb_usuario (usu_id)
);

create table tb_meta(
	met_id int auto_increment primary key,
    met_descricao TEXT,
    met_nome varchar(150) not null,
    met_status ENUM('Em andamento','Concluída','Atrasada'),
    met_val_obj decimal(10,2) not null,
    met_val_atu decimal(10,2) not null default 0,
    met_prazo varchar(100) not null,
    -- chaves estrangeiras
    met_usu_id int,
    foreign key (met_usu_id) references tb_usuario (usu_id)
);

    
CREATE VIEW vw_resultado AS

SELECT
    usu_id,
    usu_nome,

    -- TOTAL DE RECEITAS
    IFNULL(
        (
            SELECT SUM(rec_valor_salario)
            FROM tb_receita rec_valor_salario
            WHERE rec_usuario = usu_id
        ),
        0
    ) AS total_receitas,

    -- TOTAL DE DESPESAS
    IFNULL(
        (
            SELECT SUM(des_valor)
            FROM tb_despesas des_valor
            WHERE des_usuario = usu_id
        ),
        0
    ) AS total_despesas,

    -- SALDO FINAL
    IFNULL(
        (
            SELECT SUM(rec_valor_salario)
            FROM tb_receita rec_valor_salario
            WHERE rec_usuario = usu_id
        ),
        0
    )

    -

    IFNULL(
        (
            SELECT SUM(des_valor)
            FROM tb_despesas des_valor
            WHERE des_usuario = usu_id
        ),
        0
    ) AS saldo_final

FROM tb_usuario usu_id;
    
INSERT INTO tb_categoria
(cat_nome, cat_tipo)
VALUES
('Alimentação', 'Despesa'),
('Transporte', 'Despesa'),
('Salário', 'Receita');