<template>
  <div class="create-container">
    <!-- Cabeçalho -->
    <header class="create-header">
      <span class="kanji-icon">書</span>
      <h2 class="titulo-header">Cadastrar Livro</h2>
    </header>

    <!-- Formulário -->
    <div class="form-card">
      <div v-if="sucesso" class="alert-success">{{ sucesso }}</div>
      <form @submit.prevent="addLivro" class="book-form" novalidate>
        <!-- Título -->
        <div class="form-group">
          <label for="titulo">Título *</label>
          <input id="titulo" v-model.trim="livro.titulo" @blur="touched.titulo = true" type="text" class="input-dark" required />
          <small v-if="touched.titulo && !livro.titulo" class="form-error">Campo obrigatório.</small>
        </div>

        <!-- Autor -->
        <div class="form-group">
          <label for="autor">Autor *</label>
          <input id="autor" v-model.trim="livro.autor" @blur="touched.autor = true" type="text" class="input-dark" required />
          <small v-if="touched.autor && !livro.autor" class="form-error">Campo obrigatório.</small>
        </div>

        <!-- Ano -->
        <div class="form-group">
          <label for="ano">Ano *</label>
          <input id="ano" v-model.number="livro.ano" @blur="touched.ano = true" @keypress="allowNumberOnly" type="text" inputmode="numeric" maxlength="4" class="input-dark" :placeholder="`Insira o ano (1000-${currentYear})`" required />
          <small v-if="touched.ano && (livro.ano < 1000 || livro.ano > currentYear)" class="form-error">Ano entre 1000 e {{ currentYear }}.</small>
        </div>

        <!-- Quantidade -->
        <div class="form-group">
          <label for="qtd">Quantidade *</label>
          <input id="qtd" v-model.number="livro.quantidade" @blur="touched.quantidade = true" @keypress="allowNumberOnly" type="number" min="0" class="input-dark" placeholder="Insira a quantidade de livros" required />
          <small v-if="touched.quantidade && (livro.quantidade === null || livro.quantidade < 0)" class="form-error">Informe um número ≥ 0.</small>
        </div>

        <!-- Gênero -->
        <div class="form-group">
          <label for="genero">Gênero</label>
          <input id="genero" v-model.trim="livro.genero" type="text" class="input-dark" />
        </div>

        <!-- Status -->
        <div class="form-group">
          <label for="status">Status</label>
          <select id="status" v-model="livro.status" class="input-dark">
            <option value="Disponível">Disponível</option>
            <option value="Emprestado">Emprestado</option>
          </select>
        </div>

        <!-- Páginas -->
        <div class="form-group">
          <label for="paginas">Páginas</label>
          <input id="paginas" v-model.number="livro.numero_paginas" @blur="touched.paginas = true" @keypress="allowNumberOnly" type="number" min="1" class="input-dark" placeholder="Quantidade de páginas" />
          <small v-if="touched.paginas && livro.numero_paginas !== null && livro.numero_paginas < 1" class="form-error">Deve ser maior que zero.</small>
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
          <input id="isbn" v-model="livro.isbn" @blur="touched.isbn = true; validateISBN()" @keypress="allowNumberOnly" type="text" inputmode="numeric" maxlength="13" class="input-dark" placeholder="Somente 10 ou 13 dígitos" />
          <small v-if="touched.isbn && isbnError" class="form-error">{{ isbnError }}</small>
        </div>

        <!-- Descrição -->
        <div class="form-group">
          <label for="descricao">Descrição</label>
          <textarea id="descricao" v-model.trim="livro.descricao" rows="4" class="input-dark"></textarea>
        </div>

        <!-- Capa (somente via URL) -->
        <div class="form-group">
          <label for="imagem">URL da Capa</label>
          <input
            id="imagem"
            v-model="livro.imagem_url"
            @blur="coverPreview = livro.imagem_url"
            type="url"
            placeholder="https://exemplo.com/capa.jpg"
            class="input-dark"
          />
          <img v-if="coverPreview" :src="coverPreview" alt="Prévia da capa" class="cover-preview" />
        </div>

        <!-- Ações -->
        <div class="form-actions">
          <button type="submit" class="button-custom" :disabled="!formValid">Cadastrar</button>
          <router-link :to="{ name: 'home' }" class="btn-secondary">Cancelar</router-link>
        </div>
      </form>
    </div>

    <!-- Voltar -->
    <div class="back-container">
      <router-link :to="{ name: 'home' }" class="button-custom">戻 Voltar ao Menu</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Create',
  data () {
    return {
      livro: {
        titulo: '',
        autor: '',
        ano: null,
        quantidade: 1,
        genero: '',
        status: 'Disponível',
        numero_paginas: null,
        edicao: null,
        isbn: '',
        descricao: '',
        imagem_url: ''
      },
      sucesso: '',
      isbnError: '',
      coverPreview: null,
      fileName: '',
      touched: { titulo: false, autor: false, ano: false, quantidade: false, paginas: false, isbn: false }
    }
  },
  computed: {
    currentYear () { return new Date().getFullYear() },
    formValid () {
      return (
        this.livro.titulo &&
        this.livro.autor &&
        this.livro.ano >= 1000 && this.livro.ano <= this.currentYear &&
        this.livro.quantidade >= 0 &&
        (!this.livro.numero_paginas || this.livro.numero_paginas >= 1) &&
        !this.isbnError
      )
    }
  },
  methods: {
    allowNumberOnly (e) {
      if (!/[0-9]/.test(e.key) && !['Backspace', 'ArrowLeft', 'ArrowRight', 'Delete', 'Tab'].includes(e.key)) {
        e.preventDefault()
      }
    },
    validateISBN () {
      const clean = this.livro.isbn.replace(/[-\s]/g, '')
      this.isbnError = clean && !/^(\d{10}|\d{13})$/.test(clean) ? 'ISBN deve ter 10 ou 13 dígitos.' : ''
    },
    handleFileUpload (e) {
      const file = e.target.files[0]
      if (!file) return
      this.fileName = file.name
      const reader = new FileReader()
      reader.onload = ev => {
        this.coverPreview = ev.target.result
        this.livro.imagem_url = ''
      }
      reader.readAsDataURL(file)
    },
    previewCover () {
      // se URL informada, usa‑a; caso contrário mantém preview existente
      if (this.livro.imagem_url) {
        this.coverPreview = this.livro.imagem_url
      }
    },
    addLivro () {
      // marca todos campos como tocados
      Object.keys(this.touched).forEach(k => { this.touched[k] = true })
      this.validateISBN()
      if (!this.formValid) return
      this.$http.post('http://localhost:5000/livros', this.livro)
        .then(res => {
          this.sucesso = res.body.mensagem
          setTimeout(() => this.$router.push({ name: 'list' }), 1500)
        })
        .catch(() => alert('Erro ao cadastrar livro.'))
    }
  }
}
</script>

<style scoped>
/* Layout */
.create-container {
  background: var(--color-bg);
  color: var(--color-secondary);
  min-height: 100vh;
  padding: 2rem 1rem;
  max-width: 600px;
  margin: 0 auto;
}
.create-header { text-align: center; margin-bottom: 1rem; }
.kanji-icon { font-size: 2.5rem; color: var(--color-primary); display: block; margin: 0 auto; }
.titulo-header { font-size: 1.75rem; margin-top: 0.5rem; }

/* Card */
.form-card {
  background: #1f1f1f;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}

/* Alert */
.alert-success {
  background: #2f522f;
  color: #d4edda;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  text-align: center;
}

/* Form */
.form-group { margin-bottom: 1rem; display: flex; flex-direction: column; }
label { margin-bottom: 0.5rem; font-weight: 500; }
.input-dark,
select.input-dark,
textarea.input-dark {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #444;
  border-radius: 4px;
  background: #2a2a2a;
  color: #f4f4f4;
}
.input-dark:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 4px rgba(201,79,79,0.5); }
.form-error { color: #e74c3c; font-size: 0.85rem; margin-top: 0.25rem; }

/* Cover */
.cover-inputs { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; }
.file-label { background: var(--color-secondary); color: #fff; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; }
.file-input { display: none; }
.file-name { display: block; margin-top: 0.5rem; font-size: 0.9rem; color: var(--color-secondary); word-break: break-word; }
.cover-preview { display: block; margin-top: 1rem; max-width: 100%; border-radius: 4px; }

/* Buttons */
.form-actions { display: flex; gap: 1rem; justify-content: flex-end; margin-top: 1.5rem; }
.button-custom { background: var(--color-primary); color: #fff; padding: 0.5rem 1rem; border: none; border-radius: 6px; cursor: pointer; transition: background 0.2s ease; }
.button-custom:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: #6c757d; color: #fff; padding: 0.5rem 1rem; border: none; border-radius: 6px; cursor: pointer; transition: background 0.2s ease; }
.btn-secondary:hover { background: #5a6268; }
.back-container { text-align: center; margin: 2rem 0 0; }
</style>
