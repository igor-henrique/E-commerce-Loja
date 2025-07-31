from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
import uuid
import datetime
import _mysql_connector

from repositories.produto_repository import ProdutoRepository

produto_bp = Blueprint('produto', __name__, url_prefix='/produtos')

# Função auxiliar para verificar extensões de arquivo permitidas
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Função para salvar o arquivo de imagem
def save_image(file):
    if file and allowed_file(file.filename):
        # Gera um nome de arquivo único
        filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4()}_{filename}"
        
        # Salva o arquivo
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Retorna o caminho relativo para o arquivo
        return f"/static/uploads/{filename}"
    
    return None

@produto_bp.route('/')
def listar():
    produtos = ProdutoRepository.get_all()
    return render_template('produtos.html', produtos=produtos)

@produto_bp.route('/<int:produto_id>')
def detalhes(produto_id):
    produto = ProdutoRepository.get_by_id(produto_id)
    if not produto:
        flash('Produto não encontrado', 'danger')
        return redirect(url_for('produto.listar'))
    
    return render_template('produto_detalhes.html', produto=produto)

@produto_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    # Verifica se o usuário é administrador
    if not current_user.is_admin:
        flash('Acesso negado', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = request.form.get('preco')
        estoque = request.form.get('estoque')
        categoria = request.form.get('categoria')
        
        # Validações básicas
        if not nome or not preco:
            flash('Por favor, preencha os campos obrigatórios', 'danger')
            return render_template('admin/produto_form.html')
        
        try:
            preco = float(preco)
            estoque = int(estoque) if estoque else 0
        except ValueError:
            flash('Valores inválidos para preço ou estoque', 'danger')
            return render_template('admin/produto_form.html')
        
        # Processa a imagem
        imagem_url = None
        if 'imagem' in request.files:
            imagem_url = save_image(request.files['imagem'])
        
        # Cria o produto
        produto_data = {
            'nome': nome,
            'descricao': descricao,
            'preco': preco,
            'estoque': estoque,
            'categoria': categoria,
            'imagem_url': imagem_url
        }
        
        produto = ProdutoRepository.create(produto_data)
        
        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('produto.listar'))
    
    return render_template('admin/produto_form.html')

@produto_bp.route('/editar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def editar(produto_id):
    # Verifica se o usuário é administrador
    if not current_user.is_admin:
        flash('Acesso negado', 'danger')
        return redirect(url_for('index'))
    
    produto = ProdutoRepository.get_by_id(produto_id)
    if not produto:
        flash('Produto não encontrado', 'danger')
        return redirect(url_for('produto.listar'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = request.form.get('preco')
        estoque = request.form.get('estoque')
        categoria = request.form.get('categoria')
        ativo = 'ativo' in request.form
        
        # Validações básicas
        if not nome or not preco:
            flash('Por favor, preencha os campos obrigatórios', 'danger')
            return render_template('admin/produto_form.html', produto=produto)
        
        try:
            preco = float(preco)
            estoque = int(estoque) if estoque else 0
        except ValueError:
            flash('Valores inválidos para preço ou estoque', 'danger')
            return render_template('admin/produto_form.html', produto=produto)
        
        # Processa a imagem
        imagem_url = produto.imagem_url
        if 'imagem' in request.files and request.files['imagem'].filename:
            nova_imagem_url = save_image(request.files['imagem'])
            if nova_imagem_url:
                imagem_url = nova_imagem_url
        
        # Atualiza o produto
        produto_data = {
            'nome': nome,
            'descricao': descricao,
            'preco': preco,
            'estoque': estoque,
            'categoria': categoria,
            'imagem_url': imagem_url,
            'ativo': ativo
        }
        
        ProdutoRepository.update(produto_id, produto_data)
        
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produto.detalhes', produto_id=produto_id))
    
    return render_template('admin/produto_form.html', produto=produto)

@produto_bp.route('/excluir/<int:produto_id>', methods=['POST'])
@login_required
def excluir(produto_id):
    # Verifica se o usuário é administrador
    if not current_user.is_admin:
        flash('Acesso negado', 'danger')
        return redirect(url_for('index'))
    
    if ProdutoRepository.delete(produto_id):
        flash('Produto excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir produto', 'danger')
    
    return redirect(url_for('produto.listar'))
