import sqlite3

# Conecta (ou cria) o banco
conn = sqlite3.connect("meu_banco.db")

# Cria cursor
cursor = conn.cursor()

# Cria tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidatos (
    id SERIAL UNIQUE NOT NULL,
    nome VARCHAR(255) UNIQUE NOT NULL,
    cpf CHAR(11) UNIQUE NOT NULL,
    numero_candidato INTEGER UNIQUE NOT NULL
)
""")

# Insere dados
cursor.execute(
    "INSERT INTO candidatos (id, nome, cpf, numero_candidato) VALUES (?, ?, ?, ?)",
    (1,"Diogo", '10470621788', 10)
)

# Confirma alterações
conn.commit()

# Fecha conexão
conn.close()