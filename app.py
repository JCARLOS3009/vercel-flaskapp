from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Configuração da conexão com o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://default:Ew4LKOoIpBv5@ep-falling-hall-a43wfsot.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definindo o modelo de dados (Tabela "pessoa")
class Pessoa(db.Model):
    __tablename__ = 'pessoa'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Pessoa {self.nome}>'

# Criar as tabelas no banco de dados
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    return redirect(url_for('pessoas'))

@app.route('/pessoas')
def pessoas():
    # Número de itens por página
    items_per_page = 5
    page = request.args.get('page', 1, type=int)  # Pega o parâmetro 'page' da URL, se não, usa 1 como padrão

    # Usando o paginate para pegar 5 registros por vez, ordenados pelo id
    pessoas = Pessoa.query.order_by(Pessoa.id).paginate(page=page, per_page=items_per_page, error_out=False)

    return render_template('index.html', pessoas=pessoas.items, 
                           total_pages=pessoas.pages, current_page=pessoas.page)


@app.route('/criar', methods=['GET'])
def criar_pessoa_form():
    return render_template('cadastrar.html')  # Renderiza o template com o formulário de criação

@app.route('/pessoa', methods=['POST'])
def criar_pessoa():
    nome = request.form['nome']
    idade = request.form['idade']
    email = request.form['email']

    # Verificar se o e-mail já existe
    pessoa_existente = Pessoa.query.filter_by(email=email).first()
    if pessoa_existente:
        return redirect(url_for('pessoas'))

    # Tentar adicionar a nova pessoa ao banco
    nova_pessoa = Pessoa(nome=nome, idade=idade, email=email)
    db.session.add(nova_pessoa)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return redirect(url_for('pessoas'))

    return redirect(url_for('pessoas'))

@app.route('/excluir/<int:id>', methods=['GET'])
def excluir(id):
    pessoa = Pessoa.query.get(id)
    if pessoa:
        db.session.delete(pessoa)
        db.session.commit()
    return redirect(url_for('pessoas'))

@app.route('/pessoa/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pessoa = Pessoa.query.get(id)

    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.idade = request.form['idade']
        pessoa.email = request.form['email']

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect(url_for('editar', id=id))

        return redirect(url_for('pessoas'))

    return render_template('editar.html', pessoa=pessoa)

# Chamando a função de criar tabelas
create_tables()

if __name__ == '__main__':
    app.run(debug=True)
