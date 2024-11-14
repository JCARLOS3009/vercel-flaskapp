import unittest
from app import app, db, Pessoa  # Importa a aplicação Flask, o banco de dados e o modelo Pessoa
from sqlalchemy.exc import IntegrityError
from datetime import date

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configuração do banco de dados e da aplicação para os testes"""
        cls.app = app.test_client()  # Cliente de teste do Flask
        cls.app.testing = True

        # Cria o banco de dados de teste
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Limpeza após todos os testes"""
        with app.app_context():
            db.drop_all()  # Exclui todas as tabelas
            db.session.remove()

    def setUp(self):
        """Limpeza da tabela antes de cada teste"""
        with app.app_context():
            db.session.query(Pessoa).delete()  # Exclui todos os registros
            db.session.commit()

    def test_criar_pessoa(self):
        """Teste de criação de uma pessoa"""
        # Usa uma data de nascimento no formato YYYY-MM-DD
        data_nascimento = date(1993, 4, 15)  # Exemplo de data de nascimento
        response = self.app.post('/pessoa', data=dict(nome='João', data_nascimento=data_nascimento, email='joao@example.com'))

        # Espera um redirecionamento após a criação
        self.assertEqual(response.status_code, 302)

        # Verifica se a pessoa foi criada no banco de dados
        with app.app_context():
            pessoa = Pessoa.query.filter_by(nome='João').first()
            self.assertIsNotNone(pessoa)  # A pessoa deve existir no banco
            self.assertEqual(pessoa.nome, 'João')  # Verifica o nome
            self.assertEqual(pessoa.data_nascimento, data_nascimento)  # Verifica a data de nascimento
            self.assertEqual(pessoa.email, 'joao@example.com')  # Verifica o email

    def test_listar_pessoas(self):
        """Teste para listar as pessoas"""
        # Cria uma nova pessoa
        with app.app_context():
            nova_pessoa = Pessoa(nome='João', data_nascimento=date(1993, 4, 15), email='joao@example.com')
            db.session.add(nova_pessoa)
            db.session.commit()

        # Faz uma requisição GET para listar as pessoas
        response = self.app.get('/pessoas')
        
        # Verifica se a resposta contém o nome da pessoa criada
        self.assertEqual(response.status_code, 200)  # Espera um código de status 200 (OK)
        self.assertIn('João', response.data.decode('utf-8'))  # Verifica se 'João' está na resposta

    def test_excluir_pessoa(self):
        """Teste para excluir uma pessoa"""
        # Cria uma nova pessoa
        with app.app_context():
            nova_pessoa = Pessoa(nome='João', data_nascimento=date(1993, 4, 15), email='joao@example.com')
            db.session.add(nova_pessoa)
            db.session.commit()
            pessoa_id = nova_pessoa.id  # Obtém o ID da pessoa criada

        # Faz uma requisição para excluir a pessoa
        response = self.app.get(f'/excluir/{pessoa_id}')

        # Verifica se a pessoa foi excluída
        with app.app_context():
            pessoa_excluida = Pessoa.query.get(pessoa_id)
            self.assertIsNone(pessoa_excluida)  # A pessoa deve ser removida do banco de dados

        # Verifica se o redirecionamento ocorreu corretamente (status 302)
        self.assertEqual(response.status_code, 302)

    def test_editar_pessoa(self):
        """Teste para editar os dados de uma pessoa"""
        # Cria uma nova pessoa
        with app.app_context():
            nova_pessoa = Pessoa(nome='João', data_nascimento=date(1993, 4, 15), email='joao@example.com')
            db.session.add(nova_pessoa)
            db.session.commit()
            pessoa_id = nova_pessoa.id  # Obtém o ID da pessoa criada

        # Dados atualizados
        dados_atualizados = dict(nome='João Silva', data_nascimento=date(1992, 8, 30), email='joaosilva@example.com')

        # Faz uma requisição POST para atualizar os dados da pessoa
        response = self.app.post(f'/pessoa/{pessoa_id}', data=dados_atualizados)

        # Verifica se a pessoa foi atualizada no banco de dados
        with app.app_context():
            pessoa_atualizada = Pessoa.query.get(pessoa_id)
            self.assertIsNotNone(pessoa_atualizada)  # A pessoa deve existir no banco
            self.assertEqual(pessoa_atualizada.nome, 'João Silva')  # Verifica o nome atualizado
            self.assertEqual(pessoa_atualizada.data_nascimento, date(1992, 8, 30))  # Verifica a data de nascimento atualizada
            self.assertEqual(pessoa_atualizada.email, 'joaosilva@example.com')  # Verifica o email atualizado

        # Verifica se o redirecionamento ocorreu corretamente (status 302)
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
