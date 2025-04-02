import { createRouter, createWebHistory } from "vue-router";
import LoginView from "@/views/LoginView.vue";
import MainLayout from "@/layouts/MainLayout.vue";
import EditCompanies from "@/views/EditCompanies.vue";
import Monitoring from "@/views/Monitoring.vue";
// import AdminMenu from "@/views/AdminMenu.vue";

const routes = [
  {
    path: "/",
    name: "Login",
    component: LoginView, // 🚀 기본 경로에서 LoginView 표시
  },
  {
    path: "/main",
    component: MainLayout, // 🚀 헤더 + 사이드바 포함된 레이아웃
    children: [
      { path: "edit-companies", name: "EditCompanies", component: EditCompanies },
      { path: "monitoring", name: "Monitoring", component: Monitoring },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;