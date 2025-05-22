from flask import request, jsonify
from bson.objectid import ObjectId
from app import app, db
from flask_cors import cross_origin
import qrcode, base64, bcrypt
from io import BytesIO
from datetime import datetime, timedelta, timezone


@app.route('/livros', methods=['GET'])
def listar_livros():
    livros = list(db.livros.find())
    for l in livros:
        l['_id'] = str(l['_id'])
    return jsonify(livros)


@app.route('/livros/<string:livro_id>', methods=['GET'])
def buscar_livro(livro_id):
    livro = db.livros.find_one({'_id': ObjectId(livro_id)})
    if not livro:
        return jsonify(mensagem='Livro não encontrado'), 404
    livro['_id'] = str(livro['_id'])
    return jsonify(livro)


@app.route('/livros', methods=['POST'])
@cross_origin(origins='http://localhost:8080', supports_credentials=True)
def criar_livro():
    data = request.json or {}
    if not all(k in data for k in ('titulo', 'autor', 'ano', 'quantidade')):
        return jsonify(mensagem='Campos obrigatórios faltando'), 400
    try:
        data['quantidade'] = int(data['quantidade'])
        if data['quantidade'] < 0:
            raise ValueError
    except ValueError:
        return jsonify(mensagem='Quantidade deve ser inteiro ≥ 0'), 400
    db.livros.insert_one(data)
    return jsonify(mensagem='Livro criado com sucesso'), 201


@app.route('/livros/<string:livro_id>', methods=['PUT'])
@cross_origin(origins='http://localhost:8080', supports_credentials=True)
def atualizar_livro(livro_id):
    data = request.json or {}
    data.pop('_id', None)
    if 'quantidade' in data:
        try:
            data['quantidade'] = int(data['quantidade'])
            if data['quantidade'] < 0:
                raise ValueError
        except ValueError:
            return jsonify(mensagem='Quantidade inválida'), 400
    res = db.livros.update_one({'_id': ObjectId(livro_id)}, {'$set': data})
    if res.matched_count:
        return jsonify(mensagem='Livro atualizado')
    return jsonify(mensagem='Livro não encontrado'), 404


@app.route('/livros/<string:livro_id>', methods=['DELETE'])
@cross_origin(origins='http://localhost:8080', supports_credentials=True)
def deletar_livro(livro_id):
    res = db.livros.delete_one({'_id': ObjectId(livro_id)})
    if res.deleted_count:
        return jsonify(mensagem='Livro removido')
    return jsonify(mensagem='Livro não encontrado'), 404


# =============== USUÁRIOS ===============
@app.route('/usuarios', methods=['POST', 'OPTIONS'])
@cross_origin(origins='http://localhost:8080', supports_credentials=True)
def criar_usuario():
    data = request.json or {}
    if not all(k in data for k in ('nome', 'email', 'senha', 'tipo')):
        return jsonify(mensagem='Dados incompletos'), 400

    senha_hash = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
    status = 'pendente'
    if data['tipo'] == 'bibliotecario':
        status = 'pendente_bibliotecario'

    db.usuarios.insert_one({
        'nome': data['nome'],
        'email': data['email'],
        'senha': senha_hash,
        'tipo': data['tipo'],
        'status': status
    })
    return jsonify(mensagem='Usuário cadastrado com sucesso'), 201


@app.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(origins='http://localhost:8080', supports_credentials=True)
def login():
    data = request.json or {}
    if not all(k in data for k in ('email', 'senha')):
        return jsonify(mensagem='Dados incompletos'), 400

    usuario = db.usuarios.find_one({'email': data['email']})
    if not usuario or not bcrypt.checkpw(data['senha'].encode('utf-8'), usuario['senha']):
        return jsonify(mensagem='Usuário ou senha inválidos'), 401

    if usuario['status'] == 'rejeitado':
        return jsonify(mensagem='Usuário rejeitado'), 403
    if usuario['status'] != 'aprovado':
        return jsonify(mensagem='Usuário ainda não aprovado'), 403

    usuario['_id'] = str(usuario['_id'])
    usuario.pop('senha', None)
    return jsonify(usuario=usuario)


@app.route('/usuarios/pendentes', methods=['GET'])
@cross_origin(origins='http://localhost:8080', supports_credentials=True)
def listar_usuarios_pendentes():
    users = list(db.usuarios.find({'status': {'$in': ['pendente', 'pendente_bibliotecario']}}))
    for u in users:
        u['_id'] = str(u['_id'])
    return jsonify(users)


@app.route('/usuarios/status', methods=['PUT'])
@cross_origin(origins='http://localhost:8080', supports_credentials=True)
def atualizar_status_usuario():
    data = request.json or {}
    if not all(k in data for k in ('id', 'novo_status')):
        return jsonify(mensagem='Dados incompletos'), 400
    res = db.usuarios.update_one({'_id': ObjectId(data['id'])}, {'$set': {'status': data['novo_status']}})
    if res.modified_count:
        return jsonify(mensagem='Status atualizado')
    return jsonify(mensagem='Usuário não encontrado'), 404

@app.route('/reservas', methods=['POST'])
@cross_origin(origins='http://localhost:8080', supports_credentials=True)
def solicitar_reserva():
    data = request.json or {}
    if not all(k in data for k in ('aluno_id', 'livro_id')):
        return jsonify(mensagem='Dados incompletos'), 400

    livro = db.livros.find_one({'_id': ObjectId(data['livro_id'])})
    if not livro:
        return jsonify(mensagem='Livro não encontrado'), 404
    if livro.get('quantidade', 0) <= 0:
        return jsonify(mensagem='Livro sem estoque'), 409

    db.reservas.insert_one({
        'aluno_id': data['aluno_id'],
        'livro_id': data['livro_id'],
        'status': 'pendente'
    })
    return jsonify(mensagem='Reserva solicitada com sucesso'), 201


@app.route('/reservas/aluno_com_livros/<string:aluno_id>', methods=['GET'])
@cross_origin(origins='http://localhost:8080', supports_credentials=True)
def reservas_com_livros(aluno_id):
    pipeline = [
        {'$match': {'aluno_id': aluno_id}},
        {'$addFields': {'livroObjId': {'$toObjectId': '$livro_id'}}},
        {'$lookup': {
            'from': 'livros',
            'localField': 'livroObjId',
            'foreignField': '_id',
            'as': 'livro'
        }},
        {'$unwind': '$livro'}
    ]
    res = list(db.reservas.aggregate(pipeline))
    for r in res:
        r['_id'] = str(r['_id'])
        r['livro']['_id'] = str(r['livro']['_id'])
    return jsonify(res)


@app.route('/reservas/pendentes', methods=['GET'])
@cross_origin(origins='http://localhost:8080', supports_credentials=True)
def listar_reservas_pendentes():
    pipeline = [
        {"$match": {"status": "pendente"}},
        {"$addFields": {"alunoObjId": {"$toObjectId": "$aluno_id"}}},
        {"$lookup": {
            "from": "usuarios",
            "localField": "alunoObjId",
            "foreignField": "_id",
            "as": "aluno"
        }},
        {"$unwind": "$aluno"},
        {"$project": {
            "_id": 1,
            "livro_id": 1,
            "aluno_id": 1,
            "status": 1,
            "aluno_nome": "$aluno.nome"
        }}
    ]
    reservas = list(db.reservas.aggregate(pipeline))
    for r in reservas:
        r['_id'] = str(r['_id'])
        r['livro_id'] = str(r['livro_id'])
        r['aluno_id'] = str(r['aluno_id'])
    return jsonify(reservas)


@app.route('/reservas/aprovar', methods=['PUT'])
@cross_origin(origins='http://localhost:8080', supports_credentials=True)
def aprovar_reserva():
    data = request.json or {}
    if 'reserva_id' not in data:
        return jsonify(mensagem='Dados incompletos'), 400

    reserva = db.reservas.find_one({'_id': ObjectId(data['reserva_id'])})
    if not reserva:
        return jsonify(mensagem='Reserva não encontrada'), 404
    if reserva['status'] == 'aprovado':
        return jsonify(mensagem='Reserva já aprovada'), 409

    livro = db.livros.find_one({'_id': ObjectId(reserva['livro_id'])})
    if not livro or livro.get('quantidade', 0) <= 0:
        return jsonify(mensagem='Livro sem estoque'), 409

    payload = f"Res:{reserva['_id']}|Book:{livro['_id']}"
    qr = qrcode.make(payload)
    buf = BytesIO()
    qr.save(buf, format='PNG')
    qr_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    data_limite = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    db.reservas.update_one({'_id': reserva['_id']}, {
        '$set': {'status': 'aprovado', 'qr_code': qr_b64, 'data_limite': data_limite}
    })
    db.livros.update_one({'_id': livro['_id']}, {'$inc': {'quantidade': -1}})
    return jsonify(mensagem='Reserva aprovada', qr_code=qr_b64)


@app.route('/reservas/devolver', methods=['PUT'])
@cross_origin(origins='http://localhost:8080', supports_credentials=True)
def devolver_reserva():
    data = request.json or {}
    if 'reserva_id' not in data:
        return jsonify(mensagem='Dados incompletos'), 400

    reserva = db.reservas.find_one({'_id': ObjectId(data['reserva_id'])})
    if not reserva or reserva['status'] != 'aprovado':
        return jsonify(mensagem='Reserva inválida'), 404

    db.reservas.update_one(
        {'_id': reserva['_id']},
        {'$set': {'status': 'devolvido', 'data_devolucao': datetime.utcnow()}}
    )
    db.livros.update_one(
        {'_id': ObjectId(reserva['livro_id'])},
        {'$inc': {'quantidade': 1}}
    )
    return jsonify(mensagem='Livro devolvido')
