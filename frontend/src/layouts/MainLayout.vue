<template>
  <div class="layout">
    <!-- 사이드바 -->
    <Sidebar />

    <div class="content-area">
      <!-- 헤더 -->
      <LayoutHeader />

      <!-- 페이지 변경 영역 -->
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/layouts/Sidebar.vue";
import LayoutHeader from "@/layouts/LayoutHeader.vue";

export default {
  name: "MainLayout",
  components: {
    Sidebar,
    LayoutHeader,
  },
};
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

/* 사이드바 - 세로 전체 차지 */
.sidebar {
  width: 250px;
  height: 100vh;
  background-color: #2c3e50;
  color: white;
}

/* 사이드바 오른쪽 컨텐츠 영역 */
.content-area {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background-color: white;
}

/* 헤더 */
.header {
  height: 60px;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid #ddd;
}

/* 메인 컨텐츠 */
.main-content {
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
