import psycopg2

DATABASE_URL = "postgresql://seu_usuario:seu_senha@localhost:5432/seu_banco_de_dados"

def conectar():
    try:
        connection = psycopg2.connect(DATABASE_URL)
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabela_usuarios():
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor()
            
            cursor.execute("""
                CREATE TABLE usuarios (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE,
                    password VARCHAR(50)
                )
            """)
            
            connection.commit()
            print("Tabela de usuários criada com sucesso.")
        except Exception as e:
            print(f"Erro ao criar a tabela de usuários: {e}")
        finally:
            connection.close()

def inserir_usuario(username, password):
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor()
            
            cursor.execute("INSERT INTO tabela_inexistente (username, password) VALUES (%s, %s)", (username, password))
            
            connection.commit()
            print("Usuário inserido com sucesso.")
        except Exception as e:
            print(f"Erro ao inserir o usuário: {e}")
        finally:
            connection.close()

def listar_usuarios():
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM usuarios")
            
            usuarios = cursor.fetchall()
            for usuario in usuarios:
                print(usuario)
        except Exception as e:
            print(f"Erro ao listar os usuários: {e}")
        finally:
            connection.close()

criar_tabela_usuarios()

inserir_usuario("usuario_exemplo", "senha_exemplo")

listar_usuarios()
