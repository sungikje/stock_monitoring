<template>
  <div class="monitoring-container">
    <div v-for="company in companies" :key="company.id" class="company-card">
      <!-- 회사명 -->
      <div class="company-info">
        <span class="label">회사명:</span>
        <span class="value">{{ company.name }}</span>
      </div>

      <!-- 최근 주가 -->
      <div class="company-info">
        <span class="label">최근 주가:</span>
        <span class="value">{{ company.latestPrice }}원</span>
      </div>

      <!-- 주가 그래프 -->
      <div class="chart-container">
        <canvas :ref="'chart-' + company.id"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";

export default {
  data() {
    return {
      companies: [
        {
          id: 1,
          name: "삼성전자",
          latestPrice: 75000,
          history: [72000, 73000, 74000, 75000],
        },
        {
          id: 2,
          name: "현대자동차",
          latestPrice: 205000,
          history: [200000, 202000, 204000, 205000],
        },
        {
          id: 3,
          name: "네이버",
          latestPrice: 380000,
          history: [375000, 376000, 378000, 380000],
        },
      ],
    };
  },
  mounted() {
    this.companies.forEach((company) => {
      this.renderChart(company.id, company.history);
    });
  },
  methods: {
    renderChart(companyId, data) {
      const ctx = this.$refs["chart-" + companyId][0].getContext("2d");
      new Chart(ctx, {
        type: "line",
        data: {
          labels: ["1일 전", "2일 전", "3일 전", "오늘"],
          datasets: [
            {
              label: "주가 변화",
              data: data,
              borderColor: "blue",
              borderWidth: 2,
              fill: false,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: false },
          },
        },
      });
    },
  },
};
</script>

<style scoped>
.monitoring-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.company-card {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.company-info {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.label {
  font-weight: bold;
}

.value {
  color: #333;
}

.chart-container {
  width: 100%;
  height: 200px;
}
</style>
