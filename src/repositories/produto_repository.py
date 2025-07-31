from models.produto import Produto
import _mysql_connector


class ProdutoRepository:
    @staticmethod
    def get_all(only_active=True):
        return Produto.get_all(only_active)
    
    @staticmethod
    def get_by_id(produto_id):
        return Produto.get_by_id(produto_id)
    
    @staticmethod
    def get_by_categoria(categoria, only_active=True):
        return Produto.get_by_categoria(categoria, only_active)
    
    @staticmethod
    def search(termo, only_active=True):
        return Produto.search(termo, only_active)
    
    @staticmethod
    def create(produto_data):
        produto = Produto(
            nome=produto_data.get('nome'),
            descricao=produto_data.get('descricao'),
            preco=produto_data.get('preco'),
            estoque=produto_data.get('estoque', 0),
            imagem=produto_data.get('imagem'),
            categoria=produto_data.get('categoria'),
            ativo=produto_data.get('ativo', True)
        )
        produto.save()
        return produto
    
    @staticmethod
    def update(produto_id, produto_data):
        produto = ProdutoRepository.get_by_id(produto_id)
        if not produto:
            return None
        
        # Atualiza os campos
        if 'nome' in produto_data:
            produto.nome = produto_data['nome']
        if 'descricao' in produto_data:
            produto.descricao = produto_data['descricao']
        if 'preco' in produto_data:
            produto.preco = produto_data['preco']
        if 'estoque' in produto_data:
            produto.estoque = produto_data['estoque']
        if 'imagem' in produto_data:
            produto.imagem_url = produto_data['imagem']
        if 'categoria' in produto_data:
            produto.categoria = produto_data['categoria']
        if 'ativo' in produto_data:
            produto.ativo = produto_data['ativo']
        
        produto.save()
        return produto
    
    @staticmethod
    def delete(produto_id):
        return Produto.delete(produto_id)
    
    @staticmethod
    def update_estoque(produto_id, quantidade, operacao='subtrair'):
        produto = ProdutoRepository.get_by_id(produto_id)
        if not produto:
            return False
        
        if operacao == 'adicionar':
            produto.estoque += quantidade
        elif operacao == 'subtrair':
            if produto.estoque < quantidade:
                return False  # Estoque insuficiente
            produto.estoque -= quantidade
        else:
            return False  # Operação inválida
        
        produto.save()
        return True
