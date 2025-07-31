from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_login import LoginManager, current_user, login_required

import _mysql_connector
import os

# Importa configurações
from config import Config

# Importa modelos
from models.cliente import Cliente
from models.produto import Produto
from models.pedido import Pedido, ItemPedido

# Importa repositórios
from repositories.cliente_repository import ClienteRepository
from repositories.produto_repository import ProdutoRepository
from repositories.pedido_repository import PedidoRepository

# Importa rotas
from routes.auth_routes import auth_bp
from routes.produto_routes import produto_bp
from routes.pedido_routes import pedido_bp

# Cria a aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# Garante que as pastas necessárias existam
os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('templates/auth', exist_ok=True)
os.makedirs('templates/admin', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Registra blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(pedido_bp)

# Configura o gerenciador de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

# Função para carregar o usuário pelo ID
@login_manager.user_loader
def load_user(user_id):
    try:
        return ClienteRepository.get_by_id(int(user_id))
    except:
        return None

# Inicializa o banco de dados
def init_db():
    try:
        # Cria as tabelas se não existirem
        Cliente.create_table()
        Produto.create_table()
        Pedido.create_table()
        ItemPedido.create_table()
        
        # Verifica se já existe um administrador
        admin = ClienteRepository.get_by_email('admin@example.com')
        if not admin:
            # Cria um administrador padrão
            admin_data = {
                'nome': 'Administrador',
                'email': 'admin@example.com',
                'senha': 'admin123',
                'is_admin': True
            }
            ClienteRepository.create(admin_data)
            print('Administrador padrão criado com sucesso!')
            print('Email: admin@example.com')
            print('Senha: admin123')
            
        # Adiciona alguns produtos de exemplo se não existirem
        if len(ProdutoRepository.get_all()) == 0:
            produtos_exemplo = [
                {
                    'nome': 'Notebook Dell',
                    'descricao': 'Notebook Dell Inspiron 15, Intel Core i5, 8GB RAM, 256GB SSD',
                    'preco': 3499.99,
                    'estoque': 10,
                    'categoria': 'Eletrônicos',
                    'imagem': 'notebook.jpg',
                    'ativo': True
                },
                {
                    'nome': 'Mouse Logitech',
                    'descricao': 'Mouse sem fio Logitech M280',
                    'preco': 89.90,
                    'estoque': 50,
                    'categoria': 'Acessórios',
                    'imagem': 'mouse.jpg',
                    'ativo': True
                },
                {
                    'nome': 'Teclado Mecânico',
                    'descricao': 'Teclado Mecânico RGB para Gaming',
                    'preco': 299.99,
                    'estoque': 25,
                    'categoria': 'Acessórios',
                    'imagem': 'teclado.jpg',
                    'ativo': True
                }
            ]
            
            for prod in produtos_exemplo:
                ProdutoRepository.create(prod)
            print('Produtos de exemplo criados!')
            
    except Exception as e:
        print(f'Erro ao inicializar banco de dados: {e}')

# Rota principal
@app.route('/')
def index():
    try:
        produtos = ProdutoRepository.get_all(only_active=True)[:6]
        return render_template('index.html', produtos=produtos)
    except Exception as e:
        print(f"Erro na rota principal: {e}")
        return render_template('index.html', produtos=[])

# Rota para produtos
@app.route('/produtos')
def produtos():
    try:
        produtos = ProdutoRepository.get_all(only_active=True)
        return render_template('produtos.html', produtos=produtos)
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return render_template('produtos.html', produtos=[])

# Rota para carrinho
@app.route('/carrinho')
def carrinho():
    carrinho = session.get('carrinho', [])
    total = 0
    
    # Calcula o total
    for item in carrinho:
        item['subtotal'] = item['preco'] * item['quantidade']
        total += item['subtotal']
    
    return render_template('carrinho.html', carrinho=carrinho, total=total)

# Adicionar ao carrinho
@app.route('/adicionar-carrinho/<int:produto_id>')
def adicionar_carrinho(produto_id):
    try:
        produto = ProdutoRepository.get_by_id(produto_id)
        if not produto:
            flash('Produto não encontrado', 'danger')
            return redirect(url_for('produtos'))
        
        # Obtém o carrinho da sessão
        carrinho = session.get('carrinho', [])
        
        # Verifica se o produto já está no carrinho
        produto_existe = False
        for item in carrinho:
            if item['id'] == produto_id:
                item['quantidade'] += 1
                produto_existe = True
                break
        
        # Se não existe, adiciona
        if not produto_existe:
            carrinho.append({
                'id': produto.id,
                'nome': produto.nome,
                'preco': float(produto.preco),
                'quantidade': 1,
                'imagem': produto.imagem
            })
        
        session['carrinho'] = carrinho
        flash('Produto adicionado ao carrinho!', 'success')
        
    except Exception as e:
        flash(f'Erro ao adicionar produto: {str(e)}', 'danger')
    
    return redirect(request.referrer or url_for('produtos'))

# Remover do carrinho
@app.route('/remover-carrinho/<int:produto_id>')
def remover_carrinho(produto_id):
    carrinho = session.get('carrinho', [])
    carrinho = [item for item in carrinho if item['id'] != produto_id]
    session['carrinho'] = carrinho
    flash('Produto removido do carrinho', 'info')
    return redirect(url_for('carrinho'))

# Atualizar quantidade no carrinho
@app.route('/atualizar-carrinho/<int:produto_id>/<int:quantidade>')
def atualizar_carrinho(produto_id, quantidade):
    if quantidade < 1:
        return remover_carrinho(produto_id)
    
    carrinho = session.get('carrinho', [])
    for item in carrinho:
        if item['id'] == produto_id:
            item['quantidade'] = quantidade
            break
    
    session['carrinho'] = carrinho
    return redirect(url_for('carrinho'))

# Limpar carrinho
@app.route('/limpar-carrinho')
def limpar_carrinho():
    session['carrinho'] = []
    flash('Carrinho limpo', 'info')
    return redirect(url_for('carrinho'))

# Rota para pedidos
@app.route('/pedidos')
@login_required
def pedidos():
    try:
        pedidos = PedidoRepository.get_by_cliente(current_user.id)
        return render_template('pedidos.html', pedidos=pedidos)
    except Exception as e:
        flash(f'Erro ao carregar pedidos: {str(e)}', 'danger')
        return render_template('pedidos.html', pedidos=[])

# Finalizar pedido
@app.route('/finalizar-pedido', methods=['POST'])
@login_required
def finalizar_pedido():
    carrinho = session.get('carrinho', [])
    
    if not carrinho:
        flash('Carrinho vazio', 'warning')
        return redirect(url_for('carrinho'))
    
    try:
        # Calcula o total
        total = sum(item['preco'] * item['quantidade'] for item in carrinho)
        
        # Cria o pedido
        pedido_data = {
            'cliente_id': current_user.id,
            'total': total,
            'status': 'Pendente'
        }
        
        pedido = PedidoRepository.create(pedido_data)
        
        # Adiciona os itens do pedido
        for item in carrinho:
            item_pedido_data = {
                'pedido_id': pedido.id,
                'produto_id': item['id'],
                'quantidade': item['quantidade'],
                'preco_unitario': item['preco']
            }
            ItemPedido.create(**item_pedido_data)
        
        # Limpa o carrinho
        session['carrinho'] = []
        
        flash('Pedido realizado com sucesso!', 'success')
        return redirect(url_for('pedidos'))
        
    except Exception as e:
        flash(f'Erro ao finalizar pedido: {str(e)}', 'danger')
        return redirect(url_for('carrinho'))

# Contexto global para templates
@app.context_processor
def inject_globals():
    try:
        categorias = []
        
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
                cursor.execute('SELECT DISTINCT categoria FROM produtos WHERE ativo = TRUE ORDER BY categoria')
                categorias = [row['categoria'] for row in cursor.fetchall() if row['categoria']]
            
            conn.close()
        except:
            pass
        
        # Obtém quantidade de itens no carrinho
        carrinho = session.get('carrinho', [])
        qtd_carrinho = sum(item.get('quantidade', 0) for item in carrinho)
        
        return {
            'categorias': categorias,
            'qtd_carrinho': qtd_carrinho,
            'ano_atual': datetime.now().year,
            'current_user': current_user
        }
    except Exception as e:
        return {
            'categorias': [],
            'qtd_carrinho': 0,
            'ano_atual': datetime.now().year,
            'current_user': current_user
        }

# Tratamento de erros
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db()
    print("\n" + "="*50)
    print("Servidor Flask iniciado!")
    print("Acesse: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, host='localhost', port=5000)






