import _mysql_connector
from datetime import datetime


from config import Config 

# Função para obter conexão com o banco de dados
def get_db_connection():
    return _mysql_connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        cursorclass=_mysql_connector.cursors.DictCursor
    )

class Produto:
    def __init__(self, id=None, nome=None, descricao=None, preco=None, estoque=None, 
                 imagem=None, categoria=None, data_cadastro=None, ativo=True):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.imagem = imagem
        self.categoria = categoria
        self.data_cadastro = data_cadastro if data_cadastro else datetime.now()
        self.ativo = ativo
    
    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    descricao TEXT,
                    preco FLOAT NOT NULL,
                    estoque INT DEFAULT 0,
                    imagem VARCHAR(255),
                    categoria VARCHAR(50),
                    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ativo BOOLEAN DEFAULT TRUE
                )
                ''')
            conn.commit()
        finally:
            conn.close()
    
    def save(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if self.id:
                    # Atualiza um produto existente
                    cursor.execute('''
                    UPDATE produtos SET 
                        nome = %s, 
                        descricao = %s, 
                        preco = %s, 
                        estoque = %s, 
                        imagem = %s, 
                        categoria = %s, 
                        ativo = %s 
                    WHERE id = %s
                    ''', (
                        self.nome, 
                        self.descricao, 
                        self.preco, 
                        self.estoque, 
                        self.imagem, 
                        self.categoria, 
                        self.ativo, 
                        self.id
                    ))
                else:
                    # Insere um novo produto
                    cursor.execute('''
                    INSERT INTO produtos (
                        nome, descricao, preco, estoque, imagem, categoria, data_cadastro, ativo
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        self.nome, 
                        self.descricao, 
                        self.preco, 
                        self.estoque, 
                        self.imagem, 
                        self.categoria, 
                        self.data_cadastro, 
                        self.ativo
                    ))
                    self.id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(produto_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM produtos WHERE id = %s', (produto_id,))
                result = cursor.fetchone()
                if result:
                    return Produto(
                        id=result['id'],
                        nome=result['nome'],
                        descricao=result['descricao'],
                        preco=result['preco'],
                        estoque=result['estoque'],
                        imagem=result['imagem'],
                        categoria=result['categoria'],
                        data_cadastro=result['data_cadastro'],
                        ativo=result['ativo']
                    )
                return None
        finally:
            conn.close()
    
    @staticmethod
    def get_all(only_active=True):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = 'SELECT * FROM produtos'
                if only_active:
                    query += ' WHERE ativo = TRUE'
                query += ' ORDER BY nome'
                
                cursor.execute(query)
                results = cursor.fetchall()
                
                produtos = []
                for result in results:
                    produtos.append(Produto(
                        id=result['id'],
                        nome=result['nome'],
                        descricao=result['descricao'],
                        preco=result['preco'],
                        estoque=result['estoque'],
                        imagem=result['imagem'],
                        categoria=result['categoria'],
                        data_cadastro=result['data_cadastro'],
                        ativo=result['ativo']
                    ))
                return produtos
        finally:
            conn.close()
    
    @staticmethod
    def get_by_categoria(categoria, only_active=True):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = 'SELECT * FROM produtos WHERE categoria = %s'
                if only_active:
                    query += ' AND ativo = TRUE'
                query += ' ORDER BY nome'
                
                cursor.execute(query, (categoria,))
                results = cursor.fetchall()
                
                produtos = []
                for result in results:
                    produtos.append(Produto(
                        id=result['id'],
                        nome=result['nome'],
                        descricao=result['descricao'],
                        preco=result['preco'],
                        estoque=result['estoque'],
                        imagem=result['imagem'],
                        categoria=result['categoria'],
                        data_cadastro=result['data_cadastro'],
                        ativo=result['ativo']
                    ))
                return produtos
        finally:
            conn.close()
    
    @staticmethod
    def search(termo, only_active=True):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                search_term = f'%{termo}%'
                query = 'SELECT * FROM produtos WHERE nome LIKE %s OR descricao LIKE %s'
                if only_active:
                    query += ' AND ativo = TRUE'
                query += ' ORDER BY nome'
                
                cursor.execute(query, (search_term, search_term))
                results = cursor.fetchall()
                
                produtos = []
                for result in results:
                    produtos.append(Produto(
                        id=result['id'],
                        nome=result['nome'],
                        descricao=result['descricao'],
                        preco=result['preco'],
                        estoque=result['estoque'],
                        imagem=result['imagem'],
                        categoria=result['categoria'],
                        data_cadastro=result['data_cadastro'],
                        ativo=result['ativo']
                    ))
                return produtos
        finally:
            conn.close()
    
    @staticmethod
    def delete(produto_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Opção 1: Excluir permanentemente
                # cursor.execute('DELETE FROM produtos WHERE id = %s', (produto_id,))
                
                # Opção 2: Marcar como inativo (soft delete)
                cursor.execute('UPDATE produtos SET ativo = FALSE WHERE id = %s', (produto_id,))
                
                affected_rows = cursor.rowcount
            conn.commit()
            return affected_rows > 0
        finally:
            conn.close()
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'estoque': self.estoque,
            'imagem': self.imagem,
            'categoria': self.categoria,
            'data_cadastro': self.data_cadastro.isoformat() if isinstance(self.data_cadastro, datetime) else self.data_cadastro,
            'ativo': self.ativo
        }
