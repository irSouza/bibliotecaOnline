<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card-custom p-5">

      <!-- Kanji + Título -->
      <div class="text-center mb-4">
        <div class="kanji-logo-nav kanji-logo-large">書</div>
        <h2 class="titulo-header">Biblioteca Online</h2>
        <p class="text-caption">Biblioteca para todos!</p>
      </div>

      <!-- Mensagem de erro -->
      <div v-if="erro" class="alert alert-danger">
        {{ erro }}
      </div>

      <!-- Formulário de login -->
      <form @submit.prevent="login">
        <div class="form-group mb-3">
          <label class="text-light">Email</label>
          <input
            v-model="email"
            type="email"
            required
            class="form-control input-dark"
          />
        </div>

        <div class="form-group mb-4">
          <label class="text-light">Senha</label>
          <input
            v-model="senha"
            type="password"
            required
            class="form-control input-dark"
          />
        </div>

        <button type="submit" class="btn btn-primary w-100 py-2">
          Entrar
        </button>
      </form>

      <!-- Link para cadastro -->
      <div class="text-center mt-4">
        <router-link :to="{ name: 'cadastro' }" class="link-cadastro">
          Criar nova conta
        </router-link>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      email: '',
      senha: '',
      erro: ''
    }
  },
  methods: {
    login () {
      this.$http.post('http://localhost:5000/login', {
        email: this.email,
        senha: this.senha
      }).then(res => {
        const usuario = res.body.usuario
        localStorage.setItem('logado', 'true')
        localStorage.setItem('usuario', JSON.stringify(usuario))
        this.$router.push({ name: 'home' })
      }).catch(err => {
        this.erro = err.body && err.body.mensagem
          ? err.body.mensagem
          : 'Erro ao fazer login.'
      })
    }
  }
}
</script>

<style scoped>
.vh-100 {
  height: 100vh !important;
}

.card-custom {
  position: relative;
  background-color: #1f1f1f;
  border-radius: 14px;
  width: 100%;
  max-width: 400px;
  /* Iluminação suave em volta do painel */
  box-shadow: 0 0 20px var(--color-primary);
}

.kanji-logo-large {
  font-size: 64px;
}

.titulo-header {
  font-family: var(--font-heading);
  font-size: 32px;
  color: #f4f4f4;
  margin-top: 10px;
}

.text-caption {
  color: var(--color-secondary);
}

.input-dark {
  background-color: #2a2a2a;
  color: #f4f4f4;
  border: 1px solid #444;
}

.input-dark:focus {
  border-color: var(--color-primary);
  box-shadow: none;
}

.btn-primary {
  background-color: var(--color-primary);
  border: none;
}

.link-cadastro {
  color: var(--color-primary);
  text-decoration: none;
}

.link-cadastro:hover {
  color: #fff;
  text-decoration: underline;
}
</style>
