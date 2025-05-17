<template>
  <div class="book-detail-container">
    <div class="book-card-detail">
      <!-- Capa -->
      <div class="cover-column">
        <img v-if="livro.imagem_url" :src="livro.imagem_url" alt="Capa" class="book-cover-detail" />
      </div>

      <!-- Informações -->
      <div class="info-column">
        <h2 class="book-title-detail">{{ livro.titulo }}</h2>
        <p class="book-author-detail">por {{ livro.autor }}</p>
        <div class="book-sinopse">{{ livro.descricao }}</div>

        <ul class="additional-info">
          <li><strong>Ano:</strong> {{ livro.ano }}</li>
          <li><strong>Status:</strong> {{ livro.status }}</li>
          <li><strong>Quantidade:</strong> {{ livro.quantidade }}</li>
          <li v-if="livro.genero"><strong>Gênero:</strong> {{ livro.genero }}</li>
          <li v-if="livro.numero_paginas"><strong>Páginas:</strong> {{ livro.numero_paginas }}</li>
          <li v-if="livro.edicao"><strong>Edição:</strong> {{ livro.edicao }}</li>
          <li v-if="livro.isbn"><strong>ISBN:</strong> {{ livro.isbn }}</li>
        </ul>

        <!-- Botões de ação (aluno ou bibliotecário) -->
        <div class="action-row">
          <button
            v-if="canSolicitar"
            class="button-custom reserve-btn"
            @click="showConfirm = true"
          >Reservar Livro</button>

          <router-link
            v-else-if="canEditar"
            :to="{ name: 'update', params: { id: livro._id } }"
            class="button-custom reserve-btn"
          >Editar Livro</router-link>
        </div>

        <!-- QR Code -->
                <div class="qr-section" v-if="livro.qr_code">
          <h3 class="qr-label">QR Code de Reserva</h3>
          <img
            :src="`data:image/png;base64,${livro.qr_code}`"
            alt="QR Code"
            class="qr-thumbnail"
            @click="showQr = true"
          />
        </div>

        <!-- Navegação -->
        <div class="nav-buttons">
          <button class="btn-secondary" @click="$router.back()">← Voltar</button>
          <router-link :to="{ name: 'home' }" class="button-custom">戻 Menu</router-link>
        </div>
      </div>
    </div>

    <!-- Overlay QR Ampliado -->
    <div v-if="showQr" class="qr-overlay" @click.self="showQr = false">
      <img :src="`data:image/png;base64,${livro.qr_code}`" alt="QR Code" class="qr-full" />
      <button class="close-btn" @click="showQr = false">×</button>
    </div>

    <!-- Modal de confirmação -->
    <div v-if="showConfirm" class="modal-overlay" @click.self="showConfirm=false">
      <div class="modal-content">
        <p>Confirmar reserva de '<strong>{{ livro.titulo }}</strong>'?</p>
        <div class="modal-actions">
          <button class="button-custom" @click="confirmReserva">Sim</button>
          <button class="btn-secondary" @click="showConfirm = false">Não</button>
        </div>
      </div>
    </div>

    <!-- Toast de sucesso -->
    <div v-if="showSuccess" class="toast-overlay">
      <div class="toast-content">✔ Reserva solicitada!</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Livro',
  data () {
    return {
      livro: {},
      showQr: false,
      showConfirm: false,
      showSuccess: false,
      usuario: JSON.parse(localStorage.getItem('usuario') || '{}')
    }
  },
  computed: {
    canSolicitar () {
      return this.usuario.tipo === 'aluno' && this.livro.status === 'Disponível' && this.livro.quantidade > 0
    },
    canEditar () {
      return this.usuario.tipo === 'bibliotecario'
    }
  },
  methods: {
    confirmReserva () {
      this.$http.post('http://localhost:5000/reservas', {
        aluno_id: this.usuario._id,
        livro_id: this.livro._id
      })
        .then(() => {
          this.showConfirm = false
          this.showSuccess = true
          setTimeout(() => { this.showSuccess = false }, 2200)
        })
        .catch(() => {
          this.showConfirm = false
          alert('Erro ao solicitar reserva.')
        })
    }
  },
  created () {
    const id = this.$route.params.id
    this.$http.get(`http://localhost:5000/livros/${id}`)
      .then(res => { this.livro = res.body })
      .catch(() => {
        alert('Erro ao carregar livro.')
        this.$router.push({ name: 'list' })
      })
  }
}
</script>

<style scoped>
/***** Layout *****/
.book-detail-container{background:var(--color-bg);color:var(--color-secondary);min-height:100vh;padding:2rem;display:flex;justify-content:center;align-items:center}
.book-card-detail{display:flex;gap:1.5rem;max-width:800px;width:100%;background:#1f1f1f;border-radius:12px;overflow:hidden;box-shadow:0 0 15px rgba(0,0,0,.5)}
.cover-column{flex:0 0 40%}
.book-cover-detail{width:100%;height:100%;object-fit:cover}
.info-column{flex:1;padding:1.5rem;border-left:4px solid var(--color-primary);display:flex;flex-direction:column}

/***** Texto *****/
.book-title-detail{font-family:var(--font-heading);font-size:2rem;color:#f4f4f4;margin-bottom:.5rem}
.book-author-detail{font-style:italic;color:var(--color-secondary);margin-bottom:1rem}
.book-sinopse{max-height:200px;overflow-y:auto;line-height:1.6;color:#ddd;margin-bottom:1rem;padding-right:.5rem}
.additional-info{list-style:none;padding:0;margin:0 0 1rem}
.additional-info li{margin-bottom:.5rem;color:var(--color-secondary)}

/***** QR *****/
.qr-section{margin-top:1rem}
.qr-label{font-weight:bold;margin-bottom:.5rem;color:#f4f4f4}
.qr-thumbnail{width:120px;border:2px solid var(--color-primary);border-radius:8px;cursor:pointer;transition:transform .2s}
.qr-thumbnail:hover{transform:scale(1.05)}
.qr-overlay{position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,0,0,.8);display:flex;justify-content:center;align-items:center;z-index:200}
.qr-full{max-width:80%;max-height:80%}
.close-btn{position:absolute;top:1rem;right:1rem;background:transparent;border:none;font-size:2rem;color:#fff;cursor:pointer}

/***** Botões *****/
.action-row{display:flex;flex-wrap:wrap;gap:1rem;margin-bottom:1.5rem}
.button-custom{background:var(--color-primary);color:#fff;padding:.5rem 1rem;border:none;border-radius:6px;cursor:pointer;transition:background .2s}
.button-custom:hover{background:#b33636}
.btn-secondary{background:#6c757d;color:#fff;padding:.5rem 1rem;border:none;border-radius:6px;cursor:pointer;transition:background .2s}
.btn-secondary:hover{background:#5a6268}
.reserve-btn{margin:0;align-self:flex-start}
.nav-buttons{display:flex;flex-wrap:wrap;gap:1rem;margin-top:auto}

/***** Modal de confirmação *****/
.modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;z-index:300}
.modal-content{background:#1f1f1f;padding:1.5rem;border-radius:8px;color:#f4f4f4;text-align:center;width:90%;max-width:400px}
.modal-actions{display:flex;justify-content:center;gap:1rem;margin-top:1rem}

/***** Toast *****/
.toast-overlay{position:fixed;bottom:2rem;left:50%;transform:translateX(-50%);z-index:400}
.toast-content{background:var(--color-primary);color:#fff;padding:.6rem 1.5rem;border-radius:8px;box-shadow:0 0 10px rgba(0,0,0,.4);font-weight:600}

/***** Responsivo *****/
@media(max-width:768px){.book-card-detail{flex-direction:column}.cover-column,.info-column{flex:none;width:100%;border-left:none}}
</style>
