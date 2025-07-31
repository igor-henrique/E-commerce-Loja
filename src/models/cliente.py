import _mysql_connector
from config import Config

class Cliente:
    def __init__(self, id=None, nome=None, email=None, senha=None, 
                 telefone=None, endereco=None, cidade=None, estado=None, 
                 cep=None, is_admin=False, data_cadastro=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.is_admin = is_admin
        self.data_cadastro = data_cadastro
    
    # Métodos necessários para Flask-Login
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep,
            'is_admin': self.is_admin,
            'data_cadastro': str(self.data_cadastro) if self.data_cadastro else None
        }
    
    @staticmethod
    def create_table():
        """Cria a tabela clientes no banco de dados"""
        conn = None
        try:
            conn = _mysql_connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                port=Config.DB_PORT,
                cursorclass=_mysql_connector.cursors.DictCursor
            )
            
            with conn.cursor() as cursor:
                # Cria a tabela clientes
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clientes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nome VARCHAR(100) NOT NULL,
                        email VARCHAR(100) NOT NULL UNIQUE,
                        senha VARCHAR(255) NOT NULL,
                        telefone VARCHAR(20) DEFAULT '',
                        endereco VARCHAR(255) DEFAULT '',
                        cidade VARCHAR(100) DEFAULT '',
                        estado VARCHAR(2) DEFAULT '',
                        cep VARCHAR(10) DEFAULT '',
                        is_admin BOOLEAN DEFAULT FALSE,
                        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_email (email)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                
                conn.commit()
                print("✅ Tabela 'clientes' criada/verificada com sucesso!")
                
        except _mysql_connector.Error as e:
            print(f"❌ Erro ao criar tabela clientes: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()