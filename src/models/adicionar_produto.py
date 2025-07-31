
import _mysql_connector
from config import Config
from datetime import datetime

def adicionar_produtos():
    """Adiciona produtos variados à loja"""
    
    # Lista de produtos para adicionar
    produtos = [
        # Eletrônicos
        {
            'nome': 'Notebook Dell Inspiron 15',
            'descricao': 'Notebook Dell Inspiron 15 3000, Intel Core i5 11ª Geração, 8GB RAM, 256GB SSD, Tela 15.6" Full HD, Windows 11',
            'preco': 3499.99,
            'estoque': 15,
            'categoria': 'Eletrônicos',
            'imagem': 'notebook-dell.jpg'
        },
        {
            'nome': 'Smartphone Samsung Galaxy A54',
            'descricao': 'Samsung Galaxy A54 5G, 128GB, 8GB RAM, Câmera Tripla 50MP, Bateria 5000mAh, Tela 6.4" Super AMOLED',
            'preco': 2299.90,
            'estoque': 25,
            'categoria': 'Eletrônicos',
            'imagem': 'samsung-a54.jpg'
        },
        {
            'nome': 'Smart TV LG 50" 4K',
            'descricao': 'Smart TV LG 50 Polegadas 4K UHD, WiFi, Bluetooth, HDR, ThinQ AI, 3 HDMI, 2 USB',
            'preco': 2799.00,
            'estoque': 10,
            'categoria': 'Eletrônicos',
            'imagem': 'tv-lg-50.jpg'
        },
        {
            'nome': 'Fone de Ouvido JBL Tune 510BT',
            'descricao': 'Fone de Ouvido Sem Fio JBL Tune 510BT, Bluetooth 5.0, 40 horas de bateria, Dobrável',
            'preco': 249.90,
            'estoque': 50,
            'categoria': 'Eletrônicos',
            'imagem': 'jbl-tune.jpg'
        },
        {
            'nome': 'Tablet iPad 9ª Geração',
            'descricao': 'Apple iPad 9ª Geração, Tela 10.2", 64GB, Wi-Fi, Chip A13 Bionic, Câmera 8MP',
            'preco': 3599.00,
            'estoque': 12,
            'categoria': 'Eletrônicos',
            'imagem': 'ipad-9.jpg'
        },
        
        # Informática
        {
            'nome': 'Mouse Gamer Logitech G403',
            'descricao': 'Mouse Gamer Logitech G403 HERO, RGB, 25600 DPI, 6 Botões Programáveis',
            'preco': 299.90,
            'estoque': 30,
            'categoria': 'Informática',
            'imagem': 'mouse-g403.jpg'
        },
        {
            'nome': 'Teclado Mecânico Redragon Kumara',
            'descricao': 'Teclado Mecânico Gamer Redragon Kumara K552, RGB, Switch Blue, ABNT2',
            'preco': 229.90,
            'estoque': 20,
            'categoria': 'Informática',
            'imagem': 'teclado-redragon.jpg'
        },
        {
            'nome': 'SSD Kingston NV2 500GB',
            'descricao': 'SSD NVMe Kingston NV2 500GB, M.2 2280, Leitura 3500MB/s, Gravação 2100MB/s',
            'preco': 259.90,
            'estoque': 40,
            'categoria': 'Informática',
            'imagem': 'ssd-kingston.jpg'
        },
        {
            'nome': 'Webcam Logitech C920',
            'descricao': 'Webcam Logitech C920 Full HD 1080p, 30fps, Microfone Integrado, Foco Automático',
            'preco': 449.90,
            'estoque': 15,
            'categoria': 'Informática',
            'imagem': 'webcam-c920.jpg'
        },
        {
            'nome': 'Monitor Gamer AOC 24" 144Hz',
            'descricao': 'Monitor Gamer AOC Hero 24" LED, 144Hz, 1ms, Full HD, IPS, HDMI/DisplayPort',
            'preco': 1299.90,
            'estoque': 8,
            'categoria': 'Informática',
            'imagem': 'monitor-aoc.jpg'
        },
        
        # Casa e Decoração
        {
            'nome': 'Ventilador de Torre Mondial',
            'descricao': 'Ventilador de Torre Mondial Maxi Power, 3 Velocidades, Timer, Controle Remoto',
            'preco': 299.90,
            'estoque': 20,
            'categoria': 'Casa e Decoração',
            'imagem': 'ventilador-torre.jpg'
        },
        {
            'nome': 'Luminária LED de Mesa',
            'descricao': 'Luminária LED de Mesa Articulada, Touch, 3 Níveis de Intensidade, USB Recarregável',
            'preco': 89.90,
            'estoque': 35,
            'categoria': 'Casa e Decoração',
            'imagem': 'luminaria-led.jpg'
        },
        {
            'nome': 'Umidificador de Ar Ultrassônico',
            'descricao': 'Umidificador de Ar Ultrassônico 2L, LED Colorido, Aromatizador, Silencioso',
            'preco': 129.90,
            'estoque': 25,
            'categoria': 'Casa e Decoração',
            'imagem': 'umidificador.jpg'
        },
        
        # Esportes
        {
            'nome': 'Tênis Nike Revolution 6',
            'descricao': 'Tênis Nike Revolution 6 Masculino, Corrida e Academia, Solado em Borracha',
            'preco': 349.90,
            'estoque': 30,
            'categoria': 'Esportes',
            'imagem': 'tenis-nike.jpg'
        },
        {
            'nome': 'Bola de Futebol Penalty',
            'descricao': 'Bola de Futebol Penalty S11 R1, Campo, Costurada à Mão, Aprovada FIFA',
            'preco': 149.90,
            'estoque': 20,
            'categoria': 'Esportes',
            'imagem': 'bola-penalty.jpg'
        },
        {
            'nome': 'Kit Halteres 20kg',
            'descricao': 'Kit Halteres Ajustáveis com Anilhas, Total 20kg, Barras com Pegada Emborrachada',
            'preco': 189.90,
            'estoque': 15,
            'categoria': 'Esportes',
            'imagem': 'halteres.jpg'
        },
        
        # Livros
        {
            'nome': 'Python para Análise de Dados',
            'descricao': 'Livro Python para Análise de Dados - Wes McKinney, 3ª Edição, 540 páginas',
            'preco': 89.90,
            'estoque': 25,
            'categoria': 'Livros',
            'imagem': 'livro-python.jpg'
        },
        {
            'nome': 'O Programador Pragmático',
            'descricao': 'O Programador Pragmático: De Aprendiz a Mestre - Andrew Hunt e David Thomas',
            'preco': 79.90,
            'estoque': 20,
            'categoria': 'Livros',
            'imagem': 'programador-pragmatico.jpg'
        },
        {
            'nome': 'Clean Code',
            'descricao': 'Clean Code: Habilidades Práticas do Agile Software - Robert C. Martin',
            'preco': 84.90,
            'estoque': 18,
            'categoria': 'Livros',
            'imagem': 'clean-code.jpg'
        },
        
        # Games
        {
            'nome': 'PlayStation 5',
            'descricao': 'Console PlayStation 5 825GB, Controle DualSense, Ray Tracing, 4K 120fps',
            'preco': 4499.90,
            'estoque': 5,
            'categoria': 'Games',
            'imagem': 'ps5.jpg'
        },
        {
            'nome': 'Controle Xbox Series Wireless',
            'descricao': 'Controle Microsoft Xbox Series Wireless, Bluetooth, Compatível PC e Xbox',
            'preco': 499.90,
            'estoque': 15,
            'categoria': 'Games',
            'imagem': 'controle-xbox.jpg'
        },
        {
            'nome': 'Headset Gamer HyperX Cloud',
            'descricao': 'Headset Gamer HyperX Cloud Stinger, Drivers 50mm, P2, PS4/Xbox/PC',
            'preco': 299.90,
            'estoque': 20,
            'categoria': 'Games',
            'imagem': 'headset-hyperx.jpg'
        }
    ]
    
    try:
        # Conecta ao banco
        conn = _mysql_connector(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT,
            cursorclass=_mysql_connector.DictCursor
        )
        
        with conn.cursor() as cursor:
            # Primeiro, limpa produtos existentes (opcional)
            resposta = input("\\nDeseja limpar produtos existentes antes de adicionar? (s/N): ")
            if resposta.lower() == 's':
                cursor.execute("DELETE FROM produtos")
                print("✅ Produtos existentes removidos!")
            
            # Adiciona cada produto
            sql = """
                INSERT INTO produtos 
                (nome, descricao, preco, estoque, categoria, imagem, ativo, data_cadastro)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            produtos_adicionados = 0
            for produto in produtos:
                try:
                    valores = (
                        produto['nome'],
                        produto['descricao'],
                        produto['preco'],
                        produto['estoque'],
                        produto['categoria'],
                        produto['imagem'],
                        True,  # ativo
                        datetime.now()
                    )
                    cursor.execute(sql, valores)
                    produtos_adicionados += 1
                    print(f"✅ {produto['nome']} - Adicionado!")
                except _mysql_connector. IntegrityError:
                    print(f"⚠️  {produto['nome']} - Já existe!")
                except Exception as e:
                    print(f"❌ {produto['nome']} - Erro: {e}")
            
            conn.commit()
            
            # Mostra resumo
            print(f"\\n🎉 {produtos_adicionados} produtos adicionados com sucesso!")
            
            # Mostra estatísticas
            cursor.execute("SELECT categoria, COUNT(*) as total FROM produtos GROUP BY categoria")
            categorias = cursor.fetchall()
            
            print("\\n📊 Produtos por categoria:")
            for cat in categorias:
                print(f"   - {cat['categoria']}: {cat['total']} produtos")
            
            cursor.execute("SELECT COUNT(*) as total FROM produtos")
            total = cursor.fetchone()['total']
            print(f"\\n📦 Total de produtos na loja: {total}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("="*60)
    print("🛍️  ADICIONAR PRODUTOS À LOJA")
    print("="*60)
    print("\\nEste script irá adicionar 22 produtos de exemplo em várias categorias.")
    print("\\nCategorias incluídas:")
    print("- Eletrônicos")
    print("- Informática") 
    print("- Casa e Decoração")
    print("- Esportes")
    print("- Livros")
    print("- Games")
    
    confirma = input("\\nDeseja continuar? (S/n): ")
    if confirma.lower() != 'n':
        adicionar_produtos()
    else:
        print("Operação cancelada.")


with open('adicionar_produtos.py', 'w', encoding='utf-8') as f:
    


    print("✅ Script 'adicionar_produtos.py' criado com sucesso!")
    print("\n📦 Este script adiciona 22 produtos em 6 categorias diferentes!")
    print("\nPara executar:")
    print("python adicionar_produtos.py")


# # Criando script para adicionar produtos
# import pymysql
# from config import Config
# from datetime import datetime

# def adicionar_produtos():
#     """Adiciona produtos variados à loja"""
    
#     # Lista de produtos para adicionar
#     produtos = [
#         # Eletrônicos
#         {
#             'nome': 'Notebook Dell Inspiron 15',
#             'descricao': 'Notebook Dell Inspiron 15 3000, Intel Core i5 11ª Geração, 8GB RAM, 256GB SSD, Tela 15.6" Full HD, Windows 11',
#             'preco': 3499.99,
#             'estoque': 15,
#             'categoria': 'Eletrônicos',
#             'imagem': 'notebook-dell.jpg'
#         },
#         {
#             'nome': 'Smartphone Samsung Galaxy A54',
#             'descricao': 'Samsung Galaxy A54 5G, 128GB, 8GB RAM, Câmera Tripla 50MP, Bateria 5000mAh, Tela 6.4" Super AMOLED',
#             'preco': 2299.90,
#             'estoque': 25,
#             'categoria': 'Eletrônicos',
#             'imagem': 'samsung-a54.jpg'
#         },
#         {
#             'nome': 'Smart TV LG 50" 4K',
#             'descricao': 'Smart TV LG 50 Polegadas 4K UHD, WiFi, Bluetooth, HDR, ThinQ AI, 3 HDMI, 2 USB',
#             'preco': 2799.00,
#             'estoque': 10,
#             'categoria': 'Eletrônicos',
#             'imagem': 'tv-lg-50.jpg'
#         },
#         {
#             'nome': 'Fone de Ouvido JBL Tune 510BT',
#             'descricao': 'Fone de Ouvido Sem Fio JBL Tune 510BT, Bluetooth 5.0, 40 horas de bateria, Dobrável',
#             'preco': 249.90,
#             'estoque': 50,
#             'categoria': 'Eletrônicos',
#             'imagem': 'jbl-tune.jpg'
#         },
#         {
#             'nome': 'Tablet iPad 9ª Geração',
#             'descricao': 'Apple iPad 9ª Geração, Tela 10.2", 64GB, Wi-Fi, Chip A13 Bionic, Câmera 8MP',
#             'preco': 3599.00,
#             'estoque': 12,
#             'categoria': 'Eletrônicos',
#             'imagem': 'ipad-9.jpg'
#         },
        
#         # Informática
#         {
#             'nome': 'Mouse Gamer Logitech G403',
#             'descricao': 'Mouse Gamer Logitech G403 HERO, RGB, 25600 DPI, 6 Botões Programáveis',
#             'preco': 299.90,
#             'estoque': 30,
#             'categoria': 'Informática',
#             'imagem': 'mouse-g403.jpg'
#         },
#         {
#             'nome': 'Teclado Mecânico Redragon Kumara',
#             'descricao': 'Teclado Mecânico Gamer Redragon Kumara K552, RGB, Switch Blue, ABNT2',
#             'preco': 229.90,
#             'estoque': 20,
#             'categoria': 'Informática',
#             'imagem': 'teclado-redragon.jpg'
#         },
#         {
#             'nome': 'SSD Kingston NV2 500GB',
#             'descricao': 'SSD NVMe Kingston NV2 500GB, M.2 2280, Leitura 3500MB/s, Gravação 2100MB/s',
#             'preco': 259.90,
#             'estoque': 40,
#             'categoria': 'Informática',
#             'imagem': 'ssd-kingston.jpg'
#         },
#         {
#             'nome': 'Webcam Logitech C920',
#             'descricao': 'Webcam Logitech C920 Full HD 1080p, 30fps, Microfone Integrado, Foco Automático',
#             'preco': 449.90,
#             'estoque': 15,
#             'categoria': 'Informática',
#             'imagem': 'webcam-c920.jpg'
#         },
#         {
#             'nome': 'Monitor Gamer AOC 24" 144Hz',
#             'descricao': 'Monitor Gamer AOC Hero 24" LED, 144Hz, 1ms, Full HD, IPS, HDMI/DisplayPort',
#             'preco': 1299.90,
#             'estoque': 8,
#             'categoria': 'Informática',
#             'imagem': 'monitor-aoc.jpg'
#         },
        
#         # Casa e Decoração
#         {
#             'nome': 'Ventilador de Torre Mondial',
#             'descricao': 'Ventilador de Torre Mondial Maxi Power, 3 Velocidades, Timer, Controle Remoto',
#             'preco': 299.90,
#             'estoque': 20,
#             'categoria': 'Casa e Decoração',
#             'imagem': 'ventilador-torre.jpg'
#         },
#         {
#             'nome': 'Luminária LED de Mesa',
#             'descricao': 'Luminária LED de Mesa Articulada, Touch, 3 Níveis de Intensidade, USB Recarregável',
#             'preco': 89.90,
#             'estoque': 35,
#             'categoria': 'Casa e Decoração',
#             'imagem': 'luminaria-led.jpg'
#         },
#         {
#             'nome': 'Umidificador de Ar Ultrassônico',
#             'descricao': 'Umidificador de Ar Ultrassônico 2L, LED Colorido, Aromatizador, Silencioso',
#             'preco': 129.90,
#             'estoque': 25,
#             'categoria': 'Casa e Decoração',
#             'imagem': 'umidificador.jpg'
#         },
        
#         # Esportes
#         {
#             'nome': 'Tênis Nike Revolution 6',
#             'descricao': 'Tênis Nike Revolution 6 Masculino, Corrida e Academia, Solado em Borracha',
#             'preco': 349.90,
#             'estoque': 30,
#             'categoria': 'Esportes',
#             'imagem': 'tenis-nike.jpg'
#         },
#         {
#             'nome': 'Bola de Futebol Penalty',
#             'descricao': 'Bola de Futebol Penalty S11 R1, Campo, Costurada à Mão, Aprovada FIFA',
#             'preco': 149.90,
#             'estoque': 20,
#             'categoria': 'Esportes',
#             'imagem': 'bola-penalty.jpg'
#         },
#         {
#             'nome': 'Kit Halteres 20kg',
#             'descricao': 'Kit Halteres Ajustáveis com Anilhas, Total 20kg, Barras com Pegada Emborrachada',
#             'preco': 189.90,
#             'estoque': 15,
#             'categoria': 'Esportes',
#             'imagem': 'halteres.jpg'
#         },
        
#         # Livros
#         {
#             'nome': 'Python para Análise de Dados',
#             'descricao': 'Livro Python para Análise de Dados - Wes McKinney, 3ª Edição, 540 páginas',
#             'preco': 89.90,
#             'estoque': 25,
#             'categoria': 'Livros',
#             'imagem': 'livro-python.jpg'
#         },
#         {
#             'nome': 'O Programador Pragmático',
#             'descricao': 'O Programador Pragmático: De Aprendiz a Mestre - Andrew Hunt e David Thomas',
#             'preco': 79.90,
#             'estoque': 20,
#             'categoria': 'Livros',
#             'imagem': 'programador-pragmatico.jpg'
#         },
#         {
#             'nome': 'Clean Code',
#             'descricao': 'Clean Code: Habilidades Práticas do Agile Software - Robert C. Martin',
#             'preco': 84.90,
#             'estoque': 18,
#             'categoria': 'Livros',
#             'imagem': 'clean-code.jpg'
#         },
        
#         # Games
#         {
#             'nome': 'PlayStation 5',
#             'descricao': 'Console PlayStation 5 825GB, Controle DualSense, Ray Tracing, 4K 120fps',
#             'preco': 4499.90,
#             'estoque': 5,
#             'categoria': 'Games',
#             'imagem': 'ps5.jpg'
#         },
#         {
#             'nome': 'Controle Xbox Series Wireless',
#             'descricao': 'Controle Microsoft Xbox Series Wireless, Bluetooth, Compatível PC e Xbox',
#             'preco': 499.90,
#             'estoque': 15,
#             'categoria': 'Games',
#             'imagem': 'controle-xbox.jpg'
#         },
#         {
#             'nome': 'Headset Gamer HyperX Cloud',
#             'descricao': 'Headset Gamer HyperX Cloud Stinger, Drivers 50mm, P2, PS4/Xbox/PC',
#             'preco': 299.90,
#             'estoque': 20,
#             'categoria': 'Games',
#             'imagem': 'headset-hyperx.jpg'
#         }
#     ]
    
#     try:
#         # Conecta ao banco
#         conn = pymysql.connect(
#             host=Config.DB_HOST,
#             user=Config.DB_USER,
#             password=Config.DB_PASSWORD,
#             database=Config.DB_NAME,
#             port=Config.DB_PORT,
#             cursorclass=pymysql.cursors.DictCursor
#         )
        
#         with conn.cursor() as cursor:
#             # Primeiro, limpa produtos existentes (opcional)
#             resposta = input("\\nDeseja limpar produtos existentes antes de adicionar? (s/N): ")
#             if resposta.lower() == 's':
#                 cursor.execute("DELETE FROM produtos")
#                 print("✅ Produtos existentes removidos!")
            
#             # Adiciona cada produto
#             sql = """
#                 INSERT INTO produtos 
#                 (nome, descricao, preco, estoque, categoria, imagem, ativo, data_cadastro)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             """
            
#             produtos_adicionados = 0
#             for produto in produtos:
#                 try:
#                     valores = (
#                         produto['nome'],
#                         produto['descricao'],
#                         produto['preco'],
#                         produto['estoque'],
#                         produto['categoria'],
#                         produto['imagem'],
#                         True,  # ativo
#                         datetime.now()
#                     )
#                     cursor.execute(sql, valores)
#                     produtos_adicionados += 1
#                     print(f"✅ {produto['nome']} - Adicionado!")
#                 except pymysql.err.IntegrityError:
#                     print(f"⚠️  {produto['nome']} - Já existe!")
#                 except Exception as e:
#                     print(f"❌ {produto['nome']} - Erro: {e}")
            
#             conn.commit()
            
#             # Mostra resumo
#             print(f"\\n🎉 {produtos_adicionados} produtos adicionados com sucesso!")
            
#             # Mostra estatísticas
#             cursor.execute("SELECT categoria, COUNT(*) as total FROM produtos GROUP BY categoria")
#             categorias = cursor.fetchall()
            
#             print("\\n📊 Produtos por categoria:")
#             for cat in categorias:
#                 print(f"   - {cat['categoria']}: {cat['total']} produtos")
            
#             cursor.execute("SELECT COUNT(*) as total FROM produtos")
#             total = cursor.fetchone()['total']
#             print(f"\\n📦 Total de produtos na loja: {total}")
            
#     except Exception as e:
#         print(f"❌ Erro: {e}")
#     finally:
#         if conn:
#             conn.close()

# if __name__ == "__main__":
#     print("="*60)
#     print("🛍️  ADICIONAR PRODUTOS À LOJA")
#     print("="*60)
#     print("\\nEste script irá adicionar 22 produtos de exemplo em várias categorias.")
#     print("\\nCategorias incluídas:")
#     print("- Eletrônicos")
#     print("- Informática") 
#     print("- Casa e Decoração")
#     print("- Esportes")
#     print("- Livros")
#     print("- Games")
    
#     confirma = input("\\nDeseja continuar? (S/n): ")
#     if confirma.lower() != 'n':
#         adicionar_produtos()
#     else:
#         print("Operação cancelada.")

# with open('adicionar_produtos.py', 'w', encoding='utf-8') as f:
#     f.write()

# print("✅ Script 'adicionar_produtos.py' criado com sucesso!")
# print("\n📦 Este script adiciona 22 produtos em 6 categorias diferentes!")
# print("\nPara executar:")
# print("python adicionar_produtos.py")