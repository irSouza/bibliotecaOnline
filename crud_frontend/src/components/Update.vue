<template>
  <div class="update-container">
    <header class="update-header">
      <span class="kanji-icon">書</span>
      <h2 class="titulo-header">Editar Livro</h2>
    </header>

    <div class="form-card">
      <div v-if="sucesso" class="alert-success">{{ sucesso }}</div>
      <form @submit.prevent="openConfirm" novalidate>
        <!-- Título -->
        <div class="form-group">
          <label for="titulo">Título *</label>
          <input id="titulo" v-model.trim="livro.titulo" @blur="touched.titulo=true" class="input-dark" type="text" required />
          <small v-if="touched.titulo && !livro.titulo" class="form-error">Campo obrigatório.</small>
        </div>

        <!-- Autor -->
        <div class="form-group">
          <label for="autor">Autor *</label>
          <input id="autor" v-model.trim="livro.autor" @blur="touched.autor=true" class="input-dark" type="text" required />
          <small v-if="touched.autor && !livro.autor" class="form-error">Campo obrigatório.</small>
        </div>

        <!-- Ano -->
        <div class="form-group">
          <label for="ano">Ano *</label>
          <input id="ano" v-model.number="livro.ano" @keydown="allowNumberOnly" @blur="touched.ano=true" maxlength="4" class="input-dark" :placeholder="`Insira o ano (1000-${currentYear})`" required />
          <small v-if="touched.ano && (livro.ano<1000 || livro.ano>currentYear)" class="form-error">Ano entre 1000 e {{ currentYear }}.</small>
        </div>

        <!-- Quantidade -->
        <div class="form-group">
          <label for="qtd">Quantidade *</label>
          <input id="qtd" v-model.number="livro.quantidade" @keydown="allowNumberOnly" @blur="touched.quantidade=true" type="number" min="0" class="input-dark" />
          <small v-if="touched.quantidade && (livro.quantidade===null || livro.quantidade<0)" class="form-error">Informe um número ≥ 0.</small>
        </div>

        <!-- Gênero -->
        <div class="form-group">
          <label for="genero">Gênero</label>
          <input id="genero" v-model.trim="livro.genero" class="input-dark" type="text" />
        </div>

        <!-- Status -->
        <div class="form-group">
          <label for="status">Status</label>
          <select id="status" v-model="livro.status" class="input-dark">
            <option disabled value="">Selecione</option>
            <option>Disponível</option>
            <option>Emprestado</option>
          </select>
        </div>

        <!-- Páginas -->
        <div class="form-group">
          <label for="paginas">Páginas *</label>
          <input id="paginas" v-model.number="livro.numero_paginas" @keydown="allowNumberOnly" @blur="touched.paginas=true" type="number" min="1" class="input-dark" />
          <small v-if="touched.paginas && (livro.numero_paginas===null || livro.numero_paginas<1)" class="form-error">Deve ser maior que zero.</small>
        </div>

        <!-- Edição -->
        <div class="form-group">
          <label for="edicao">Edição</label>
          <select id="edicao" v-model.number="livro.edicao" class="input-dark">
            <option :value="null">Selecione</option>
            <option v-for="n in 10" :key="n" :value="n">{{ n }}ª Edição</option>
          </select>
        </div>

        <!-- ISBN -->
        <div class="form-group">
          <label for="isbn">ISBN</label>
          <input id="isbn" v-model="livro.isbn" @input="formatarIsbn" @keydown="allowNumberOnly" @blur="touched.isbn=true" maxlength="13" class="input-dark" placeholder="Somente 10 ou 13 dígitos" />
          <small v-if="touched.isbn && livro.isbn && (livro.isbn.length!==10 && livro.isbn.length!==13)" class="form-error">ISBN deve ter 10 ou 13 dígitos.</small>
        </div>

        <!-- Descrição -->
        <div class="form-group">
          <label for="descricao">Descrição</label>
          <textarea id="descricao" v-model.trim="livro.descricao" rows="4" class="input-dark"></textarea>
        </div>

        <!-- Capa URL -->
        <div class="form-group">
          <label for="capa">URL da Capa</label>
          <input id="capa" v-model="livro.imagem_url" @blur="coverPreview = livro.imagem_url" type="url" placeholder="https://..." class="input-dark" />
          <img v-if="coverPreview" :src="coverPreview" alt="Capa" class="cover-preview" />
        </div>

        <!-- Ações -->
        <div class="form-actions">
          <button type="submit" class="button-custom" :disabled="!formValid">Salvar Alterações</button>
          <router-link :to="{ name: 'home' }" class="btn-secondary">Cancelar</router-link>
        </div>
      </form>
    </div>

    <div class="back-container">
      <router-link :to="{ name: 'home' }" class="button-custom">戻 Voltar ao Menu</router-link>
    </div>

    <!-- Modal de confirmação -->
    <div v-if="showConfirm" class="modal-overlay" @click.self="showConfirm=false">
      <div class="modal-content">
        <p>Confirmar salvar alterações?</p>
        <div class="modal-actions">
          <button class="button-custom" @click="atualizarLivro">Sim</button>
          <button class="btn-secondary" @click="showConfirm=false">Não</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Update',
  data () {
    return {
      livro: {},
      sucesso: '',
      coverPreview: null,
      showConfirm: false,
      touched: { titulo: false, autor: false, ano: false, quantidade: false, paginas: false, isbn: false }
    }
  },
  computed: {
    currentYear () { return new Date().getFullYear() },
    formValid () {
      const i = this.livro
      const y = this.currentYear
      return i.titulo && i.autor && i.ano >= 1000 && i.ano <= y && i.quantidade !== null && i.quantidade >= 0 && i.numero_paginas && i.numero_paginas >= 1 && (!i.isbn || i.isbn.length === 10 || i.isbn.length === 13)
    }
  },
  created () {
    const id = this.$route.params.id
    this.$http.get(`http://localhost:5000/livros/${id}`)
      .then(res => { this.livro = res.body; this.coverPreview = this.livro.imagem_url })
      .catch(() => { alert('Erro ao carregar dados.'); this.$router.push({ name: 'list' }) })
  },
  methods: {
    allowNumberOnly (e) { if (!/[0-9]/.test(e.key) && !['Backspace', 'ArrowLeft', 'ArrowRight', 'Delete', 'Tab'].includes(e.key)) e.preventDefault() },
    formatarIsbn () { this.livro.isbn = this.livro.isbn.replace(/\D/g, '') },
    openConfirm () { if (this.formValid) { this.showConfirm = true } },
    atualizarLivro () {
      this.showConfirm = false
      this.$http.put('http://localhost:5000/livros', this.livro)
        .then(res => { this.sucesso = res.body.mensagem; setTimeout(() => this.$router.push({ name: 'list' }), 1500) })
        .catch(() => alert('Erro ao atualizar livro.'))
    }
  }
}
</script>

<style scoped>
.update-container{background:var(--color-bg);color:var(--color-secondary);min-height:100vh;padding:2rem 1rem;max-width:600px;margin:0 auto}
.update-header{text-align:center;margin-bottom:1rem}
.kanji-icon{font-size:2.5rem;color:var(--color-primary);display:block;margin:0 auto}
.titulo-header{font-size:1.75rem;margin-top:.5rem}
.form-card{background:#1f1f1f;padding:2rem;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,.5)}
.alert-success{background:#2f522f;color:#d4edda;padding:.75rem;border-radius:4px;margin-bottom:1rem;text-align:center}
.form-group{margin-bottom:1rem;display:flex;flex-direction:column}
label{margin-bottom:.5rem;font-weight:500}
.input-dark{padding:.5rem;border:1px solid #444;border-radius:4px;background:#2a2a2a;color:#f4f4f4}
.input-dark::placeholder{color:var(--color-secondary)}
.input-dark:focus{outline:none;border-color:var(--color-primary);box-shadow:0 0 4px rgba(201,79,79,.5)}
.form-error{color:#e74c3c;font-size:.85rem;margin-top:.25rem}
.cover-preview{display:block;margin-top:1rem;max-width:100%;border-radius:4px}
.form-actions{display:flex;gap:1rem;justify-content:flex-end;margin-top:1.5rem}
.button-custom{background:var(--color-primary);color:#fff;padding:.5rem 1rem;border:none;border-radius:6px;cursor:pointer;transition:background .2s}
.button-custom:hover{background:#b33636}
.btn-secondary{background:#6c757d;color:#fff;padding:.5rem 1rem;border:none;border-radius:6px;cursor:pointer;transition:background .2s}
.btn-secondary:hover{background:#5a6266}
.back-container{text-align:center;margin:2rem 0 0}
/* modal */
.modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center;z-index:1000}
.modal-content{background:#1f1f1f;padding:1.5rem;border-radius:8px;color:#f4f4f4;text-align:center;width:90%;max-width:400px}
.modal-actions{display:flex;justify-content:center;gap:1rem;margin-top:1rem}
</style>
