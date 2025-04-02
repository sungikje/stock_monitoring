<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>