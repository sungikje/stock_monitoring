<template>
  <div class="login-container">
    <h2>Welcome Stock Monitoring Service</h2>
    <input v-model="username" type="text" placeholder="아이디 입력" />
    <input v-model="password" type="password" placeholder="비밀번호 입력" />

    <div class="btn-group">
      <button @click="login">로그인</button>
      <button @click="showSignupModal = true">회원가입</button>
    </div>

    <p v-if="errorMessage">{{ errorMessage }}</p>

    <!-- 회원가입 모달 컴포넌트 사용 -->
    <SignupModal :visible="showSignupModal" @close="showSignupModal = false" />
  </div>
</template>

<script>
import { mapActions } from "vuex";
import SignupModal from "@/modal/SignupModal.vue";
import axios from "axios";

export default {
  components: {
    SignupModal,
  },
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
      showSignupModal: false,
    };
  },
  methods: {
    async login() {
      try {
        const res = await axios.post("http://localhost:8000/api/login", {
          email: this.username,
          password: this.password,
        });
        await this.user_login(res.data.access_token);
        this.$router.push("/main");
      } catch (error) {
        this.errorMessage = "로그인 실패!";
      }
    },
    ...mapActions(["user_login"]),
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.btn-group {
  display: flex;
  gap: 10px;
}
</style>
