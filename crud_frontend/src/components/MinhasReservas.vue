<template>
  <div class="reservas-container">
    <!-- Cabeçalho -->
    <header class="reservas-header">
      <span class="kanji-icon-large">予約</span>
      <h2 class="titulo-header">Minhas Reservas</h2>
    </header>

<!-- Loader / vazio -->
<div v-if="loading" class="empty-state">Carregando reservas…</div>

<!-- Tabela -->
<div v-else class="table-card">
  <table v-if="reservas.length" class="reservas-table">
    <thead>
      <tr>
        <th>Livro</th>
        <th>Status</th>
        <th>Devolver&nbsp;até</th>
        <th>QR&nbsp;Code</th>
        <th v-if="hasAcao">Ação</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="r in reservas" :key="r._id">
        <td>{{ r.livro.titulo }}</td>
        <td><span :class="['badge-status', r.status]">{{ r.status }}</span></td>
        <td>{{ r.data_limite ? formatDate(r.data_limite) : '—' }}</td>
        <td>
          <img
            v-if="r.status==='aprovado' && r.qr_code"
            :src="`data:image/png;base64,${r.qr_code}`"
            alt="QR"
            class="qr-img"
            @click="abrirQr(r.qr_code)"
          />
          <span v-else>—</span>
        </td>
        <td v-if="hasAcao">
          <button
            v-if="r.status==='aprovado'"
            class="btn-action devolver"
            @click="openConfirm(r)"
          >
            Devolver
          </button>
        </td>
      </tr>
    </tbody>
  </table>
  <div v-else class="empty-state">Nenhuma reserva encontrada.</div>
</div>

<!-- Botão Voltar -->
<div class="back-container">
  <router-link :to="{ name: 'home' }" class="button-custom">戻Voltar ao Menu</router-link>
</div>

<!-- Overlay QR -->
<div v-if="qrFull" class="qr-overlay" @click.self="qrFull=''">
  <img :src="`data:image/png;base64,${qrFull}`" alt="QR Code" class="qr-full" />
  <button class="close-btn" @click="qrFull=''">×</button>
</div>

<!-- Modal confirmar devolução -->
<div v-if="showConfirm" class="modal-overlay" @click.self="showConfirm=false">
  <div class="modal-content">
    <p>
      Confirmar devolução de
      <strong>{{ modalTitulo }}</strong>?
    </p>
    <div class="modal-actions">
      <button class="button-custom" @click="devolverReserva">Sim</button>
      <button class="btn-secondary" @click="showConfirm=false">Não</button>
    </div>
  </div>
</div>

<!-- Toast -->
<div v-if="toastMsg" class="toast-overlay" @animationend="toastMsg=''">
  <div class="toast-content">{{ toastMsg }}</div>
</div>

  </div>
</template>

<script>
export default {
  name: 'MinhasReservas',
  data () {
    return {
      reservas: [],
      loading: true,
      qrFull: '',
      showConfirm: false,
      selected: null,
      toastMsg: ''
    }
  },
  computed: {
    hasAcao () {
      return this.reservas.some(r => r.status === 'aprovado')
    },
    modalTitulo () {
      return this.selected && this.selected.livro ? this.selected.livro.titulo : ''
    }
  },
  methods: {
    formatDate (iso) {
      const d = new Date(iso)
      return isNaN(d) ? '—' : d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
    },
    abrirQr (code) {
      this.qrFull = code
    },
    openConfirm (r) {
      this.selected = r
      this.showConfirm = true
    },
    async devolverReserva () {
      try {
        await this.$http.put('http://localhost:5000/reservas/devolver', {
          reserva_id: this.selected._id
        })
        this.toastMsg = '✔ Livro devolvido!'
        this.showConfirm = false
        this.fetchReservas()
      } catch (_) {
        alert('Erro ao devolver reserva.')
      }
    },
    async fetchReservas () {
      const user = JSON.parse(localStorage.getItem('usuario') || '{}')
      if (!user._id) {
        this.loading = false
        return
      }
      try {
        const res = await this.$http.get(`http://localhost:5000/reservas/aluno_com_livros/${user._id}`)
        this.reservas = res.body || []
      } catch (_) {
        alert('Erro ao carregar reservas.')
      } finally {
        this.loading = false
      }
    }
  },
  created () {
    this.fetchReservas()
  }
}
</script>

<style scoped>
/* Paleta e elementos já existentes */
.reservas-container{background:var(--color-bg);color:var(--color-secondary);min-height:100vh;padding:2rem 1rem;max-width:900px;margin:0 auto}
.table-card{background:#1f1f1f;border-radius:8px;padding:1rem;overflow-x:auto}
.reservas-table{width:100%;border-collapse:collapse}
.reservas-table th,.reservas-table td{padding:.75rem;border:1px solid #333;text-align:center}
.badge-status{padding:.25rem .75rem;border-radius:12px;font-size:.85rem;text-transform:capitalize}
.badge-status.aprovado{background:rgba(40,167,69,.7);color:#fff}
.badge-status.pendente{background:rgba(255,193,7,.7);color:#000}
.badge-status.rejeitado{background:rgba(220,53,69,.7);color:#fff}
.badge-status.devolvido{background:rgba(108,117,125,.7);color:#fff}
.qr-img{max-width:80px;cursor:pointer}
.btn-action.devolver{background:var(--color-primary);color:#fff;border:none;padding:.4rem .8rem;border-radius:6px;cursor:pointer}
.btn-action.devolver:hover{background:#b33636}
.back-container{text-align:center;margin-top:1.5rem}
.button-custom{background:var(--color-primary);color:#fff;padding:.5rem 1.5rem;border:none;border-radius:6px;cursor:pointer;transition:background .2s}
.button-custom:hover{background:#b33636}
/* Modal / toast */
.modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.8);display:flex;align-items:center;justify-content:center;z-index:1100}
.modal-content{background:#1f1f1f;padding:1.5rem;border-radius:8px;color:#f4f4f4;text-align:center;max-width:350px;width:90%}
.modal-actions{display:flex;justify-content:center;gap:1rem;margin-top:1rem}
.btn-secondary{background:#6c757d;color:#fff;border:none;padding:.4rem 1rem;border-radius:6px}
.btn-secondary:hover{background:#5a6268}
.toast-overlay{position:fixed;bottom:1rem;left:50%;transform:translateX(-50%);z-index:1200;animation:fade 2.5s forwards}
.toast-content{background:#1f1f1f;color:#fff;padding:.75rem 1.5rem;border-radius:6px;border:1px solid var(--color-primary)}
@keyframes fade{0%{opacity:0}10%,80%{opacity:1}100%{opacity:0}}
/* QR overlay */
.qr-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.8);display:flex;align-items:center;justify-content:center;z-index:1150}
.qr-full{max-width:300px;width:90%;border:8px solid #fff;border-radius:8px}
.close-btn{position:absolute;top:1rem;right:1rem;font-size:2rem;background:none;border:none;color:#fff;cursor:pointer}
.empty-state{text-align:center;color:#777;margin:2rem 0}
.reservas-header{display:flex;align-items:center;justify-content:center;gap:.5rem;margin-bottom:1.5rem;padding-top:80px}
.kanji-icon-large{font-size:2.5rem;color:var(--color-primary);display:block;margin:0}
</style>
