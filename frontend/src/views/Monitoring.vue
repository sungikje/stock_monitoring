<template>
  <div class="monitoring-container">
    <div>
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
        server_static_url: 'http://localhost:8000/static'
    };
  },
  methods: {
    async searchStockChart() {
        try {
            const access_token = localStorage.getItem("access_token");
            const res = await axios.post(
                "http://localhost:8000/api/stock_monitoring",
                {}, 
                {
                    headers: {
                        Authorization: `Bearer ${access_token}`,
                    },
            });
            this.stockCharts = res.data;
            console.log(this.stockCharts)
      } catch (error) {
            console.error('Request failed:', error);
            this.errorMessage = error.message || "Request failed";
      }
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
