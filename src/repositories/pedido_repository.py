from models.pedido import Pedido, ItemPedido
from repositories.produto_repository import ProdutoRepository
import _mysql_connector

class PedidoRepository:
    @staticmethod
    def get_all():
        return Pedido.get_all()
    
    @staticmethod
    def get_by_id(pedido_id):
        return Pedido.get_by_id(pedido_id)
    
    @staticmethod
    def get_by_cliente(cliente_id):
        return Pedido.get_by_cliente(cliente_id)
    
    @staticmethod
    def get_by_status(status):
        return Pedido.get_by_status(status)
    
    @staticmethod
    def create(pedido_data, itens_data):
        # Cria o pedido
        pedido = Pedido(
            cliente_id=pedido_data.get('cliente_id'),
            status=pedido_data.get('status', 'pendente'),
            endereco_entrega=pedido_data.get('endereco_entrega'),
            cidade_entrega=pedido_data.get('cidade_entrega'),
            estado_entrega=pedido_data.get('estado_entrega'),
            cep_entrega=pedido_data.get('cep_entrega'),
            forma_pagamento=pedido_data.get('forma_pagamento'),
            observacoes=pedido_data.get('observacoes')
        )
        
        # Salva o pedido para obter o ID
        pedido.save()
        
        # Adiciona os itens ao pedido
        itens = []
        for item_data in itens_data:
            produto_id = item_data.get('produto_id')
            quantidade = item_data.get('quantidade', 1)
            
            # Obtém o produto para pegar o preço atual
            produto = ProdutoRepository.get_by_id(produto_id)
            if not produto:
                continue
            
            # Verifica estoque
            if produto.estoque < quantidade:
                continue
            
            # Cria o item do pedido
            item = ItemPedido(
                pedido_id=pedido.id,
                produto_id=produto_id,
                quantidade=quantidade,
                preco_unitario=produto.preco,
                produto=produto
            )
            
            # Atualiza o estoque
            ProdutoRepository.update_estoque(produto_id, quantidade, 'subtrair')
            
            # Salva o item
            item.save()
            itens.append(item)
        
        # Atualiza a lista de itens do pedido
        pedido.itens = itens
        
        return pedido
    
    @staticmethod
    def update_status(pedido_id, novo_status):
        pedido = PedidoRepository.get_by_id(pedido_id)
        if not pedido:
            return False
        
        pedido.status = novo_status
        pedido.save()
        return True
    
    @staticmethod
    def cancel(pedido_id):
        pedido = PedidoRepository.get_by_id(pedido_id)
        if not pedido or pedido.status == 'cancelado':
            return False
        
        # Devolve os itens ao estoque
        for item in pedido.itens:
            ProdutoRepository.update_estoque(
                item.produto_id, 
                item.quantidade, 
                'adicionar'
            )
        
        pedido.status = 'cancelado'
        pedido.save()
        return True
    
    @staticmethod
    def add_item(pedido_id, produto_id, quantidade):
        pedido = PedidoRepository.get_by_id(pedido_id)
        if not pedido or pedido.status != 'pendente':
            return False
        
        produto = ProdutoRepository.get_by_id(produto_id)
        if not produto or produto.estoque < quantidade:
            return False
        
        # Verifica se o item já existe no pedido
        item_existente = None
        for item in pedido.itens:
            if item.produto_id == produto_id:
                item_existente = item
                break
        
        if item_existente:
            # Atualiza a quantidade
            nova_quantidade = item_existente.quantidade + quantidade
            
            # Verifica estoque
            if produto.estoque < quantidade:
                return False
            
            item_existente.quantidade = nova_quantidade
            item_existente.save()
            
        else:
            # Cria um novo item
            item = ItemPedido(
                pedido_id=pedido_id,
                produto_id=produto_id,
                quantidade=quantidade,
                preco_unitario=produto.preco,
                produto=produto
            )
            item.save()
            pedido.itens.append(item)
        
        # Atualiza o estoque
        ProdutoRepository.update_estoque(produto_id, quantidade, 'subtrair')
        
        return True
    
    @staticmethod
    def remove_item(pedido_id, item_id):
        pedido = PedidoRepository.get_by_id(pedido_id)
        if not pedido or pedido.status != 'pendente':
            return False
        
        # Encontra o item no pedido
        item_to_remove = None
        for item in pedido.itens:
            if item.id == item_id:
                item_to_remove = item
                break
        
        if not item_to_remove:
            return False
        
        # Devolve ao estoque
        ProdutoRepository.update_estoque(
            item_to_remove.produto_id, 
            item_to_remove.quantidade, 
            'adicionar'
        )
        
        # Remove o item
        ItemPedido.delete(item_id)
        
        # Atualiza a lista de itens do pedido
        pedido.itens = [item for item in pedido.itens if item.id != item_id]
        
        return True
