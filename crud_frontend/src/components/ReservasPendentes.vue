<template>
  <div class="pendentes-container">
    <header class="pendentes-header">
      <span class="kanji-icon">予</span>
      <h2 class="titulo-header">Reservas Pendentes</h2>
    </header>

    <div class="table-card">
      <table v-if="reservas.length" class="reserva-table">
        <thead>
          <tr>
            <th>Reserva</th>
            <th>Livro</th>
            <th>Aluno</th>
            <th colspan="2" class="text-center">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in reservas" :key="r._id">
            <td>{{ r._id }}</td>
            <td>{{ r.livroTitulo || r.livro_id }}</td>
            <td>{{ r.alunoNome   || r.aluno_id }}</td>
            <td class="actions">
              <button class="btn-approve" @click="openConfirm(r,'aprovar')">✔ Aprovar</button>
            </td>
            <td class="actions">
              <button class="btn-reject" @click="openConfirm(r,'rejeitar')">✖ Recusar</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">Nenhuma reserva pendente.</div>
    </div>

    <div class="back-container">
      <router-link :to="{ name: 'home' }" class="button-custom">戻 Voltar ao Menu</router-link>
    </div>

    <div v-if="showConfirm" class="modal-overlay" @click.self="showConfirm=false">
      <div class="modal-content">
        <p>
          {{ actionType==='aprovar' ? 'Confirmar aprovação' : 'Confirmar recusa' }} da reserva
          <strong>{{ selected._id }}</strong>?
        </p>
        <div class="modal-actions">
          <button class="button-custom" @click="confirmarAcao">Sim</button>
          <button class="btn-secondary" @click="showConfirm=false">Não</button>
        </div>
      </div>
    </div>

    <div v-if="toast" class="toast-overlay"><div class="toast-content">{{ toast }}</div></div>
  </div>
</template>

<script>
export default {
  name: 'ReservasPendentes',
  data () {
    return {
      reservas: [],
      showConfirm: false,
      selected: {},
      actionType: 'aprovar',
      toast: ''
    }
  },
  created () { this.carregar() },
  methods: {
    carregar () {
      this.$http.get('http://localhost:5000/reservas/pendentes')
        .then(async res => {
          const lista = res.body
          const reqs = lista.map(async r => {
            // busca livro
            try {
              const lv = await this.$http.get(`http://localhost:5000/livros/${r.livro_id}`)
              this.$set(r, 'livroTitulo', lv.body.titulo)
            } catch (e) { this.$set(r, 'livroTitulo', r.livro_id) }
            // busca aluno
            try {
              const al = await this.$http.get(`http://localhost:5000/usuarios/${r.aluno_id}`)
              this.$set(r, 'alunoNome', al.body.nome)
            } catch (e) { this.$set(r, 'alunoNome', r.aluno_id) }
            return r
          })
          this.reservas = await Promise.all(reqs)
        })
        .catch(() => alert('Erro ao carregar reservas.'))
    },
    openConfirm (r, tipo) {
      this.selected = r
      this.actionType = tipo
      this.showConfirm = true
    },
    confirmarAcao () {
      this.showConfirm = false
      const url = this.actionType === 'aprovar'
        ? 'http://localhost:5000/reservas/aprovar'
        : 'http://localhost:5000/reservas/recusar'
      this.$http.put(url, { reserva_id: this.selected._id })
        .then(() => {
          const aluno = this.selected.alunoNome || this.selected.aluno_id
          const msg = this.actionType === 'aprovar'
            ? `Reserva de ${aluno} aprovada!`
            : `Reserva de ${aluno} recusada.`
          this.toastMsg(msg)
          this.carregar()
        })
        .catch(() => alert('Erro ao processar reserva.'))
    },
    toastMsg (msg) {
      this.toast = msg
      setTimeout(() => { this.toast = '' }, 2500)
    }
  }
}
</script>

<style scoped>
.pendentes-container{background:var(--color-bg);color:var(--color-secondary);min-height:100vh;padding:2rem 1rem;max-width:900px;margin:0 auto}
.pendentes-header{text-align:center;margin-bottom:1rem}
.kanji-icon{font-size:2.5rem;color:var(--color-primary);display:block;margin:0 auto}
.titulo-header{font-size:1.75rem;margin-top:.5rem}
.table-card{background:#1f1f1f;padding:1rem;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,.5)}
.reserva-table{width:100%;border-collapse:collapse}
.reserva-table th,.reserva-table td{padding:.75rem;border-bottom:1px solid #333;text-align:left}
.actions{display:flex;justify-content:center}
.btn-approve,.btn-reject{padding:.45rem 1rem;font-size:.85rem;border:none;border-radius:6px;cursor:pointer;min-width:100px;text-align:center;transition:background .2s}
.btn-approve{background:var(--color-primary);color:#fff}
.btn-approve:hover{background:#b33636}
.btn-reject{background:var(--color-danger,#c94f4f);color:#fff}
.btn-reject:hover{background:#b33636}
.empty-state{text-align:center;padding:1rem;color:var(--color-secondary)}
.back-container{text-align:center;margin:1.5rem 0}
.button-custom{background:var(--color-primary);color:#fff;padding:.5rem 1.5rem;border:none;border-radius:8px;cursor:pointer;transition:background .2s}
.button-custom:hover{background:#b33636}
.modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center;z-index:1000}
.modal-content{background:#1f1f1f;padding:1.5rem;border-radius:8px;color:#f4f4f4;text-align:center;width:90%;max-width:400px}
.modal-actions{display:flex;justify-content:center;gap:1rem;margin-top:1rem}
.btn-secondary{background:#6c757d;color:#fff;padding:.4rem 1rem;border:none;border-radius:6px;cursor:pointer}
.toast-overlay{position:fixed;top:1rem;left:50%;transform:translateX(-50%);background:#2f522f;color:#d4edda;padding:.75rem 1.25rem;border-radius:6px;box-shadow:0 4px 10px rgba(0,0,0,.4);z-index:1100}
</style>
