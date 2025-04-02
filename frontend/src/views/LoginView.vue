<template>
  <div class="login-container">
    <h2>Welcom Stock Monitoring Service</h2>
    <input type="text" v-model="username" placeholder="아이디 입력" />
    <input type="password" v-model="password" placeholder="비밀번호 입력" />
    <button @click="login">로그인</button>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        // const response = await axios.post("http://localhost:8000/users/login", {
        //   username: this.username,
        //   password: this.password,
        // });
        // alert(response.data.message);
        this.$router.push("/main"); // 로그인 후 메인 화면 이동
      } catch (error) {
        this.errorMessage = "로그인 실패!";
      }
    },
  },
};
</script>

<style>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
</style>