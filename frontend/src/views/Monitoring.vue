<template>
  <div class="monitoring-container">
    <div v-if="isLoading" class="loading-message">
      차트 생성 중 ⏳ {{ loadingDots }}
    </div>
    <div v-else>
      <div v-for="chart in stockCharts" :key="chart.company_name">
        <p class="company-name">{{ chart.company_name }}</p>
        <img :src="server_static_url + chart.save_path" class="stock-image" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      stockCharts: [],
      isLoading: true,
      server_static_url: "http://localhost:8000/static",
      loadingDots: "",
      loadingInterval: null,
    };
  },
  methods: {
    async searchStockChart() {
      this.isLoading = true;
      this.startLoadingAnimation();

      try {
        const access_token = localStorage.getItem("access_token");
        const res = await axios.post(
          "http://localhost:8000/api/stock_monitoring",
          {},
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          },
        );
        this.stockCharts = res.data;
        this.isLoading = false;
      } catch (error) {
        console.error("Request failed:", error);
        this.errorMessage = error.message || "Request failed";
      }
    },
    startLoadingAnimation() {
      let dotCount = 0;
      this.loadingInterval = setInterval(() => {
        dotCount = (dotCount + 1) % 4; // 0, 1, 2, 3 -> ..., .., ., ''
        this.loadingDots = ".".repeat(dotCount);
      }, 500);
    },
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.searchStockChart();
    });
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

.company-name {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.stock-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
