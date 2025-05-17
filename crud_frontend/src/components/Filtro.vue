<template>
  <div class="filter-container">
    <!-- Cabeçalho -->
    <div class="title-row">
      <span class="kanji-icon-large">探</span>
      <h2 class="titulo-header">Filtro de Livros</h2>
    </div>

    <!-- Card de filtros -->
    <div class="filter-card">
      <form @submit.prevent="handleSearch" class="filters-grid">
        <div class="filter-field">
          <label class="filter-label"><span class="kanji-icon-small">書</span> Título</label>
          <input
            v-model="filtros.titulo"
            type="text"
            placeholder="Título"
            class="form-control input-dark"
          />
        </div>
        <div class="filter-field">
          <label class="filter-label"><span class="kanji-icon-small">人</span> Autor</label>
          <input
            v-model="filtros.autor"
            type="text"
            placeholder="Autor"
            class="form-control input-dark"
          />
        </div>
        <div class="filter-field">
          <label class="filter-label"><span class="kanji-icon-small">類</span> Gênero</label>
          <input
            v-model="filtros.genero"
            type="text"
            placeholder="Gênero"
            class="form-control input-dark"
          />
        </div>
        <div class="filter-field">
          <label class="filter-label"><span class="kanji-icon-small">状</span> Status</label>
          <select v-model="filtros.status" class="form-select input-dark">
            <option value="">Todos</option>
            <option value="Disponível">Disponível</option>
            <option value="Emprestado">Emprestado</option>
          </select>
        </div>

        <!-- Botões de ação, lado a lado -->
        <div class="grid-actions">
          <button type="submit" class="btn action-button">検 Pesquisar</button>
          <button type="button" class="btn cancel-button" @click="limparFiltros">清 Limpar</button>
        </div>
      </form>
    </div>

    <!-- Resultados -->
    <div v-if="hasSearched">
      <div v-if="isLoading" class="loading-state">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Carregando...</span>
        </div>
      </div>
      <div v-else class="result-count">{{ sortedLivros.length }} resultado(s)</div>
      <div class="table-wrapper">
        <table class="table table-hover table-dark">
          <thead>
            <tr>
              <th @click="sortBy('titulo')" class="sortable">Título</th>
              <th @click="sortBy('autor')" class="sortable">Autor</th>
              <th @click="sortBy('quantidade')" class="sortable">Qtd.</th>
              <th @click="sortBy('status')" class="sortable">Status</th>
              <th @click="sortBy('genero')" class="sortable">Gênero</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="livro in sortedLivros"
              :key="livro._id"
              @click="irParaLivro(livro._id)"
              class="clickable-row"
            >
              <td>{{ livro.titulo }}</td>
              <td>{{ livro.autor }}</td>
              <td>{{ livro.quantidade }}</td>
              <td>{{ livro.status }}</td>
              <td>{{ livro.genero }}</td>
            </tr>
            <tr v-if="sortedLivros.length === 0">
              <td colspan="5" class="text-center text-muted">Nenhum livro encontrado.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Voltar ao menu -->
    <div class="back-link">
      <router-link :to="{ name: 'home' }" class="btn action-button">戻 Voltar ao Menu</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Filtro',
  data () {
    return {
      livros: [],
      filtros: { titulo: '', autor: '', genero: '', status: '' },
      isLoading: false,
      hasSearched: false,
      sortKey: '',
      sortAsc: true
    }
  },
  computed: {
    livrosFiltrados () {
      return this.livros.filter(livro => {
        const t = livro.titulo.toLowerCase().includes(this.filtros.titulo.toLowerCase())
        const a = livro.autor.toLowerCase().includes(this.filtros.autor.toLowerCase())
        const g = livro.genero.toLowerCase().includes(this.filtros.genero.toLowerCase())
        const s = this.filtros.status ? livro.status === this.filtros.status : true
        return t && a && g && s
      })
    },
    sortedLivros () {
      if (!this.sortKey) return this.livrosFiltrados
      return [...this.livrosFiltrados].sort((a, b) => {
        const valA = a[this.sortKey] || ''
        const valB = b[this.sortKey] || ''
        if (valA < valB) return this.sortAsc ? -1 : 1
        if (valA > valB) return this.sortAsc ? 1 : -1
        return 0
      })
    }
  },
  methods: {
    handleSearch () { this.hasSearched = true },
    limparFiltros () { this.filtros = { titulo: '', autor: '', genero: '', status: '' }; this.hasSearched = false },
    irParaLivro (id) { this.$router.push({ name: 'livro', params: { id } }) },
    sortBy (key) {
      if (this.sortKey === key) this.sortAsc = !this.sortAsc
      else { this.sortKey = key; this.sortAsc = true }
    }
  },
  created () {
    this.$http.get('http://localhost:5000/livros')
      .then(res => { this.livros = res.body })
      .catch(() => { alert('Erro ao carregar livros.') })
  }
}
</script>

<style scoped>
.filter-container {
  padding: 80px 1rem 1rem;
  max-width: 900px;
  margin: 0 auto;
}

.title-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.kanji-icon-large {
  font-size: 2.5rem;
  color: var(--color-primary);
}

.titulo-header {
  font-family: var(--font-heading);
  font-size: 1.75rem;
  color: #f4f4f4;
}

.filter-card {
  background-color: #1f1f1f;
  border-radius: 8px;
  padding: 1rem;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

@media (max-width: 768px) {
  .filters-grid { grid-template-columns: repeat(2, 1fr) }
}

.filter-field {
  display: flex;
  flex-direction: column;
}

.filter-label {
  font-weight: 500;
  color: #f4f4f4;
  margin-bottom: 0.5rem;
}

.input-dark,
.form-select.input-dark {
  background-color: #2a2a2a;
  color: #f4f4f4;
  border: 1px solid #444;
}

.input-dark::placeholder,
.form-select.input-dark::placeholder {
  color: var(--color-secondary);
}

.input-dark:focus,
.form-select.input-dark:focus {
  border-color: var(--color-primary);
  box-shadow: none;
}

.grid-actions {
  grid-column: 1 / -1;
  display: flex;
  gap: 1rem;
  justify-content: flex-start;
  margin-top: 0.5rem;
}

.grid-actions button {
  min-width: 160px;
}

.action-button,
.cancel-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
}

.action-button {
  background-color: var(--color-primary);
  transition: background-color 0.2s ease;
}
.action-button:hover {
  background-color: #b33636;
}

.cancel-button {
  background-color: var(--color-danger, #c94f4f);
}
.cancel-button:hover {
  background-color: #b33636;
}

.loading-state,
.result-count {
  text-align: center;
  margin: 1rem 0;
  color: var(--color-secondary);
}

.table-wrapper {
  max-height: 400px;
  overflow-y: auto;
}

.table-dark th,
.table-dark td {
  border-color: #333;
  color: #f4f4f4;
}

.sortable {
  cursor: pointer;
  user-select: none;
}
.sortable::after {
  content: ' ⇅';
  font-size: 0.8rem;
  color: var(--color-secondary);
}

.clickable-row:hover {
  background-color: rgba(230, 57, 70, 0.2);
}

.back-link {
  text-align: center;
  margin-top: 1rem;
}

.back-link .action-button {
  padding: 0.5rem 1.5rem;
}
</style>
