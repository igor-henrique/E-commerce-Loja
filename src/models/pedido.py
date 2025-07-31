import _mysql_connector
from datetime import datetime
from config import Config
from models.produto import Produto
from models.cliente import Cliente

# Função para obter conexão com o banco de dados
def get_db_connection():
    return _mysql_connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT,
        cursorclass=_mysql_connector.cursors.DictCursor
    )

class ItemPedido:
    def __init__(self, id=None, pedido_id=None, produto_id=None, quantidade=None, 
                 preco_unitario=None, produto=None):
        self.id = id
        self.pedido_id = pedido_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.produto = produto  # Objeto Produto
    
    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario
    
    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS itens_pedido (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    pedido_id INT NOT NULL,
                    produto_id INT NOT NULL,
                    quantidade INT NOT NULL DEFAULT 1,
                    preco_unitario FLOAT NOT NULL,
                    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
                    FOREIGN KEY (produto_id) REFERENCES produtos(id)
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
                    # Atualiza um item existente
                    cursor.execute('''
                    UPDATE itens_pedido SET 
                        pedido_id = %s, 
                        produto_id = %s, 
                        quantidade = %s, 
                        preco_unitario = %s
                    WHERE id = %s
                    ''', (
                        self.pedido_id, 
                        self.produto_id, 
                        self.quantidade, 
                        self.preco_unitario, 
                        self.id
                    ))
                else:
                    # Insere um novo item
                    cursor.execute('''
                    INSERT INTO itens_pedido (
                        pedido_id, produto_id, quantidade, preco_unitario
                    ) VALUES (%s, %s, %s, %s)
                    ''', (
                        self.pedido_id, 
                        self.produto_id, 
                        self.quantidade, 
                        self.preco_unitario
                    ))
                    self.id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def get_by_pedido(pedido_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                SELECT i.*, p.nome as produto_nome 
                FROM itens_pedido i
                JOIN produtos p ON i.produto_id = p.id
                WHERE i.pedido_id = %s
                ''', (pedido_id,))
                results = cursor.fetchall()
                
                itens = []
                for result in results:
                    produto = Produto.get_by_id(result['produto_id'])
                    item = ItemPedido(
                        id=result['id'],
                        pedido_id=result['pedido_id'],
                        produto_id=result['produto_id'],
                        quantidade=result['quantidade'],
                        preco_unitario=result['preco_unitario'],
                        produto=produto
                    )
                    itens.append(item)
                return itens
        finally:
            conn.close()
    
    @staticmethod
    def delete(item_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM itens_pedido WHERE id = %s', (item_id,))
                affected_rows = cursor.rowcount
            conn.commit()
            return affected_rows > 0
        finally:
            conn.close()
    
    def to_dict(self):
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'produto_id': self.produto_id,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.subtotal,
            'produto': self.produto.nome if self.produto else None
        }

class Pedido:
    def __init__(self, id=None, cliente_id=None, data_pedido=None, status=None, 
                 endereco_entrega=None, cidade_entrega=None, estado_entrega=None, 
                 cep_entrega=None, forma_pagamento=None, observacoes=None, 
                 cliente=None, itens=None):
        self.id = id
        self.cliente_id = cliente_id
        self.data_pedido = data_pedido if data_pedido else datetime.now()
        self.status = status if status else 'pendente'
        self.endereco_entrega = endereco_entrega
        self.cidade_entrega = cidade_entrega
        self.estado_entrega = estado_entrega
        self.cep_entrega = cep_entrega
        self.forma_pagamento = forma_pagamento
        self.observacoes = observacoes
        self.cliente = cliente  # Objeto Cliente
        self.itens = itens if itens else []  # Lista de objetos ItemPedido
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.itens)
    
    @property
    def quantidade_itens(self):
        return sum(item.quantidade for item in self.itens)
    
    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    cliente_id INT NOT NULL,
                    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'pendente',
                    endereco_entrega VARCHAR(255),
                    cidade_entrega VARCHAR(100),
                    estado_entrega VARCHAR(2),
                    cep_entrega VARCHAR(10),
                    forma_pagamento VARCHAR(50),
                    observacoes TEXT,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
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
                    # Atualiza um pedido existente
                    cursor.execute('''
                    UPDATE pedidos SET 
                        cliente_id = %s, 
                        status = %s, 
                        endereco_entrega = %s, 
                        cidade_entrega = %s, 
                        estado_entrega = %s, 
                        cep_entrega = %s, 
                        forma_pagamento = %s, 
                        observacoes = %s
                    WHERE id = %s
                    ''', (
                        self.cliente_id, 
                        self.status, 
                        self.endereco_entrega, 
                        self.cidade_entrega, 
                        self.estado_entrega, 
                        self.cep_entrega, 
                        self.forma_pagamento, 
                        self.observacoes, 
                        self.id
                    ))
                else:
                    # Insere um novo pedido
                    cursor.execute('''
                    INSERT INTO pedidos (
                        cliente_id, data_pedido, status, endereco_entrega, cidade_entrega, 
                        estado_entrega, cep_entrega, forma_pagamento, observacoes
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        self.cliente_id, 
                        self.data_pedido, 
                        self.status, 
                        self.endereco_entrega, 
                        self.cidade_entrega, 
                        self.estado_entrega, 
                        self.cep_entrega, 
                        self.forma_pagamento, 
                        self.observacoes
                    ))
                    self.id = cursor.lastrowid
            conn.commit()
            
            # Salva os itens do pedido
            if self.itens and self.id:
                for item in self.itens:
                    item.pedido_id = self.id
                    item.save()
                    
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(pedido_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM pedidos WHERE id = %s', (pedido_id,))
                result = cursor.fetchone()
                if result:
                    # Obtém o cliente
                    cliente = Cliente.get_by_id(result['cliente_id'])
                    
                    # Obtém os itens do pedido
                    itens = ItemPedido.get_by_pedido(pedido_id)
                    
                    return Pedido(
                        id=result['id'],
                        cliente_id=result['cliente_id'],
                        data_pedido=result['data_pedido'],
                        status=result['status'],
                        endereco_entrega=result['endereco_entrega'],
                        cidade_entrega=result['cidade_entrega'],
                        estado_entrega=result['estado_entrega'],
                        cep_entrega=result['cep_entrega'],
                        forma_pagamento=result['forma_pagamento'],
                        observacoes=result['observacoes'],
                        cliente=cliente,
                        itens=itens
                    )
                return None
        finally:
            conn.close()
    
    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM pedidos ORDER BY data_pedido DESC')
                results = cursor.fetchall()
                
                pedidos = []
                for result in results:
                    # Obtém o cliente
                    cliente = Cliente.get_by_id(result['cliente_id'])
                    
                    # Obtém os itens do pedido
                    itens = ItemPedido.get_by_pedido(result['id'])
                    
                    pedidos.append(Pedido(
                        id=result['id'],
                        cliente_id=result['cliente_id'],
                        data_pedido=result['data_pedido'],
                        status=result['status'],
                        endereco_entrega=result['endereco_entrega'],
                        cidade_entrega=result['cidade_entrega'],
                        estado_entrega=result['estado_entrega'],
                        cep_entrega=result['cep_entrega'],
                        forma_pagamento=result['forma_pagamento'],
                        observacoes=result['observacoes'],
                        cliente=cliente,
                        itens=itens
                    ))
                return pedidos
        finally:
            conn.close()
    
    @staticmethod
    def get_by_cliente(cliente_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM pedidos WHERE cliente_id = %s ORDER BY data_pedido DESC', (cliente_id,))
                results = cursor.fetchall()
                
                pedidos = []
                for result in results:
                    # Obtém o cliente
                    cliente = Cliente.get_by_id(result['cliente_id'])
                    
                    # Obtém os itens do pedido
                    itens = ItemPedido.get_by_pedido(result['id'])
                    
                    pedidos.append(Pedido(
                        id=result['id'],
                        cliente_id=result['cliente_id'],
                        data_pedido=result['data_pedido'],
                        status=result['status'],
                        endereco_entrega=result['endereco_entrega'],
                        cidade_entrega=result['cidade_entrega'],
                        estado_entrega=result['estado_entrega'],
                        cep_entrega=result['cep_entrega'],
                        forma_pagamento=result['forma_pagamento'],
                        observacoes=result['observacoes'],
                        cliente=cliente,
                        itens=itens
                    ))
                return pedidos
        finally:
            conn.close()
    
    @staticmethod
    def get_by_status(status):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM pedidos WHERE status = %s ORDER BY data_pedido DESC', (status,))
                results = cursor.fetchall()
                
                pedidos = []
                for result in results:
                    # Obtém o cliente
                    cliente = Cliente.get_by_id(result['cliente_id'])
                    
                    # Obtém os itens do pedido
                    itens = ItemPedido.get_by_pedido(result['id'])
                    
                    pedidos.append(Pedido(
                        id=result['id'],
                        cliente_id=result['cliente_id'],
                        data_pedido=result['data_pedido'],
                        status=result['status'],
                        endereco_entrega=result['endereco_entrega'],
                        cidade_entrega=result['cidade_entrega'],
                        estado_entrega=result['estado_entrega'],
                        cep_entrega=result['cep_entrega'],
                        forma_pagamento=result['forma_pagamento'],
                        observacoes=result['observacoes'],
                        cliente=cliente,
                        itens=itens
                    ))
                return pedidos
        finally:
            conn.close()
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'data_pedido': self.data_pedido.isoformat() if isinstance(self.data_pedido, datetime) else self.data_pedido,
            'status': self.status,
            'endereco_entrega': self.endereco_entrega,
            'cidade_entrega': self.cidade_entrega,
            'estado_entrega': self.estado_entrega,
            'cep_entrega': self.cep_entrega,
            'forma_pagamento': self.forma_pagamento,
            'observacoes': self.observacoes,
            'total': self.total,
            'quantidade_itens': self.quantidade_itens,
            'itens': [item.to_dict() for item in self.itens]
        }
