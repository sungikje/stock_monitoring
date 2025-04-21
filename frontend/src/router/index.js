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
            {
                path: "edit-companies",
                name: "EditCompanies",
                component: EditCompanies,
            },
            { path: "monitoring", name: "Monitoring", component: Monitoring },
        ],
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const publicPages = ["/"];
    const authRequired = !publicPages.includes(to.path);
    const token = localStorage.getItem("access_token");

    if (authRequired && (!token || isTokenExpired(token))) {
        return next("/"); // 토큰 없거나 만료되면 로그인으로 리디렉트
    }

    next();
});

function isTokenExpired(token) {
    try {
        const payload = JSON.parse(atob(token.split(".")[1]));
        const now = Math.floor(Date.now() / 1000);
        return payload.exp < now;
    } catch (e) {
        return true; // 잘못된 토큰이면 만료된 걸로 처리
    }
}

export default router;
