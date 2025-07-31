import _mysql_connector
from config import Config

def verificar_produtos():
    """Verifica se os produtos estão no banco de dados"""

    try:
        # Conecta ao banco
        conn = _mysql_connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT,
            cursorclass=_mysql_connector
        )

        print("✅ Conectado ao banco de dados\n")

        with conn.cursor() as cursor:
            # 1. Verifica se a tabela produtos existe
            cursor.execute("SHOW TABLES LIKE 'produtos'")
            if not cursor.fetchone():
                print("❌ ERRO: Tabela 'produtos' NÃO existe!")
                print("\nCriando tabela produtos...")

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS produtos (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nome VARCHAR(200) NOT NULL,
                        descricao TEXT,
                        preco DECIMAL(10, 2) NOT NULL,
                        estoque INT DEFAULT 0,
                        categoria VARCHAR(100),
                        imagem VARCHAR(255),
                        ativo BOOLEAN DEFAULT TRUE,
                        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_categoria (categoria),
                        INDEX idx_ativo (ativo)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                conn.commit()
                print("✅ Tabela 'produtos' criada!")
                return

            # 2. Verifica estrutura da tabela
            print("📋 Estrutura da tabela produtos:")
            cursor.execute("DESCRIBE produtos")
            for col in cursor.fetchall():
                print(f"   - {col['Field']}: {col['Type']}")

            # 3. Conta produtos
            cursor.execute("SELECT COUNT(*) as total FROM produtos")
            total = cursor.fetchone()['total']
            print(f"\n📦 Total de produtos no banco: {total}")

            if total == 0:
                print("\n⚠️  Nenhum produto encontrado!")
                print("\nExecute: python adicionar_produtos.py")
            else:
                # 4. Lista produtos
                print("\n🛍️  Produtos cadastrados:")
                cursor.execute("SELECT id, nome, preco, estoque, categoria, ativo FROM produtos LIMIT 10")
                produtos = cursor.fetchall()

                for p in produtos:
                    status = "✅ Ativo" if p['ativo'] else "❌ Inativo"
                    print(f"   [{p['id']}] {p['nome']} - R$ {p['preco']} - Estoque: {p['estoque']} - {p['categoria']} - {status}")

                if total > 10:
                    print(f"   ... e mais {total - 10} produtos")

                # 5. Verifica produtos ativos
                cursor.execute("SELECT COUNT(*) as total FROM produtos WHERE ativo = TRUE")
                ativos = cursor.fetchone()['total']
                print(f"\n✅ Produtos ativos: {ativos}")

                # 6. Produtos por categoria
                print("\n📊 Produtos por categoria:")
                cursor.execute("SELECT categoria, COUNT(*) as total FROM produtos GROUP BY categoria")
                for cat in cursor.fetchall():
                    print(f"   - {cat['categoria']}: {cat['total']}")

        conn.close()

    except Exception as e:
        print(f"❌ Erro: {e}")

    print("\n" + "="*50)
    print("💡 PRÓXIMOS PASSOS:")
    print("="*50)
    print("1. Se não há produtos, execute: python adicionar_produtos.py")
    print("2. Certifique-se de que o Flask está rodando: python app.py")
    print("3. Acesse: http://localhost:5000/produtos")
    print("4. Verifique o console do Flask para erros")

if __name__ == "__main__":
    print("="*50)
    print("🔍 VERIFICAÇÃO DE PRODUTOS NO BANCO")
    print("="*50)
    print()
    verificar_produtos()
