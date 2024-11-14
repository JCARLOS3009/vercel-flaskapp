# Aplicação Flask com PostgreSQL

Este é um exemplo de aplicação Flask conectada a um banco de dados PostgreSQL. O aplicativo permite realizar operações CRUD (Criar, Ler, Atualizar, Excluir) para uma tabela simples de pessoas, armazenando nome, idade e e-mail.

## Componentização no Frontend:
Templates Jinja2: O uso de templates Jinja2 (render_template('index.html'), render_template('cadastrar.html'), etc.) contribui para a componentização do frontend. Isso permite que você tenha diferentes partes da aplicação divididas em componentes reutilizáveis, como:

Um template para cadastrar pessoas (cadastrar.html).
Um template para editar pessoas (editar.html).
Um template para listar pessoas (index.html).

## Extensibilidade:
Rotas e Funcionalidades Fáceis de Expandir: A estrutura de rotas que você tem (/pessoas, /criar, /excluir/<int:id>, /pessoa/<int:id>) é bem modular, permitindo adicionar mais funcionalidades sem dificuldade. Por exemplo, se você precisar adicionar um recurso de pesquisa de pessoas, você pode facilmente criar uma nova rota /pesquisar e adaptar o código para suportar filtros.

Banco de Dados e Modelos: O uso do SQLAlchemy e a definição do modelo Pessoa também contribuem para a extensibilidade, pois você pode adicionar novas colunas e relacionamentos à medida que o sistema cresce (por exemplo, relacionamentos entre pessoa e endereço, pessoa e telefone, etc.).

## Requisitos

- **Python 3.x**: Verifique se o Python está instalado no seu sistema.
- **PostgreSQL**: Banco de dados utilizado para armazenar os dados.
- **Dependências**:
  - Flask
  - Flask-SQLAlchemy
  - psycopg2

## Como rodar localmente

### 1. Instalar o Python
Verifique se o Python está instalado com o comando:

```bash
python --version
```
2. Criar um ambiente virtual (opcional, mas recomendado)
Crie um ambiente virtual para isolar as dependências do projeto:

```bash

# Navegue até a pasta onde está o seu projeto
cd /caminho/para/seu/projeto
```
```bash
# Crie o ambiente virtual
python -m venv venv
```
```bash
# Ative o ambiente virtual:
# Para Windows:
venv\Scripts\activate
```
# Para Linux/Mac:
source venv/bin/activate
```
3. Instalar as dependências
Com o ambiente virtual ativado, instale as dependências necessárias:

```bash
pip install flask flask_sqlalchemy psycopg2
```
Flask: Framework web para construir o aplicativo.
Flask-SQLAlchemy: Extensão Flask para integração com SQLAlchemy.
psycopg2: Adaptador para conectar o Flask com o PostgreSQL.

4. Configurar o Banco de Dados PostgreSQL
Certifique-se de ter o banco de dados PostgreSQL rodando localmente ou use um banco de dados remoto. A URI de conexão está configurada no código. Se você for usar um banco local, siga estas instruções:

Para um banco local:
Instale o PostgreSQL seguindo as instruções no site oficial do PostgreSQL.
Crie um banco de dados:
```bash
psql -U postgres
CREATE DATABASE verceldb;
Para um banco remoto (usando a URI fornecida no código):
```

python
Se for usar um banco local, altere a URI para algo assim:

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:senha@localhost:5432/verceldb'
usuario: Seu nome de usuário do PostgreSQL (geralmente postgres).
senha: Sua senha do PostgreSQL.
localhost: Endereço local do banco de dados (ou um IP/hostname se estiver usando um banco remoto).
verceldb: Nome do banco de dados.
5. Criar as tabelas no banco de dados
O código já possui a função create_tables() que cria as tabelas automaticamente. Para garantir que as tabelas sejam criadas, você pode rodar o seguinte código no Python:

python
from app import db
db.create_all()
6. Rodar o servidor Flask
Com as dependências instaladas e o banco de dados configurado, rode o servidor Flask:

```bash
python app.py
```
Isso iniciará o servidor Flask no endereço http://127.0.0.1:5000.

7. Verificar a aplicação
Abra o navegador e acesse http://127.0.0.1:5000 para ver a aplicação em funcionamento. A página inicial redireciona para a lista de pessoas. Você pode adicionar uma nova pessoa, editar ou excluir registros.