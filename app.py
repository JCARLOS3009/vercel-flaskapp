from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Adicione essa importação
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

@app.route('/test-db')
def test_db_connection():
    try:
        # Use a função text() para a consulta SQL
        db.session.execute(text('SELECT 1'))  # Agora 'text' está definido
        db.session.commit()  # Se não houver erro, a conexão foi bem-sucedida
        return "Conexão com o banco de dados PostgreSQL bem-sucedida!"
    except OperationalError as e:
        # Caso haja erro na conexão
        return f"Erro ao conectar com o banco de dados: {e}"

@app.route('/')
def home():
    return "Hello, Vercel!"

if __name__ == '__main__':
    app.run(debug=True)
