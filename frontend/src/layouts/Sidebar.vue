<template>
  <div class="sidebar">
    <!-- 날짜 & 시간 표시 -->
    <div class="datetime">
      <p>{{ currentDate }}</p>
      <p>{{ currentTime }}</p>
    </div>

    <!-- 메뉴 항목 -->
    <nav class="menu">
      <ul>
        <li>
          <router-link to="/edit-companies">📊 관심 기업</router-link>
        </li>
        <li>
          <router-link to="/monitoring">📈 주식 모니터링</router-link>
        </li>
        <!-- <li><a href="#">⚙ 설정</a></li> -->
      </ul>
    </nav>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentDate: "",
      currentTime: "",
    };
  },
  mounted() {
    this.updateDateTime();
    setInterval(this.updateDateTime, 1000); // 초 단위 갱신
  },
  methods: {
    updateDateTime() {
      const now = new Date();
      this.currentDate = now.toLocaleDateString("ko-KR", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      });
      this.currentTime = now.toLocaleTimeString("ko-KR");
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 260px;
  height: 100vh;
  background: linear-gradient(to bottom, #6cb4ee, #87ceeb);
  color: white;
  display: flex;
  flex-direction: column;
  font-family: "Arial", sans-serif;
  box-shadow: 3px 0 5px rgba(0, 0, 0, 0.1);
}

/* 날짜 & 시간 */
.datetime {
  padding: 20px;
  text-align: center;
  height: 93px;
  display: flex;
  flex-direction: column; /* ✅ 위-아래로 정렬 */
  align-items: center; /* ✅ 세로 중앙 정렬 */
  justify-content: center; /* ✅ 가로 중앙 정렬 */
  background: rgba(255, 255, 255, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.datetime p {
  margin: 5px 0;
  font-size: 16px;
  font-weight: bold;
}

/* 메뉴 */
.menu {
  flex-grow: 1;
  padding-top: 15px;
}

.menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu li {
  padding: 15px 20px;
}

.menu a {
  color: white;
  font-size: 18px;
  font-weight: bold;
  text-decoration: none;
  display: block;
  transition:
    background 0.3s,
    transform 0.2s;
}

.menu a:hover {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  transform: scale(1.05);
}
</style>
