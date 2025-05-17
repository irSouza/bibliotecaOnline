import Vue from 'vue'
import Router from 'vue-router'
import VueResource from 'vue-resource'

import Login from '../components/Login.vue'
import CadastroUsuario from '../components/CadastroUsuario.vue'
import Home from '../components/Home.vue'
import List from '../components/List.vue'
import Create from '../components/Create.vue'
import Update from '../components/Update.vue'
import Livro from '../components/Livro.vue'
import Filtro from '../components/Filtro.vue'
import Dashboard from '../components/Dashboard.vue'
import UsuariosPendentes from '../components/UsuariosPendentes.vue'
import ReservasPendentes from '../components/ReservasPendentes.vue'
import MinhasReservas from '../components/MinhasReservas.vue'

Vue.use(Router)
Vue.use(VueResource)

// Proteção de rotas: exige login
function requireAuth (to, from, next) {
  if (localStorage.getItem('logado') === 'true') {
    next()
  } else {
    next({ name: 'login' })
  }
}

export default new Router({
  mode: 'history',
  routes: [
    { path: '/', name: 'login', component: Login },
    { path: '/cadastro', name: 'cadastro', component: CadastroUsuario },
    { path: '/home', name: 'home', component: Home, beforeEnter: requireAuth },
    { path: '/list', name: 'list', component: List, beforeEnter: requireAuth },
    { path: '/create', name: 'create', component: Create, beforeEnter: requireAuth },
    { path: '/update', name: 'update', component: Update, beforeEnter: requireAuth },
    { path: '/livro/:id', name: 'livro', component: Livro, beforeEnter: requireAuth },
    { path: '/filtro', name: 'filtro', component: Filtro, beforeEnter: requireAuth },
    { path: '/dashboard', name: 'dashboard', component: Dashboard, beforeEnter: requireAuth },
    { path: '/usuarios-pendentes', name: 'usuarios-pendentes', component: UsuariosPendentes, beforeEnter: requireAuth },
    { path: '/reservas-pendentes', name: 'reservas-pendentes', component: ReservasPendentes, beforeEnter: requireAuth },
    { path: '/minhas-reservas', name: 'minhas-reservas', component: MinhasReservas, beforeEnter: requireAuth }

  ]
})
