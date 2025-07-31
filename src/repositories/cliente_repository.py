# repositories/cliente_repository.py
import _mysql_connector
from werkzeug.security import generate_password_hash, check_password_hash
from models.cliente import Cliente
from config import Config

class ClienteRepository:
    
    @staticmethod
    def get_connection():
        """Retorna uma conexão com o banco de dados"""
        return _mysql_connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=int(Config.DB_PORT) if isinstance(Config.DB_PORT, str) else Config.DB_PORT,
            cursorclass=_mysql_connector.cursors.DictCursor
        )
    
    @staticmethod
    def create(cliente_data):
        """Cria um novo cliente"""
        print(f"\n🔍 Tentando criar cliente: {cliente_data.get('email')}")
        conn = None
        
        try:
            conn = ClienteRepository.get_connection()
            print("✅ Conexão com banco estabelecida!")
            
            with conn.cursor() as cursor:
                # Hash da senha
                senha_hash = generate_password_hash(cliente_data['senha'])
                
                # SQL para inserir cliente
                sql = """
                    INSERT INTO clientes 
                    (nome, email, senha, telefone, endereco, cidade, estado, cep, is_admin)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                valores = (
                    cliente_data.get('nome'),
                    cliente_data.get('email'),
                    senha_hash,
                    cliente_data.get('telefone', ''),
                    cliente_data.get('endereco', ''),
                    cliente_data.get('cidade', ''),
                    cliente_data.get('estado', ''),
                    cliente_data.get('cep', ''),
                    1 if cliente_data.get('is_admin', False) else 0
                )
                
                cursor.execute(sql, valores)
                conn.commit()
                
                # Retorna o cliente criado
                cliente_id = cursor.lastrowid
                print(f"✅ Cliente criado com ID: {cliente_id}")
                return ClienteRepository.get_by_id(cliente_id)
                
        except _mysql_connector.err.OperationalError as e:
            print(f"❌ Erro operacional MySQL: {e}")
            if e.args[0] == 2003:
                raise Exception("MySQL não está rodando. Inicie o serviço MySQL.")
            elif e.args[0] == 1049:
                raise Exception(f"Banco de dados '{Config.DB_NAME}' não existe.")
            else:
                raise Exception(f"Erro de conexão MySQL: {e}")
                
        except _mysql_connector.err.IntegrityError as e:
            print(f"❌ Erro de integridade: {e}")
            if "Duplicate entry" in str(e):
                raise Exception("Este email já está cadastrado!")
            else:
                raise Exception(f"Erro de integridade: {e}")
                
        except Exception as e:
            print(f"❌ Erro geral: {e}")
            if conn:
                conn.rollback()
            raise e
            
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_by_id(cliente_id):
        """Busca um cliente pelo ID"""
        conn = None
        try:
            conn = ClienteRepository.get_connection()
            with conn.cursor() as cursor:
                sql = "SELECT * FROM clientes WHERE id = %s"
                cursor.execute(sql, (cliente_id,))
                result = cursor.fetchone()
                
                if result:
                    cliente = Cliente(
                        id=result['id'],
                        nome=result['nome'],
                        email=result['email'],
                        senha=result['senha'],
                        data_cadastro=result.get('data_cadastro')
                    )
                    # Adiciona atributos extras se existirem
                    cliente.telefone = result.get('telefone', '')
                    cliente.endereco = result.get('endereco', '')
                    cliente.cidade = result.get('cidade', '')
                    cliente.estado = result.get('estado', '')
                    cliente.cep = result.get('cep', '')
                    cliente.is_admin = bool(result.get('is_admin', False))
                    return cliente
                return None
                
        except Exception as e:
            print(f"❌ Erro ao buscar cliente por ID: {e}")
            raise e
            
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_by_email(email):
        """Busca um cliente pelo email"""
        conn = None
        try:
            conn = ClienteRepository.get_connection()
            with conn.cursor() as cursor:
                sql = "SELECT * FROM clientes WHERE email = %s"
                cursor.execute(sql, (email,))
                result = cursor.fetchone()
                
                if result:
                    cliente = Cliente(
                        id=result['id'],
                        nome=result['nome'],
                        email=result['email'],
                        senha=result['senha'],
                        data_cadastro=result.get('data_cadastro')
                    )
                    # Adiciona atributos extras se existirem
                    cliente.telefone = result.get('telefone', '')
                    cliente.endereco = result.get('endereco', '')
                    cliente.cidade = result.get('cidade', '')
                    cliente.estado = result.get('estado', '')
                    cliente.cep = result.get('cep', '')
                    cliente.is_admin = bool(result.get('is_admin', False))
                    return cliente
                return None
                
        except Exception as e:
            print(f"❌ Erro ao buscar cliente por email: {e}")
            raise e
            
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def authenticate(email, senha):
        """Autentica um cliente"""
        try:
            cliente = ClienteRepository.get_by_email(email)
            if cliente and check_password_hash(cliente.senha, senha):
                return cliente
            return None
        except Exception as e:
            print(f"❌ Erro na autenticação: {e}")
            return None
    
    @staticmethod
    def update(cliente_id, cliente_data):
        """Atualiza os dados de um cliente"""
        conn = None
        try:
            conn = ClienteRepository.get_connection()
            with conn.cursor() as cursor:
                # Campos que podem ser atualizados
                update_fields = []
                values = []
                
                if 'nome' in cliente_data:
                    update_fields.append("nome = %s")
                    values.append(cliente_data['nome'])
                
                if 'telefone' in cliente_data:
                    update_fields.append("telefone = %s")
                    values.append(cliente_data['telefone'])
                
                if 'endereco' in cliente_data:
                    update_fields.append("endereco = %s")
                    values.append(cliente_data['endereco'])
                
                if 'cidade' in cliente_data:
                    update_fields.append("cidade = %s")
                    values.append(cliente_data['cidade'])
                
                if 'estado' in cliente_data:
                    update_fields.append("estado = %s")
                    values.append(cliente_data['estado'])
                
                if 'cep' in cliente_data:
                    update_fields.append("cep = %s")
                    values.append(cliente_data['cep'])
                
                if 'senha' in cliente_data and cliente_data['senha']:
                    update_fields.append("senha = %s")
                    values.append(generate_password_hash(cliente_data['senha']))
                
                if update_fields:
                    values.append(cliente_id)
                    sql = f"UPDATE clientes SET {', '.join(update_fields)} WHERE id = %s"
                    cursor.execute(sql, values)
                    conn.commit()
                
                return ClienteRepository.get_by_id(cliente_id)
                
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"❌ Erro ao atualizar cliente: {e}")
            raise e
            
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def delete(cliente_id):
        """Deleta um cliente"""
        conn = None
        try:
            conn = ClienteRepository.get_connection()
            with conn.cursor() as cursor:
                sql = "DELETE FROM clientes WHERE id = %s"
                cursor.execute(sql, (cliente_id,))
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"❌ Erro ao deletar cliente: {e}")
            raise e
            
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_all():
        """Retorna todos os clientes"""
        conn = None
        try:
            conn = ClienteRepository.get_connection()
            with conn.cursor() as cursor:
                sql = "SELECT * FROM clientes ORDER BY nome"
                cursor.execute(sql)
                results = cursor.fetchall()
                
                clientes = []
                for result in results:
                    cliente = Cliente(
                        id=result['id'],
                        nome=result['nome'],
                        email=result['email'],
                        senha=result['senha'],
                        data_cadastro=result.get('data_cadastro')
                    )
                    # Adiciona atributos extras
                    cliente.telefone = result.get('telefone', '')
                    cliente.endereco = result.get('endereco', '')
                    cliente.cidade = result.get('cidade', '')
                    cliente.estado = result.get('estado', '')
                    cliente.cep = result.get('cep', '')
                    cliente.is_admin = bool(result.get('is_admin', False))
                    clientes.append(cliente)
                
                return clientes
                
        except Exception as e:
            print(f"❌ Erro ao listar clientes: {e}")
            raise e
            
        finally:
            if conn:
                conn.close()