<template>
  <div class="home-container">
    <header class="text-center mb-4">
      <div class="kanji-logo-large">書</div>
      <h2 class="titulo-header">Biblioteca Online</h2>
      <p class="text-caption">Painel principal</p>
    </header>

    <div class="buttons-grid d-grid gap-3">
      <router-link
        :to="{ name: 'list' }"
        class="btn button-custom d-flex align-items-center"
      >
        <span class="kanji-icon-small">書</span>
        <span class="ms-3">Ver Livros</span>
      </router-link>

      <router-link
        :to="{ name: 'filtro' }"
        class="btn button-custom d-flex align-items-center"
      >
        <span class="kanji-icon-small">探</span>
        <span class="ms-3">Buscar Livros</span>
      </router-link>

      <router-link
        v-if="usuario.tipo === 'bibliotecario'"
        :to="{ name: 'create' }"
        class="btn button-custom d-flex align-items-center"
      >
        <span class="kanji-icon-small">登</span>
        <span class="ms-3">Cadastrar Livro</span>
      </router-link>

      <router-link
        v-if="usuario.tipo === 'bibliotecario'"
        :to="{ name: 'usuarios-pendentes' }"
        class="btn button-custom d-flex align-items-center"
      >
        <span class="kanji-icon-small">学</span>
        <span class="ms-3">Alunos Pendentes</span>
      </router-link>

      <router-link
        v-if="usuario.tipo === 'bibliotecario'"
        :to="{ name: 'reservas-pendentes' }"
        class="btn button-custom d-flex align-items-center"
      >
        <span class="kanji-icon-small">予</span>
        <span class="ms-3">Reservas Pendentes</span>
      </router-link>

      <router-link
        v-if="usuario.tipo === 'bibliotecario'"
        :to="{ name: 'dashboard' }"
        class="btn button-custom d-flex align-items-center"
      >
        <span class="kanji-icon-small">情</span>
        <span class="ms-3">Dashboard</span>
      </router-link>

      <router-link
        v-if="usuario.tipo === 'aluno'"
        :to="{ name: 'minhas-reservas' }"
        class="btn button-custom d-flex align-items-center"
      >
        <span class="kanji-icon-small">所</span>
        <span class="ms-3">Minhas Reservas</span>
      </router-link>

      <button
        @click="logout"
        class="btn button-cancel d-flex align-items-center"
      >
        <span class="kanji-icon-small">出</span>
        <span class="ms-3">Sair</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      usuario: {}
    }
  },
  created () {
    const usuarioStorage = localStorage.getItem('usuario')
    this.usuario = usuarioStorage ? JSON.parse(usuarioStorage) : {}
  },
  methods: {
    logout () {
      localStorage.removeItem('logado')
      localStorage.removeItem('usuario')
      this.$router.push({ name: 'login' })
    }
  }
}
</script>

<style scoped>
.home-container {
  background-color: var(--color-bg);
  color: var(--color-secondary);
  min-height: 100vh;
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.kanji-logo-large {
  font-size: 64px;
  font-family: var(--font-base);
  color: var(--color-primary);
  font-weight: bold;
}

.titulo-header {
  font-family: var(--font-heading);
  font-size: 2rem;
  color: #f4f4f4;
  margin-top: 0.5rem;
}

.text-caption {
  color: var(--color-secondary);
  margin-top: 0.25rem;
}

.buttons-grid {
  width: 100%;
  max-width: 500px;
}

.button-custom {
  background-color: #2a2a2a;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #f4f4f4;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
  position: relative;
}

.button-custom:hover {
  background-color: var(--color-primary);
  color: #fff;
  box-shadow: 0 0 10px var(--color-primary);
}

.button-custom:hover .kanji-icon-small,
.button-cancel:hover .kanji-icon-small {
  color: #fff;
}

.button-cancel {
  background-color: var(--color-primary);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #fff;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.button-cancel:hover {
  background-color: #b33636;
  box-shadow: 0 0 10px var(--color-primary);
}

.button-cancel .kanji-icon-small {
  color: #fff;
}

.kanji-icon-small {
  font-size: 24px;
  font-family: var(--font-base);
  color: var(--color-primary);
}
</style>
