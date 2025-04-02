<template>
  <header class="layout-header">
    <h1>📈 관심 기업 모니터링 시스템</h1>
    <p>
      실시간으로 관심 있는 기업의 정보를 모니터링하고,  
      주식 시장의 변화를 빠르게 파악하세요.  
      간편한 UI로 기업을 추가하고, 원하는 정보를 빠르게 확인할 수 있습니다.
    </p>
  </header>
</template>

<script>
export default {
  name: "LayoutHeader",
};
</script>

<style scoped>
.layout-header {
  width: 100%;
  padding: 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
  text-align: center;
}

.layout-header h1 {
  font-size: 24px;
  font-weight: bold;
}

.layout-header p {
  font-size: 14px;
  color: #666;
}
</style>