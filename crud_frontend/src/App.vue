<template>
  <div id="app">
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
</style>
