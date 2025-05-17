<template>
  <div id="app">
    <!-- Navbar só aparece se estiver logado e não estivermos na tela de login -->
    <Navbar v-if="showNavbar" @logout="logout" />

    <main class="p-4">
      <router-view />
    </main>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'

export default {
  name: 'App',
  components: { Navbar },
  computed: {
    // Continua usando a flag de login, mas também bloqueia a rota 'login'
    logado () {
      return localStorage.getItem('logado') === 'true'
    },
    showNavbar () {
      return this.logado && this.$route.name !== 'login'
    }
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

<style>
/* Seu theme.css já cuida de html/body/#app */
</style>
