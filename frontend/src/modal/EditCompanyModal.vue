<template>
    <div class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-content">
        <h2>관찰 기간 수정</h2>
        <p>{{ company.company_name }}의 관찰 기간을 수정하세요.</p>
        <input v-model="newPeriod" placeholder="예: 1개월, 3개월" />
        <div class="modal-actions">
          <button @click="submit()">수정</button>
          <button @click="$emit('close')">취소</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      company: Object,
    },
    data() {
      return {
        newPeriod: this.company.industry_period,
      };
    },
    methods: {
      async submit() {
        this.$emit("confirm", {
          company_name: this.company.company_name,
          industry_period: this.newPeriod,
        });
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
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .modal-content {
    background: white;
    padding: 30px;
    border-radius: 10px;
    min-width: 300px;
  }
  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }
  </style>
  