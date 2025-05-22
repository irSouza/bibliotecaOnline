<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <span class="kanji-icon" aria-hidden="true">書</span>
      <h2 class="titulo-header">Dashboard da Biblioteca</h2>
    </header>

    <div class="metrics-grid">
      <div class="metric-card total">
        <h5>Total de Livros</h5>
        <p class="metric-value">{{ total }}</p>
      </div>
      <div class="metric-card disponiveis">
        <h5>Disponíveis</h5>
        <p class="metric-value">{{ disponiveis }}</p>
      </div>
      <div class="metric-card emprestados">
        <h5>Emprestados</h5>
        <p class="metric-value">{{ emprestados }}</p>
      </div>
    </div>

    <div class="charts-grid">
      <div class="chart-card">
        <h5>Disponível × Emprestado</h5>
        <canvas ref="statusChart" height="180"></canvas>
      </div>
      <div class="chart-card">
        <h5>Livros por Gênero</h5>
        <canvas ref="genreChart" height="180"></canvas>
      </div>
    </div>

    <div class="back-container">
      <router-link :to="{ name: 'home' }" class="button-custom">戻 Voltar ao Menu</router-link>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js'

export default {
  name: 'Dashboard',
  data () {
    return {
      total: 0,
      disponiveis: 0,
      emprestados: 0,
      genreCounts: {},
      statusChartInstance: null,
      genreChartInstance: null
    }
  },
  methods: {
    fetchMetrics () {
      this.$http.get('http://localhost:5000/livros')
        .then(res => {
          const livros = res.body || []
          this.total = livros.length
          this.disponiveis = livros.filter(l => l.status === 'Disponível').length
          this.emprestados = livros.filter(l => l.status === 'Emprestado').length
          this.genreCounts = livros.reduce((acc, l) => {
            const g = l.genero || 'Não especificado'
            acc[g] = (acc[g] || 0) + 1
            return acc
          }, {})

          this.$nextTick(this.renderCharts)
        })
        .catch(() => alert('Erro ao carregar dados do dashboard.'))
    },
    renderCharts () {
      if (this.statusChartInstance) this.statusChartInstance.destroy()
      if (this.genreChartInstance) this.genreChartInstance.destroy()

      this.statusChartInstance = new Chart(this.$refs.statusChart.getContext('2d'), {
        type: 'pie',
        data: {
          datasets: [{
            data: [this.disponiveis, this.emprestados],
            backgroundColor: ['#28a745', '#dc3545']
          }],
          labels: ['Disponíveis', 'Emprestados']
        },
        options: {
          legend: { position: 'bottom', labels: { fontColor: '#f4f4f4' } }
        }
      })

      this.genreChartInstance = new Chart(this.$refs.genreChart.getContext('2d'), {
        type: 'horizontalBar',
        data: {
          labels: Object.keys(this.genreCounts),
          datasets: [{
            label: 'Livros',
            data: Object.values(this.genreCounts),
            backgroundColor: '#36a2eb'
          }]
        },
        options: {
          scales: {
            xAxes: [{ ticks: { beginAtZero: true, fontColor: '#f4f4f4' }, gridLines: { color: '#444' } }],
            yAxes: [{ ticks: { fontColor: '#f4f4f4' }, gridLines: { display: false } }]
          },
          legend: { display: false }
        }
      })
    }
  },
  mounted () {
    this.fetchMetrics()
  }
}
</script>

<style scoped>
.dashboard-container {
  background: var(--color-bg);
  color: var(--color-secondary);
  min-height: 100vh;
  padding: 2rem 1rem;
  max-width: 1000px;
  margin: 0 auto;
}
.dashboard-header {
  text-align: center;
  margin-bottom: 2rem;
}
.kanji-icon { font-size: 2.5rem; color: var(--color-primary); display: block; margin: 0 auto; }
.titulo-header { font-size: 1.75rem; margin-top: 0.5rem; }
.metrics-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(200px,1fr)); gap: 1.5rem; margin-bottom: 2rem; }
.metric-card { background:#1f1f1f; border-radius:8px; padding:1.5rem; box-shadow:0 4px 12px rgba(0,0,0,.5); text-align:center; }
.metric-card.total{border-top:4px solid var(--color-primary);} .metric-card.disponiveis{border-top:4px solid var(--color-success);} .metric-card.emprestados{border-top:4px solid var(--color-danger);} .metric-card h5{margin-bottom:.5rem;font-weight:500;} .metric-value{font-size:2.5rem;margin:0;}

.charts-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:2rem;margin-bottom:2rem;}
.chart-card{background:#1f1f1f;border-radius:8px;padding:1rem;box-shadow:0 4px 12px rgba(0,0,0,.5);} .chart-card h5{text-align:center;margin-bottom:1rem;font-weight:500;}

.back-container{text-align:center;} .button-custom{background:var(--color-primary);color:#fff;padding:.5rem 1.5rem;border:none;border-radius:6px;cursor:pointer;transition:background .2s ease;} .button-custom:hover{background:#b33636;}
</style>
