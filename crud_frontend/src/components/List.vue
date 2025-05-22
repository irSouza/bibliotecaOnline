<template>
  <div class="list-container">
    <header class="list-header">
      <span class="kanji-icon">書</span>
      <h2 class="titulo-header">Acervo de Livros</h2>
    </header>

    <div class="toolbar">
      <input v-model="searchTerm" @input="currentPage=1" type="text" placeholder="Buscar por título ou autor" class="input-search" />
      <router-link v-if="usuario.tipo==='bibliotecario'" :to="{name:'create'}" class="btn button-custom">＋ Cadastrar Novo</router-link>
    </div>

    <div class="table-card">
      <table class="book-table">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col.key" @click="sortBy(col.key)" class="sortable" :class="{asc:sortKey===col.key&&sortAsc, desc:sortKey===col.key&&!sortAsc}">
              {{ col.label }}
            </th>
            <th v-if="hasActions">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="livro in paginatedLivros" :key="livro._id" class="clickable-row" @click="goToDetalhes(livro._id)">
            <td>{{ livro.titulo }}</td>
            <td>{{ livro.autor }}</td>
            <td>{{ livro.ano }}</td>
            <td>{{ livro.quantidade }}</td>
            <td>{{ livro.status }}</td>
            <td v-if="hasActions" class="actions">
              <router-link :to="{ name:'update', params:{ id: livro._id }}" class="btn-action edit" @click.stop>Editar</router-link>
              <button class="btn-action delete" @click.stop="promptDelete(livro)">Excluir</button>
            </td>
          </tr>
          <tr v-if="filteredLivros.length===0">
            <td :colspan="columns.length + (hasActions ? 1 : 0)" class="empty-state">Nenhum livro encontrado.</td>
          </tr>
        </tbody>
      </table>

      <div v-if="pageCount>1" class="pagination">
        <button class="pg-btn" :disabled="currentPage===1" @click="currentPage--">&lt;</button>
        <span>Página {{ currentPage }} de {{ pageCount }}</span>
        <button class="pg-btn" :disabled="currentPage===pageCount" @click="currentPage++">&gt;</button>
      </div>
    </div>

    <div v-if="showConfirm" class="modal-overlay" @click.self="showConfirm=false">
      <div class="modal-content">
        <p>Deseja excluir o livro '<strong>{{ toDelete.titulo }}</strong>'?</p>
        <div class="modal-actions">
          <button class="btn button-custom" @click="confirmDelete">Sim</button>
          <button class="btn btn-secondary" @click="showConfirm=false">Não</button>
        </div>
      </div>
    </div>

    <div class="back-container">
      <router-link :to="{name:'home'}" class="btn button-custom">戻 Voltar ao Menu</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'List',
  data () {
    const usuarioStorage = localStorage.getItem('usuario')
    return {
      usuario: usuarioStorage ? JSON.parse(usuarioStorage) : {},
      livros: [],
      searchTerm: '',
      sortKey: '',
      sortAsc: true,
      currentPage: 1,
      pageSize: 10,
      showConfirm: false,
      toDelete: null,
      columns: [
        { key: 'titulo', label: 'Título' },
        { key: 'autor', label: 'Autor' },
        { key: 'ano', label: 'Ano' },
        { key: 'quantidade', label: 'Qtd.' },
        { key: 'status', label: 'Status' }
      ]
    }
  },
  computed: {
    filteredLivros () {
      const t = this.searchTerm.toLowerCase()
      return this.livros.filter(l => l.titulo.toLowerCase().includes(t) || l.autor.toLowerCase().includes(t))
    },
    sortedLivros () {
      if (!this.sortKey) return this.filteredLivros
      return [...this.filteredLivros].sort((a, b) => {
        const A = a[this.sortKey] || ''
        const B = b[this.sortKey] || ''
        if (A < B) return this.sortAsc ? -1 : 1
        if (A > B) return this.sortAsc ? 1 : -1
        return 0
      })
    },
    pageCount () { return Math.ceil(this.sortedLivros.length / this.pageSize) },
    paginatedLivros () { const s = (this.currentPage - 1) * this.pageSize; return this.sortedLivros.slice(s, s + this.pageSize) },
    hasActions () { return this.usuario.tipo === 'bibliotecario' }
  },
  watch: {
    searchTerm () { this.currentPage = 1 }
  },
  methods: {
    fetchLivros () {
      this.$http.get('http://localhost:5000/livros').then(res => { this.livros = res.body }).catch(() => alert('Erro ao carregar livros'))
    },
    sortBy (k) { if (this.sortKey === k) this.sortAsc = !this.sortAsc; else { this.sortKey = k; this.sortAsc = true } },
    goToDetalhes (id) { this.$router.push({ name: 'livro', params: { id } }) },
    promptDelete (l) { this.toDelete = l; this.showConfirm = true },
    confirmDelete () {
      this.$http.delete(`http://localhost:5000/livros/${this.toDelete._id}`).then(() => { this.fetchLivros(); this.showConfirm = false }).catch(() => alert('Erro ao excluir'))
    }
  },
  created () { this.fetchLivros() }
}
</script>

<style scoped>
.list-container{background:var(--color-bg);color:var(--color-secondary);min-height:100vh;padding:2rem 1rem;}
.list-header{text-align:center;margin-bottom:1rem;}
.kanji-icon{font-size:2.5rem;color:var(--color-primary);display:block;margin:0 auto;}
.titulo-header{font-size:1.75rem;margin:0.5rem 0;}
.toolbar{max-width:900px;margin:0 auto 1rem;display:flex;justify-content:space-between;align-items:center;}
.input-search{flex:1;max-width:400px;padding:0.5rem;border-radius:6px;border:1px solid #444;background:#2a2a2a;color:#f4f4f4;}
.btn{text-decoration:none;}
.button-custom{background:var(--color-primary);color:#fff;padding:0.5rem 1rem;border-radius:8px;border:none;cursor:pointer;transition:background 0.2s ease;}
.button-custom:hover{background:#b33636;}
.table-card{background:#1f1f1f;border-radius:8px;padding:1rem;overflow-x:auto;max-width:900px;margin:0 auto;}
.book-table{width:100%;border-collapse:collapse;}
.book-table th,.book-table td{padding:0.75rem;text-align:left;border-bottom:1px solid #333;}
.book-table th.sortable{cursor:pointer;}
.book-table th.sortable.asc::after{content:'↑';float:right;}
.book-table th.sortable.desc::after{content:'↓';float:right;}
.clickable-row:hover{background:rgba(230,57,70,0.2);}
.actions{display:flex;gap:0.5rem;}
.btn-action.edit{background:transparent;color:var(--color-primary);border:1px solid var(--color-primary);padding:0.25rem 0.5rem;border-radius:6px;}
.btn-action.delete{background:var(--color-danger);color:#fff;border:1px solid var(--color-danger);padding:0.25rem 0.5rem;border-radius:6px;}
.empty-state{text-align:center;padding:1rem;}
.pagination{display:flex;align-items:center;justify-content:center;gap:1rem;margin-top:1rem;max-width:900px;margin:1rem auto 0;}
.pg-btn{background:var(--color-primary);color:#fff;border:none;padding:0.5rem;border-radius:4px;}
.pg-btn:disabled{opacity:0.5;cursor:default;}
.modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;z-index:1000;}
.modal-content{background:#1f1f1f;padding:1.5rem;border-radius:8px;color:#f4f4f4;text-align:center;width:90%;max-width:400px;}
.modal-actions{display:flex;justify-content:center;gap:1rem;margin-top:1rem;}
.back-container{text-align:center;margin:1.5rem 0;}
</style>
