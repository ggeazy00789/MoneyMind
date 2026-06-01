import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="db_moneyMind3"
)

# ----------

cursor = conexao.cursor()

print('\n===== CADASTRO =====\n')

usuario = input('insira seu nome:')
senha = input('insira seu senha:')
email = input('insira seu email:')
cpf = input('insira seu CPF(sem pontuação):')
data_nascimento = input('insira a data de nascimento:')

sql = """
      insert into tb_usuario (usu_nome, usu_senha, usu_email, usu_cpf, usu_data_de_nascimento)
      VALUES (%s, %s, %s, %s, %s) \
      """
valores = (usuario, senha, email, cpf, data_nascimento)

cursor.execute(sql, valores)
conexao.commit()
usuario_id = cursor.lastrowid

print('Dados inseridos com sucesso!')

print('\n===== META =====\n')

meta_nome = input('insira o nome da sua meta:')
meta_valor_obj = int(input('insira o valor da sua meta:'))
meta_valor_atu = int(input('insira o valor atual:'))
meta_prazo = input('insira o prazo:')

sql4 = """
       INSERT INTO tb_meta (met_nome, met_val_obj, met_val_atu, met_prazo)
       VALUES (%s, %s, %s, %s) \
       """

valores4 = (meta_nome, meta_valor_obj, meta_valor_atu, meta_prazo)
cursor.execute(sql4, valores4)
conexao.commit()

print('Metas cadastradas com sucesso!')

print('\n===== CATEGORIA =====\n')

c = 's'
while c == 's':
    categoria = input('insira o nome da categoria:')
    tipo = input('insira o tipo da categoria:(despesa ou receita)').lower()

    sql1 = """
           insert into tb_categoria (cat_nome, cat_tipo)
           VALUES (%s, %s) \
           """
    valores1 = (categoria, tipo)
    cursor.execute(sql1, valores1)
    conexao.commit()

    print('Categoria atualizada com sucesso!')

    if tipo == 'receita':

        print('\n===== RECEITAS =====\n')

        descricao = input('insira o nome da receita:')
        valor = float(input('insira o valor da receita:'))
        data = input('insira a data desta receita')

        sql2 = """
               INSERT INTO tb_receita
                   (rec_descricao, rec_valor_salario, rec_data_salario, rec_usuario)
               VALUES (%s, %s, %s, %s) \
               """

        valores2 = (descricao, valor, data, usuario_id)

        cursor.execute(sql2, valores2)

        conexao.commit()

        print('Receitas inseridas com sucesso!')

    elif tipo == 'despesa':

        print('\n===== DESPESAS =====\n')

        descricao_des = input('insira o nome da despesa:')
        data_des = input('insira a data da despesa:')
        forma_pag = input('insira a forma de pagamento:(pix, debito, credito, dinheiro)')
        pagamento = int(input('insira o valor do pagamento:'))
        status = input('insira a status da despesa:(pendente, pago, atrasado ou cancelado)')
        vencimento = input('insira a data de vencimento:')
        data_pag = input('insira a data de pagamento:')

        sql3 = """
               INSERT INTO tb_despesas
               (des_descricao, des_data, des_forma_pagamento,
                des_valor, des_status, des_vencimento,
                des_data_pagamento, des_usuario)

               VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
               """

        valores3 = (descricao_des, data_des, forma_pag, pagamento, status, vencimento, data_pag, usuario_id)

        cursor.execute(sql3, valores3)

        conexao.commit()
        print('Despesa atualizada com sucesso!')

    else:
        print("Tipo inválido!")
        exit()

    c = input('Deseja adicionar um novo valor?<s> ou <n>')

sql5 = "SELECT * FROM vw_resultado"

cursor.execute(sql5)

resultado = cursor.fetchall()

print('\n===== RESULTADO FINANCEIRO =====\n')

for linha in resultado:
    print(f'Usuário: {linha[1]}')
    print(f'Total Receitas: R$ {linha[2]}')
    print(f'Total Despesas: R$ {linha[3]}')
    print(f'Saldo Final: R$ {linha[4]}')
    print('---------------------------')

cursor.close()
conexao.close()
