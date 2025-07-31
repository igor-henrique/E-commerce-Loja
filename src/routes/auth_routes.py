from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from repositories.cliente_repository import ClienteRepository
from werkzeug.security import check_password_hash
import _mysql_connector
import traceback

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip()
            senha = request.form.get('senha', '').strip()
            
            if not email or not senha:
                flash('Por favor, preencha todos os campos.', 'danger')
                return render_template('login.html')
            
            # Autentica o usuário
            cliente = ClienteRepository.authenticate(email, senha)
            
            if cliente:
                login_user(cliente)
                
                # Redireciona para a página anterior ou index
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Email ou senha incorretos.', 'danger')
                
        except Exception as e:
            print(f"Erro no login: {e}")
            print(traceback.format_exc())
            flash('Erro ao fazer login. Tente novamente.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            # Debug - mostra o que foi recebido
            print("\n=== DADOS DO FORMULÁRIO ===")
            for key, value in request.form.items():
                print(f"{key}: {value}")
            print("========================\n")
            
            # Captura os dados do formulário
            nome = request.form.get('nome', '').strip()
            email = request.form.get('email', '').strip()
            senha = request.form.get('senha', '').strip()
            confirmar_senha = request.form.get('confirmar_senha', '').strip()
            
            # Validações
            if not nome or not email or not senha:
                flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
                return render_template('cadastro.html')
            
            if senha != confirmar_senha:
                flash('As senhas não coincidem!', 'danger')
                return render_template('cadastro.html')
            
            if len(senha) < 6:
                flash('A senha deve ter pelo menos 6 caracteres!', 'danger')
                return render_template('cadastro.html')
            
            # Verifica se o email já existe
            try:
                usuario_existente = ClienteRepository.get_by_email(email)
                if usuario_existente:
                    flash('Este email já está cadastrado!', 'danger')
                    return render_template('cadastro.html')
            except Exception as e:
                print(f"Erro ao verificar email existente: {e}")
                flash('Erro ao verificar email. Verifique a conexão com o banco de dados.', 'danger')
                return render_template('cadastro.html')
            
            # Prepara os dados do cliente
            cliente_data = {
                'nome': nome,
                'email': email,
                'senha': senha,
                'telefone': request.form.get('telefone', ''),
                'endereco': request.form.get('endereco', ''),
                'cidade': request.form.get('cidade', ''),
                'estado': request.form.get('estado', ''),
                'cep': request.form.get('cep', ''),
                'is_admin': False
            }
            
            print(f"Tentando criar cliente: {cliente_data['email']}")
            
            # Cria o cliente
            novo_cliente = ClienteRepository.create(cliente_data)
            
            if novo_cliente:
                # Faz login automático
                login_user(novo_cliente)
                flash('Conta criada com sucesso! Bem-vindo!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Erro ao criar conta. Tente novamente.', 'danger')
                
        except Exception as e:  # A variável 'e' é definida aqui
            error_msg = str(e)
            print(f"\n❌ ERRO ao criar conta: {type(e).__name__}: {error_msg}")
            print("Traceback completo:")
            print(traceback.format_exc())
            
            # Tratamento específico de erros
            if "MySQL não está rodando" in error_msg:
                flash('Erro: MySQL não está rodando. Inicie o serviço MySQL.', 'danger')
            elif "não existe" in error_msg:
                flash('Erro: Banco de dados não encontrado. Execute o script de instalação.', 'danger')
            elif "já está cadastrado" in error_msg:
                flash('Este email já está cadastrado!', 'danger')
            else:
                flash(f'Erro ao criar conta: {error_msg}', 'danger')
    
    return render_template('cadastro.html')
                
        # except Exception as e:
        #     print(f"\n❌ ERRO ao criar conta: {type(e).__name__}: {e}")
        #     print("Traceback completo:")
        #     print(traceback.format_exc())
        #     flash(f'Erro ao criar conta. Verifique se o MySQL está rodando.', 'danger')
    if "MySQL não está rodando" in error_msg:
        flash('Erro: MySQL não está rodando. Inicie o serviço MySQL.', 'danger')
    elif "não existe" in error_msg:
        flash('Erro: Banco de dados não encontrado. Execute o script de instalação.', 'danger')
    elif "já está cadastrado" in error_msg:
        flash('Este email já está cadastrado!', 'danger')
    else:
        flash(f'Erro ao criar conta: {error_msg}', 'danger')

    
    return render_template('cadastro.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/perfil')
@login_required
def profile():
    return render_template('auth/profile.html')