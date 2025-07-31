# import pymysql
# import sys
# from config import Config

# print("=== SETUP COMPLETO DO BANCO DE DADOS ===\n")

# # PASSO 1: Conectar sem especificar banco
# print("1. Testando conexão com MySQL...")
# try:
#     # Conexão sem banco de dados especificado
#     conn = pymysql.connect(
#         host=Config.DB_HOST,
#         user=Config.DB_USER,
#         password=Config.DB_PASSWORD,
#         port=int(Config.DB_PORT) if isinstance(Config.DB_PORT, str) else Config.DB_PORT
#     )
#     print("   ✅ Conectado ao MySQL!")
    
# except pymysql.err.OperationalError as e:
#     print(f"   ❌ Erro de conexão: {e}")
#     print("\n⚠️  SOLUÇÃO:")
#     print("1. Verifique se o MySQL está rodando")
#     print("2. Se usa XAMPP: Abra o XAMPP Control Panel e inicie o MySQL")
#     print("3. Se usa MySQL Server: Execute 'net start MySQL80' como admin")
#     sys.exit(1)

# # PASSO 2: Criar banco de dados
# print("\n2. Criando banco de dados...")
# try:
#     with conn.cursor() as cursor:
#         cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
#         print(f"   ✅ Banco '{Config.DB_NAME}' criado/verificado!")
#     conn.close()
# except Exception as e:
#     print(f"   ❌ Erro ao criar banco: {e}")
#     sys.exit(1)

# # PASSO 3: Conectar ao banco criado
# print("\n3. Conectando ao banco de dados...")
# try:
#     conn = pymysql.connect(
#         host=Config.DB_HOST,
#         user=Config.DB_USER,
#         password=Config.DB_PASSWORD,
#         database=Config.DB_NAME,
#         port=int(Config.DB_PORT) if isinstance(Config.DB_PORT, str) else Config.DB_PORT,
#         charset='utf8mb4'
#     )
#     print(f"   ✅ Conectado ao banco '{Config.DB_NAME}'!")
# except Exception as e:
#     print(f"   ❌ Erro ao conectar ao banco: {e}")
#     sys.exit(1)

# # PASSO 4: Criar tabelas
# print("\n4. Criando tabelas...")

# with conn.cursor() as cursor:
#     # Tabela de clientes
#     print("   - Criando tabela 'clientes'...")
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS clientes (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             nome VARCHAR(100) NOT NULL,
#             email VARCHAR(100) UNIQUE NOT NULL,
#             senha VARCHAR(255) NOT NULL,
#             telefone VARCHAR(20),
#             endereco TEXT,
#             cidade VARCHAR(100),
#             estado VARCHAR(2),
#             cep VARCHAR(10),
#             is_admin BOOLEAN DEFAULT FALSE,
#             data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             INDEX idx_email (email)
#         ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
#     """)
#     print("     ✅ Tabela 'clientes' criada!")

#     # Tabela de produtos
#     print("   - Criando tabela 'produtos'...")
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS produtos (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             nome VARCHAR(200) NOT NULL,
#             descricao TEXT,
#             preco DECIMAL(10, 2) NOT NULL,
#             estoque INT DEFAULT 0,
#             categoria VARCHAR(100),
#             imagem VARCHAR(255),
#             ativo BOOLEAN DEFAULT TRUE,
#             data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             INDEX idx_categoria (categoria),
#             INDEX idx_ativo (ativo)
#         ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
#     """)
#     print("     ✅ Tabela 'produtos' criada!")

#     # Tabela de pedidos
#     print("   - Criando tabela 'pedidos'...")
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS pedidos (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             cliente_id INT NOT NULL,
#             data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             status VARCHAR(50) DEFAULT 'pendente',
#             total DECIMAL(10, 2) NOT NULL,
#             endereco_entrega TEXT,
#             observacoes TEXT,
#             FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
#             INDEX idx_cliente (cliente_id),
#             INDEX idx_status (status)
#         ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
#     """)
#     print("     ✅ Tabela 'pedidos' criada!")

#     # Tabela de itens do pedido
#     print("   - Criando tabela 'itens_pedido'...")
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS itens_pedido (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             pedido_id INT NOT NULL,
#             produto_id INT NOT NULL,
#             quantidade INT NOT NULL,
#             preco_unitario DECIMAL(10, 2) NOT NULL,
#             FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
#             FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE,
#             INDEX idx_pedido (pedido_id),
#             INDEX idx_produto (produto_id)
#         ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
#     """)
#     print("     ✅ Tabela 'itens_pedido' criada!")

#     conn.commit()

# # PASSO 5: Inserir dados de teste
# print("\n5. Inserindo dados de teste...")
# with conn.cursor() as cursor:
#     # Verifica se já existem produtos
#     cursor.execute("SELECT COUNT(*) as total FROM produtos")
#     if cursor.fetchone()['total'] == 0:
#         print("   - Inserindo produtos de exemplo...")
#         produtos_exemplo = [
#             ('Notebook Dell Inspiron', 'Notebook com processador Intel Core i5', 2999.99, 10, 'Eletrônicos'),
#             ('Mouse Gamer RGB', 'Mouse com 7 botões programáveis e iluminação RGB', 129.90, 50, 'Periféricos'),
#             ('Teclado Mecânico', 'Teclado mecânico com switches blue', 299.90, 30, 'Periféricos'),
#             ('Monitor 24" Full HD', 'Monitor LED com resolução 1920x1080', 899.00, 15, 'Monitores'),
#             ('Webcam HD 1080p', 'Webcam com microfone integrado', 199.90, 25, 'Periféricos')
#         ]
        
#         for produto in produtos_exemplo:
#             cursor.execute("""
#                 INSERT INTO produtos (nome, descricao, preco, estoque, categoria)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, produto)
        
#         conn.commit()
#         print("     ✅ Produtos de exemplo inseridos!")
#     else:
#         print("     ℹ️  Produtos já existem no banco")

# # PASSO 6: Verificar instalação
# print("\n6. Verificando instalação...")
# with conn.cursor() as cursor:
#     cursor.execute("SHOW TABLES")
#     tables = cursor.fetchall()
#     print(f"   Tabelas criadas: {len(tables)}")
#     for table in tables:
#         table_name = list(table.values())[0]
#         cursor.execute(f"SELECT COUNT(*) as total FROM {table_name}")
#         count = cursor.fetchone()['total']
#         print(f"   - {table_name}: {count} registros")

# conn.close()

# print("\n✅ SETUP COMPLETO! Seu banco de dados está pronto para uso.")
# print("\n📝 Informações de conexão:")
# print(f"   Host: {Config.DB_HOST}")
# print(f"   Porta: {Config.DB_PORT}")
# print(f"   Banco: {Config.DB_NAME}")
# print(f"   Usuário: {Config.DB_USER}")







import _mysql_connector
from config import Config

def criar_banco_dados():
    print("=== CONFIGURANDO BANCO DE DADOS (MariaDB) ===\n")
    
    try:
        # Primeiro conecta sem especificar banco
        print("1. Conectando ao MariaDB...")
        conn = _mysql_connector(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT,
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        print("   ✅ Conectado com sucesso!")
        
        # Cria o banco se não existir
        print("\n2. Criando banco de dados...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {Config.DB_NAME}")
        print(f"   ✅ Banco '{Config.DB_NAME}' criado/selecionado!")
        
        # Remove tabelas existentes com problemas
        print("\n3. Removendo tabelas com problemas...")
        tables_to_drop = ['itens_pedido', 'pedidos', 'carrinho', 'produtos', 'clientes']
        for table in tables_to_drop:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"   - Tabela '{table}' removida")
            except:
                pass
        
        # Cria tabela de clientes
        print("\n4. Criando tabela 'clientes'...")
        create_clientes = """
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            senha VARCHAR(255) NOT NULL,
            telefone VARCHAR(20) DEFAULT NULL,
            endereco TEXT DEFAULT NULL,
            cidade VARCHAR(100) DEFAULT NULL,
            estado VARCHAR(2) DEFAULT NULL,
            cep VARCHAR(10) DEFAULT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        cursor.execute(create_clientes)
        print("   ✅ Tabela 'clientes' criada!")
        
        # Cria tabela de produtos
        print("\n5. Criando tabela 'produtos'...")
        create_produtos = """
        CREATE TABLE IF NOT EXISTS produtos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(200) NOT NULL,
            descricao TEXT DEFAULT NULL,
            preco DECIMAL(10, 2) NOT NULL,
            estoque INT DEFAULT 0,
            categoria VARCHAR(100) DEFAULT NULL,
            imagem VARCHAR(255) DEFAULT NULL,
            ativo BOOLEAN DEFAULT TRUE,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        cursor.execute(create_produtos)
        print("   ✅ Tabela 'produtos' criada!")
        
        # Cria tabela de pedidos
        print("\n6. Criando tabela 'pedidos'...")
        create_pedidos = """
        CREATE TABLE IF NOT EXISTS pedidos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT NOT NULL,
            data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50) DEFAULT 'pendente',
            total DECIMAL(10, 2) NOT NULL,
            endereco_entrega TEXT DEFAULT NULL,
            observacoes TEXT DEFAULT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        cursor.execute(create_pedidos)
        print("   ✅ Tabela 'pedidos' criada!")
        
        # Cria tabela de itens do pedido
        print("\n7. Criando tabela 'itens_pedido'...")
        create_itens = """
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pedido_id INT NOT NULL,
            produto_id INT NOT NULL,
            quantidade INT NOT NULL,
            preco_unitario DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
            FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        cursor.execute(create_itens)
        print("   ✅ Tabela 'itens_pedido' criada!")
        
        # Cria tabela de carrinho
        print("\n8. Criando tabela 'carrinho'...")
        create_carrinho = """
        CREATE TABLE IF NOT EXISTS carrinho (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT DEFAULT NULL,
            produto_id INT NOT NULL,
            quantidade INT NOT NULL DEFAULT 1,
            session_id VARCHAR(255) DEFAULT NULL,
            data_adicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
            FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        cursor.execute(create_carrinho)
        print("   ✅ Tabela 'carrinho' criada!")
        
        conn.commit()
        
        # Verifica as tabelas criadas
        print("\n9. Verificando tabelas criadas...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"   Total de tabelas: {len(tables)}")
        for table in tables:
            cursor.execute(f"DESCRIBE {table[0]}")
            columns = cursor.fetchall()
            print(f"\n   📋 Tabela '{table[0]}' ({len(columns)} colunas):")
            for col in columns:
                print(f"      - {col[0]:15} {col[1]:20}")
        
        # Insere dados de exemplo
        print("\n10. Inserindo dados de exemplo...")
        
        # Produtos de exemplo
        produtos_exemplo = [
            ('Notebook Dell', 'Intel Core i5, 8GB RAM', 2999.99, 10, 'Eletrônicos'),
            ('Mouse Gamer', 'RGB com 6 botões', 129.90, 50, 'Periféricos'),
            ('Teclado Mecânico', 'Switches Blue', 299.90, 30, 'Periféricos'),
            ('Monitor 24"', 'Full HD IPS', 899.00, 15, 'Monitores'),
            ('Webcam HD', '1080p com microfone', 199.90, 25, 'Periféricos')
        ]
        
        for produto in produtos_exemplo:
            cursor.execute("""
                INSERT INTO produtos (nome, descricao, preco, estoque, categoria)
                VALUES (%s, %s, %s, %s, %s)
            """, produto)
        print("   ✅ Produtos de exemplo inseridos!")
        
        # Admin padrão (senha: admin123)
        from werkzeug.security import generate_password_hash
        admin_senha = generate_password_hash('admin123')
        cursor.execute("""
            INSERT INTO clientes (nome, email, senha, is_admin)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE nome=nome
        """, ('Administrador', 'admin@loja.com', admin_senha, True))
        print("   ✅ Usuário admin criado (email: admin@loja.com, senha: admin123)")
        
        conn.commit()
        print("\n✅ BANCO DE DADOS CONFIGURADO COM SUCESSO!")
        
    except _mysql_connector as e:
        print(f"\n❌ Erro de conexão: {e}")
        print("\nVerifique:")
        print("1. Se o MariaDB/MySQL está rodando")
        print("2. Se as credenciais no config.py estão corretas")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    criar_banco_dados()