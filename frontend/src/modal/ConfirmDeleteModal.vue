<template>
    <div class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-content">
        <h2>정말 삭제하시겠습니까?</h2>
        <p>{{ companyName }} 회사를 관심 목록에서 삭제합니다.</p>
        <div class="modal-actions">
          <button @click="$emit('confirm')">삭제</button>
          <button @click="$emit('close')">취소</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      companyName: String,
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
  