<template>
  <nav class="navbar-custom d-flex justify-content-between align-items-center px-4 py-2">
    <div class="d-flex align-items-center gap-2">
      <span class="kanji-logo-nav">書</span>
      <span class="titulo-navbar">Biblioteca Online</span>
    </div>

    <button class="hamburger-btn" @click="toggleMenu" aria-label="Menu">
      <span></span>
      <span></span>
      <span></span>
    </button>

    <div :class="['menu-links', 'd-flex', 'gap-4', { open: menuOpen }]">
      <router-link
        :to="{ name: 'home' }"
        exact-active-class="active-link"
      >
        Home
      </router-link>

      <router-link
        :to="{ name: 'list' }"
        exact-active-class="active-link"
      >
        Listar
      </router-link>

      <router-link
        :to="{ name: 'filtro' }"
        exact-active-class="active-link"
      >
        Buscar
      </router-link>

      <router-link
        v-if="isBibliotecario"
        :to="{ name: 'dashboard' }"
        exact-active-class="active-link"
      >
        Dashboard
      </router-link>

      <router-link
        v-if="isAluno"
        :to="{ name: 'minhas-reservas' }"
        exact-active-class="active-link"
      >
        Minhas Reservas
      </router-link>

      <a
        @click="logout"
        class="link-logout"
      >
        Sair
      </a>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  data () {
    return { menuOpen: false }
  },
  computed: {
    user () {
      const u = localStorage.getItem('usuario')
      return u ? JSON.parse(u) : {}
    },
    isBibliotecario () {
      return this.user.tipo === 'bibliotecario'
    },
    isAluno () {
      return this.user.tipo === 'aluno'
    }
  },
  methods: {
    toggleMenu () {
      this.menuOpen = !this.menuOpen
    },
    logout () {
      this.$emit('logout')
    }
  }
}
</script>

<style scoped>
.navbar-custom {
  position: fixed;
  top: 0;
  width: 100%;
  background: linear-gradient(135deg, rgba(18,18,18,0.95), rgba(30,30,30,0.95));
  backdrop-filter: blur(10px);
  border-bottom: 2px solid var(--color-primary);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
  z-index: 100;
  transition: background 0.3s ease;
}
.navbar-custom:hover {
  background: linear-gradient(135deg, rgba(18,18,18,1), rgba(30,30,30,1));
}

.kanji-logo-nav {
  font-family: var(--font-base);
  font-size: 28px;
  color: var(--color-primary);
}
.titulo-navbar {
  font-family: var(--font-heading);
  font-size: 20px;
  color: var(--color-secondary);
  margin-left: 4px;
}

.menu-links a,
.menu-links router-link {
  position: relative;
  padding: 0.5rem 0.75rem;
  color: var(--color-secondary);
  font-weight: 500;
  transition: color 0.2s ease;
}
.menu-links a:hover,
.menu-links router-link:hover,
.menu-links .active-link {
  color: var(--color-primary);
}
.menu-links a::after,
.menu-links router-link::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 0;
  height: 2px;
  background: var(--color-primary);
  transition: width 0.3s ease;
}
.menu-links a:hover::after,
.menu-links router-link:hover::after,
.menu-links .active-link::after {
  width: 100%;
}

.link-logout {
  padding: 0.5rem 0.75rem;
  color: var(--color-danger, #e63946);
  cursor: pointer;
  transition: color 0.2s ease;
}
.link-logout:hover {
  color: #fff;
}

.hamburger-btn {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 24px;
  height: 18px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
}
.hamburger-btn span {
  display: block;
  height: 3px;
  background: var(--color-secondary);
  border-radius: 2px;
  transition: background 0.2s ease;
}
.hamburger-btn:hover span {
  background: var(--color-primary);
}

@media (max-width: 768px) {
  .hamburger-btn {
    display: flex;
  }
  .menu-links {
    display: none;
    position: absolute;
    top: 60px;
    right: 0;
    background: var(--color-bg);
    flex-direction: column;
    gap: 0;
    padding: 1rem;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
    width: 200px;
  }
  .menu-links.open {
    display: flex;
  }
}
</style>
