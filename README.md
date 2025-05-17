# 📚 Biblioteca Online

Sistema completo de gestão de acervo e reservas para bibliotecas acadêmicas. A aplicação é dividida em **back‑end** (Flask + MongoDB) e **front‑end** (Vue 2), oferecendo cadastro de usuários, CRUD de livros, reservas com QR Code, painel administrativo e dashboard analítico.

---

## ✨ Funcionalidades

| Módulo                      | Descrição                                                                                                                 |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Autenticação**            | Registro / login de **Alunos** e **Bibliotecários** (perfis com permissões diferentes)                                    |
| **CRUD de Livros**          | Inserir, editar, excluir livros com validações; upload de capa via URL; controle de **quantidade em estoque**             |
| **Filtro Avançado**         | Busca por título, autor, gênero e status com ordenação dinâmica                                                           |
| **Reservas & QR Code**      | Aluno solicita reserva; bibliotecário aprova/recusa; QR gerado automaticamente; controle de devolução e ajuste de estoque |
| **Painel Dashboard**        | Métricas em tempo‑real (total, disponíveis, emprestados, livros por gênero) com gráfico de barras                         |
| **Gestão de Usuários**      | Aprovação ou rejeição de cadastros pendentes                                                                              |
| **Dark Theme + Responsive** | Interface consistente em dispositivos desktop e mobile                                                                    |

---

## 🛠️ Tecnologias Principais

| Camada          | Tech                                                                  |
| --------------- | --------------------------------------------------------------------- |
| **Back‑end**    | Python 3 · Flask 2 · PyMongo · MongoDB · python‑qrcode                |
| **Front‑end**   | Vue 2 · Vue Router · Vue Resource · Bootstrap 4 (custom) · Chart.js 2 |
| **Dev & Build** | npm · Webpack · Babel · ESLint · Prettier                             |

---

## 📁 Estrutura de Pastas

```
.
├── crud_backend          # API Flask / MongoDB
│   ├── app/              # pacote da aplicação
│   │   ├── __init__.py   # factory e configs
│   │   └── routes.py     # todas as rotas REST
│   ├── requirements.txt
│   └── .env.example      # variáveis (opcional)
│
├── crud_frontend         # SPA Vue
│   ├── public/
│   ├── src/
│   │   ├── components/   # views & componentes
│   │   └── router/
│   ├── package.json
│   └── vue.config.js
└── README.md             
```

---

## ⚙️ Pré‑requisitos

* **Python 3.10 +**
* **Node 18 +** e **npm 9 +**
* **MongoDB 6 +** (local ou Atlas)

---

## 🚀 Instalação

```bash
# 1. clone o repositório
$ git clone https://github.com/irSouza/bibliotecaOnline.git
$ cd bibliotecaOnline
```

### 1) Back‑end

```bash
cd crud_backend
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# (opcional) copie .env.example → .env e ajuste as variáveis
export FLASK_APP=app
flask run  # http://127.0.0.1:5000
```

### 2) Front‑end

```bash
cd ../crud_frontend
npm install           # instala dependências listadas em package.json
npm run dev           # abre em http://localhost:8080
```

> **Produção:** `npm run build` gera artefatos estáticos em `crud_frontend/dist/`.

---

## 🧪 Scripts Úteis

| Comando        | Descrição                 |
| -------------- | ------------------------- |
| `npm run dev`  | Dev server com hot‑reload |
| `npm run lint` | ESLint + Prettier         |
| `flask run`    | Sobe a API no modo debug  |
| `pytest`       | (caso existam testes)     |

---

## 🗄️ Configuração do Banco

* Base: `biblioteca`
* Coleções: `livros`, `usuarios`, `reservas`
* Scripts de seed estão em `crud_backend/seed/*.py` (opcional)


