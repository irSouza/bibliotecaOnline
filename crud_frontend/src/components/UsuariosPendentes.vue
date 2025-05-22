<template>
  <div class="pendentes-container">
    <header class="pendentes-header">
      <span class="kanji-icon">学</span>
      <h2 class="titulo-header">Alunos Pendentes</h2>
    </header>

<div class="table-card">
  <table v-if="usuarios.length" class="pend-table">
    <thead>
      <tr>
        <th>Nome</th>
        <th>Email</th>
        <th colspan="2" class="text-center">Ações</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="u in usuarios" :key="u._id">
        <td>{{ u.nome }}</td>
        <td>{{ u.email }}</td>
        <td class="actions">
          <button class="btn-approve" @click="openConfirm(u,'aprovado')">✔ Aprovar</button>
        </td>
        <td class="actions">
          <button class="btn-reject" @click="openConfirm(u,'rejeitado')">✖ Rejeitar</button>
        </td>
      </tr>
    </tbody>
  </table>
  <div v-else class="empty-state">Nenhum aluno pendente.</div>
</div>

<div class="back-container">
  <router-link :to="{ name: 'home' }" class="button-custom">戻 Voltar ao Menu</router-link>
</div>

<div v-if="showConfirm" class="modal-overlay" @click.self="showConfirm=false">
  <div class="modal-content">
    <p>
      Confirmar {{ actionType==='aprovado' ? 'aprovação' : 'rejeição' }} do aluno
      <strong>{{ selected.nome }}</strong>?
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
  name: 'UsuariosPendentes',
  data () {
    return {
      usuarios: [],
      showConfirm: false,
      selected: {},
      actionType: 'aprovado',
      toast: ''
    }
  },
  created () { this.carregar() },
  methods: {
    carregar () {
      this.$http.get('http://localhost:5000/usuarios/pendentes')
        .then(res => { this.usuarios = res.body })
        .catch(() => alert('Erro ao carregar usuários pendentes.'))
    },
    openConfirm (u, tipo) {
      this.selected = u
      this.actionType = tipo
      this.showConfirm = true
    },
    confirmarAcao () {
      this.showConfirm = false
      this.$http.put('http://localhost:5000/usuarios/status', {
        id: this.selected._id,
        novo_status: this.actionType
      })
        .then(() => {
          const msg = this.actionType === 'aprovado'
            ? `Aluno ${this.selected.nome} aprovado!`
            : `Aluno ${this.selected.nome} rejeitado.`
          this.toastMsg(msg)
          this.carregar()
        })
        .catch(() => alert('Erro ao atualizar status do usuário.'))
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
.pend-table{width:100%;border-collapse:collapse}
.pend-table th,.pend-table td{padding:.75rem;border-bottom:1px solid #333;text-align:left}
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
