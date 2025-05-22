# Biblioteca Online

Sistema completo de gerenciamento de uma biblioteca, com funcionalidades para cadastro de livros, controle de reservas, autenticação de usuários e dashboards informativos. O projeto é composto por um backend em Flask (Python) e um frontend em Vue.js, integrando com MongoDB como banco de dados.


## Funcionalidades

- Cadastro e autenticação de usuários (`aluno` e `bibliotecario`)
- Aprovação de usuários pendentes
- Cadastro, edição e remoção de livros
- Sistema de reservas com aprovação e geração de QR Code
- Devolução de livros com atualização automática do estoque
- Dashboard com métricas (livros por status e por gênero)
- Visual refinado com tema escuro e estilo japonês

##  Instruções para execução

### Requisitos

- Python 3.10+
- Node.js 18+
- MongoDB Atlas (ou local)

### Backend (Flask)

cd crud_backend
python -m venv venv
venv\Scripts\activate   # ou source venv/bin/activate no Linux/Mac
pip install -r requirements.txt
# Configure o arquivo .env com sua URI do MongoDB Atlas
flask run


### Frontend (Vue.js)

cd crud_frontend
npm install
npm run dev

### Acesso de Teste

Use os logins abaixo para acessar como cada tipo de usuário:
### Bibliotecário

    Email: admin@admin.com

    Senha: 123456

### Aluno

    Email: aluno@teste.com

    Senha: 123456

    Observação: contas novas requerem aprovação do bibliotecário antes de acesso total ao sistema.

### Segurança

    As senhas são armazenadas com hash utilizando bcrypt.

    Apenas usuários aprovados podem acessar o sistema.

    O cadastro de bibliotecários exige aprovação manual pelo administrador.

### Tecnologias

    Frontend: Vue.js, Bootstrap, CSS personalizado

    Backend: Flask, Flask-CORS, PyMongo, bcrypt

    Banco de dados: MongoDB Atlas

    Extras: QR Code, autenticação, controle de sessão via localStorage