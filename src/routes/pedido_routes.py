from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
import _mysql_connector

from repositories.produto_repository import ProdutoRepository
from repositories.pedido_repository import PedidoRepository

pedido_bp = Blueprint('pedido', __name__)

@pedido_bp.route('/carrinho')
def carrinho():
    # Obtém o carrinho da sessão
    carrinho = session.get('carrinho', [])
    
    # Calcula o total
    total = 0
    itens_carrinho = []
    
    for item in carrinho:
        produto = ProdutoRepository.get_by_id(item['produto_id'])
        if produto:
            subtotal = produto.preco * item['quantidade']
            total += subtotal
            
            itens_carrinho.append({
                'produto': produto,
                'quantidade': item['quantidade'],
                'subtotal': subtotal
            })
    
    return render_template('carrinho.html', itens=itens_carrinho, total=total)

@pedido_bp.route('/carrinho/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_carrinho(produto_id):
    produto = ProdutoRepository.get_by_id(produto_id)
    if not produto:
        flash('Produto não encontrado', 'danger')
        return redirect(url_for('index'))
    
    # Obtém a quantidade do formulário
    quantidade = int(request.form.get('quantidade', 1))
    
    # Verifica estoque
    if produto.estoque < quantidade:
        flash('Quantidade indisponível em estoque', 'danger')
        return redirect(url_for('produto.detalhes', produto_id=produto_id))
    
    # Obtém o carrinho atual
    carrinho = session.get('carrinho', [])
    
    # Verifica se o produto já está no carrinho
    for item in carrinho:
        if item['produto_id'] == produto_id:
            # Atualiza a quantidade
            item['quantidade'] += quantidade
            session['carrinho'] = carrinho
            flash('Quantidade atualizada no carrinho', 'success')
            return redirect(url_for('pedido.carrinho'))
    
    # Adiciona o produto ao carrinho
    carrinho.append({
        'produto_id': produto_id,
        'quantidade': quantidade
    })
    
    session['carrinho'] = carrinho
    flash('Produto adicionado ao carrinho', 'success')
    
    return redirect(url_for('pedido.carrinho'))

@pedido_bp.route('/carrinho/atualizar/<int:produto_id>', methods=['POST'])
def atualizar_carrinho(produto_id):
    # Obtém a nova quantidade
    quantidade = int(request.form.get('quantidade', 1))
    
    # Verifica estoque
    produto = ProdutoRepository.get_by_id(produto_id)
    if not produto:
        flash('Produto não encontrado', 'danger')
        return redirect(url_for('pedido.carrinho'))
    
    if produto.estoque < quantidade:
        flash('Quantidade indisponível em estoque', 'danger')
        return redirect(url_for('pedido.carrinho'))
    
    # Atualiza o carrinho
    carrinho = session.get('carrinho', [])
    
    for item in carrinho:
        if item['produto_id'] == produto_id:
            item['quantidade'] = quantidade
            break
    
    session['carrinho'] = carrinho
    flash('Carrinho atualizado', 'success')
    
    return redirect(url_for('pedido.carrinho'))

@pedido_bp.route('/carrinho/remover/<int:produto_id>', methods=['POST'])
def remover_carrinho(produto_id):
    # Remove o produto do carrinho
    carrinho = session.get('carrinho', [])
    
    carrinho = [item for item in carrinho if item['produto_id'] != produto_id]
    
    session['carrinho'] = carrinho
    flash('Produto removido do carrinho', 'success')
    
    return redirect(url_for('pedido.carrinho'))

@pedido_bp.route('/carrinho/limpar', methods=['POST'])
def limpar_carrinho():
    # Limpa o carrinho
    session['carrinho'] = []
    flash('Carrinho esvaziado', 'success')
    
    return redirect(url_for('pedido.carrinho'))

@pedido_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    # Obtém o carrinho
    carrinho = session.get('carrinho', [])
    
    if not carrinho:
        flash('Seu carrinho está vazio', 'warning')
        return redirect(url_for('pedido.carrinho'))
    
    # Calcula o total
    total = 0
    itens_carrinho = []
    
    for item in carrinho:
        produto = ProdutoRepository.get_by_id(item['produto_id'])
        if produto:
            subtotal = produto.preco * item['quantidade']
            total += subtotal
            
            itens_carrinho.append({
                'produto': produto,
                'quantidade': item['quantidade'],
                'subtotal': subtotal
            })
    
    if request.method == 'POST':
        # Obtém os dados do formulário
        endereco = request.form.get('endereco')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        cep = request.form.get('cep')
        forma_pagamento = request.form.get('forma_pagamento')
        observacoes = request.form.get('observacoes')
        
        # Validações básicas
        if not endereco or not cidade or not estado or not cep or not forma_pagamento:
            flash('Por favor, preencha todos os campos obrigatórios', 'danger')
            return render_template('checkout.html', itens=itens_carrinho, total=total)
        
        # Cria o pedido
        pedido_data = {
            'cliente_id': current_user.id,
            'endereco_entrega': endereco,
            'cidade_entrega': cidade,
            'estado_entrega': estado,
            'cep_entrega': cep,
            'forma_pagamento': forma_pagamento,
            'observacoes': observacoes
        }
        
        # Prepara os itens do pedido
        itens_data = []
        for item in carrinho:
            itens_data.append({
                'produto_id': item['produto_id'],
                'quantidade': item['quantidade']
            })
        
        # Cria o pedido
        pedido = PedidoRepository.create(pedido_data, itens_data)
        
        if pedido:
            # Limpa o carrinho
            session['carrinho'] = []
            
            flash('Pedido realizado com sucesso!', 'success')
            return redirect(url_for('pedido.confirmacao', pedido_id=pedido.id))
        else:
            flash('Erro ao processar o pedido', 'danger')
    
    return render_template('checkout.html', itens=itens_carrinho, total=total)

@pedido_bp.route('/confirmacao/<int:pedido_id>')
@login_required
def confirmacao(pedido_id):
    pedido = PedidoRepository.get_by_id(pedido_id)
    
    if not pedido or pedido.cliente_id != current_user.id:
        flash('Pedido não encontrado', 'danger')
        return redirect(url_for('index'))
    
    return render_template('confirmacao.html', pedido=pedido)

@pedido_bp.route('/meus-pedidos')
@login_required
def meus_pedidos():
    pedidos = PedidoRepository.get_by_cliente(current_user.id)
    return render_template('meus_pedidos.html', pedidos=pedidos)

@pedido_bp.route('/pedido/<int:pedido_id>')
@login_required
def detalhes_pedido(pedido_id):
    pedido = PedidoRepository.get_by_id(pedido_id)
    
    if not pedido or (pedido.cliente_id != current_user.id and not current_user.is_admin):
        flash('Pedido não encontrado', 'danger')
        return redirect(url_for('index'))
    
    return render_template('pedido_detalhes.html', pedido=pedido)

@pedido_bp.route('/admin/pedidos')
@login_required
def admin_pedidos():
    # Verifica se o usuário é administrador
    if not current_user.is_admin:
        flash('Acesso negado', 'danger')
        return redirect(url_for('index'))
    
    status = request.args.get('status', '')
    
    if status:
        pedidos = PedidoRepository.get_by_status(status)
    else:
        pedidos = PedidoRepository.get_all()
    
    return render_template('admin/pedidos.html', pedidos=pedidos, status_atual=status)

@pedido_bp.route('/admin/pedido/<int:pedido_id>/status', methods=['POST'])
@login_required
def atualizar_status(pedido_id):
    # Verifica se o usuário é administrador
    if not current_user.is_admin:
        flash('Acesso negado', 'danger')
        return redirect(url_for('index'))
    
    novo_status = request.form.get('status')
    
    if PedidoRepository.update_status(pedido_id, novo_status):
        flash('Status atualizado com sucesso', 'success')
    else:
        flash('Erro ao atualizar status', 'danger')
    
    return redirect(url_for('pedido.detalhes_pedido', pedido_id=pedido_id))

@pedido_bp.route('/admin/pedido/<int:pedido_id>/cancelar', methods=['POST'])
@login_required
def cancelar_pedido(pedido_id):
    # Verifica se o usuário é administrador
    if not current_user.is_admin:
        flash('Acesso negado', 'danger')
        return redirect(url_for('index'))
    
    if PedidoRepository.cancel(pedido_id):
        flash('Pedido cancelado com sucesso', 'success')
    else:
        flash('Erro ao cancelar pedido', 'danger')
    
    return redirect(url_for('pedido.detalhes_pedido', pedido_id=pedido_id))
