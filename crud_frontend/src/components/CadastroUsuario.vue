<template>
  <div class="register-container">
    <header class="register-header">
      <span class="kanji-icon">人</span>
      <h2 class="titulo-header">Cadastrar Usuário</h2>
    </header>

    <div v-if="mensagem" class="alert-success">{{ mensagem }}</div>

    <form @submit.prevent="cadastrar" class="register-form" novalidate>
      <div class="form-group">
        <label for="nome">Nome *</label>
        <input
          id="nome"
          v-model.trim="usuario.nome"
          @blur="touched.nome = true"
          type="text"
          class="input-dark"
          required
        />
        <small v-if="touched.nome && !usuario.nome" class="form-error">Campo obrigatório.</small>
      </div>

      <div class="form-group">
        <label for="email">Email *</label>
        <input
          id="email"
          v-model.trim="usuario.email"
          @blur="touched.email = true"
          type="email"
          class="input-dark"
          required
        />
        <small v-if="touched.email && !validEmail" class="form-error">Email inválido.</small>
      </div>

      <div class="form-group pwd-group">
        <label for="senha">Senha *</label>
        <div class="pwd-wrapper">
          <input
            id="senha"
            :type="showPwd ? 'text' : 'password'"
            v-model.trim="usuario.senha"
            @blur="touched.senha = true"
            placeholder="Mínimo 6 caracteres"
            class="input-dark pwd-input"
            required
          />
          <button
            type="button"
            class="pwd-toggle"
            :aria-label="showPwd ? 'Ocultar senha' : 'Mostrar senha'"
            @click="showPwd = !showPwd"
          >
            {{ showPwd ? '🙈' : '👁️' }}
          </button>
        </div>
        <small v-if="touched.senha && usuario.senha.length < 6" class="form-error">Mínimo 6 caracteres.</small>
      </div>

      <div class="form-group">
        <label for="tipo">Tipo *</label>
        <select
          id="tipo"
          v-model="usuario.tipo"
          @blur="touched.tipo = true"
          class="input-dark"
          required
        >
          <option disabled value="">Selecione</option>
          <option value="aluno">Aluno</option>
          <option value="bibliotecario">Bibliotecário</option>
        </select>
        <small v-if="touched.tipo && !usuario.tipo" class="form-error">Selecione o tipo.</small>
      </div>

      <div class="form-actions">
        <button type="submit" class="button-custom" :disabled="!formValid">Cadastrar</button>
        <router-link :to="{ name: 'login' }" class="btn-secondary">Cancelar</router-link>
      </div>
    </form>

    <div class="back-container">
      <router-link :to="{ name: 'login' }" class="button-custom">← Voltar ao Login</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CadastroUsuario',
  data () {
    return {
      usuario: { nome: '', email: '', senha: '', tipo: '' },
      touched: { nome: false, email: false, senha: false, tipo: false },
      mensagem: '',
      showPwd: false
    }
  },
  computed: {
    validEmail () { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.usuario.email) },
    formValid () {
      return (
        this.usuario.nome &&
        this.validEmail &&
        this.usuario.senha.length >= 6 &&
        this.usuario.tipo
      )
    }
  },
  methods: {
    cadastrar () {
      if (!this.formValid) {
        Object.keys(this.touched).forEach(k => { this.touched[k] = true })
        return
      }
      this.$http.post('http://localhost:5000/usuarios', this.usuario)
        .then(res => {
          this.mensagem = res.body.mensagem
          this.usuario = { nome: '', email: '', senha: '', tipo: '' }
          Object.keys(this.touched).forEach(k => { this.touched[k] = false })
        })
        .catch(() => { alert('Erro ao cadastrar usuário.') })
    }
  }
}
</script>

<style scoped>
.register-container {
  background: var(--color-bg);
  color: var(--color-secondary);
  min-height: 100vh;
  padding: 2rem 1rem;
  max-width: 500px;
  margin: 0 auto;
}
.register-header {
  text-align: center;
  margin-bottom: 1rem;
}
.kanji-icon {
  font-size: 2rem;
  color: var(--color-primary);
  display: block;
  margin: 0 auto;
}
.titulo-header {
  font-size: 1.75rem;
  margin-top: 0.5rem;
}
.form-group {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}
.input-dark {
  padding: 0.5rem;
  border: 1px solid #444;
  border-radius: 4px;
  background: #2a2a2a;
  color: #f4f4f4;
}
.input-dark:focus {
  outline: none;
  border-color: var(--color-primary);
}
.form-error {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}
.pwd-wrapper { position: relative; }
.pwd-input { padding-right: 2.5rem; }
.pwd-toggle {
  position: absolute;
  top: 0;
  right: 0.25rem;
  height: 100%;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: var(--color-secondary);
}
.pwd-toggle:focus { outline: none; }
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}
.button-custom {
  background: var(--color-primary);
  color: #fff;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;
}
.button-custom:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.btn-secondary {
  background: #6c757d;
  color: #fff;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;
}
.btn-secondary:hover { background: #5a6268; }
.alert-success {
  background: #2f522f;
  color: #d4edda;
  padding: 0.75rem;
  border-radius: 4px;
  text-align: center;
  margin-bottom: 1rem;
}
.back-container { text-align: center; margin-top: 1.5rem; }
</style>
