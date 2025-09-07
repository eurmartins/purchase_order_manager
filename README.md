# Po-manager-FastApi

Este projeto é uma API RESTful construída com FastAPI, SQLAlchemy e MySQL para gerenciar usuários. Abaixo está a explicação detalhada dos principais arquivos e pastas do projeto (exceto bibliotecas externas):

## Estrutura

```
app/
├── __init__.py
├── api/
│   └── v1/
│       ├── __init__.py
│       └── endpoints/
│           ├── __init__.py
│           └── user.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── security.py
├── crud/
│   ├── __init__.py
│   └── user.py
├── db/
│   ├── __init__.py
│   ├── base.py
│   ├── session.py
├── models/
│   ├── __init__.py
│   └── user.py
├── schemas/
│   ├── __init__.py
│   └── user.py
├── main.py
.env
requirements.txt
```

## Explicação detalhada dos arquivos

### app/main.py
Ponto de entrada da aplicação FastAPI. Inicializa o app, inclui as rotas, importa os modelos e garante que as tabelas do banco de dados sejam criadas automaticamente ao iniciar o projeto.

### app/api/v1/endpoints/user.py
Define as rotas da API para operações CRUD de usuários:
- `POST /` cria um novo usuário
- `GET /{user_id}` retorna um usuário pelo id
- `GET /` retorna todos os usuários
- `PUT /{user_id}` atualiza um usuário pelo id
- `DELETE /{user_id}` remove um usuário pelo id
Utiliza dependências para acesso ao banco e validação dos dados.

### app/crud/user.py
Contém funções de acesso ao banco de dados para usuários:
- `get_user_by_email`: busca usuário pelo email
- `create_user`: cria novo usuário
- `get_user`: busca usuário pelo id
- `get_users`: retorna todos os usuários
- `update_user`: atualiza dados de um usuário
- `delete_user`: remove usuário do banco
Separa a lógica de persistência do restante da aplicação.

### app/models/user.py
Define o modelo User, que representa a tabela `users` no banco de dados. Utiliza SQLAlchemy para mapear os campos:
- `id`: identificador único
- `email`: email do usuário
- `hashed_password`: senha criptografada
- `full_name`: nome completo

### app/schemas/user.py
Define os schemas Pydantic para validação e serialização dos dados de entrada/saída da API:
- `UserBase`: campos básicos do usuário
- `UserCreate`: campos para criação (inclui senha)
- `UserRead`: campos para leitura (inclui id)
A classe interna `Config` com `from_attributes = True` permite conversão de ORM para schema.

### app/core/config.py
Carrega as configurações do projeto a partir do arquivo `.env` usando a biblioteca `python-dotenv`. Centraliza variáveis sensíveis e de ambiente, como credenciais do banco e chave secreta.

### app/core/security.py
Implementa funções para hash e verificação de senha usando `passlib` e `bcrypt`:
- `get_password_hash`: gera hash seguro da senha
- `verify_password`: compara senha digitada com hash salvo
Garante que senhas nunca sejam salvas em texto puro.

### app/db/base.py
Define o objeto `Base` do SQLAlchemy, usado como base para todos os modelos ORM do projeto. Todos os modelos devem herdar de `Base` para serem reconhecidos pelo SQLAlchemy.

### app/db/session.py
Configura a conexão com o banco de dados MySQL usando SQLAlchemy. Cria o `engine` e o `sessionmaker`, que gerenciam as sessões de acesso ao banco.

### app/api/v1/endpoints/__init__.py, app/api/v1/__init__.py, app/api/__init__.py, app/core/__init__.py, app/crud/__init__.py, app/db/__init__.py, app/models/__init__.py, app/schemas/__init__.py
Arquivos de inicialização de pacotes Python. Permitem que as pastas sejam reconhecidas como módulos e facilitam importações organizadas.

### .env
Arquivo de variáveis de ambiente. Guarda credenciais e configurações sensíveis fora do código-fonte, como usuário, senha, host, porta e nome do banco.

### requirements.txt
Lista as dependências do projeto para instalação via pip. Permite que qualquer pessoa instale os pacotes necessários com `pip install -r requirements.txt`.

---

Se quiser explicações sobre outros arquivos, exemplos de uso ou detalhes de funcionamento, só pedir!
