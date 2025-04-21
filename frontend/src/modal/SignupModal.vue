<template>
  <div class="modal-overlay" v-if="visible">
    <div class="modal-content">
      <h3>회원가입</h3>
      <input
        v-model="signupInfo.username"
        type="text"
        placeholder="이름 (필수)"
      />
      <input
        v-model="signupInfo.email"
        type="email"
        placeholder="이메일 (필수)"
      />
      <input
        v-model="signupInfo.password"
        type="password"
        placeholder="비밀번호 (필수)"
      />
      <input
        v-model="signupInfo.phone"
        type="text"
        placeholder="전화번호 (선택)"
      />

      <div class="modal-buttons">
        <button @click="register">가입하기</button>
        <button @click="$emit('close')">닫기</button>
      </div>
      <p v-if="signupError">{{ signupError }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    visible: Boolean,
  },
  data() {
    return {
      signupInfo: {
        username: "",
        email: "",
        password: "",
        phone: "",
      },
      signupError: "",
    };
  },
  methods: {
    async register() {
      const { username, email, password } = this.signupInfo;
      if (!username || !email || !password) {
        this.signupError = "이름, 이메일, 비밀번호는 필수입니다.";
        return;
      }

      try {
        // await axios.post("http://localhost:8000/users/register", this.signupInfo);
        alert("회원가입 완료!");
        this.signupError = "";
        this.$emit("close");
      } catch (err) {
        this.signupError = "회원가입 실패!";
      }
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.modal-buttons {
  display: flex;
  justify-content: space-between;
}
</style>
