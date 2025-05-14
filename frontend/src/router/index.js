import { createRouter, createWebHistory } from "vue-router";
import MainLayout from "@/layouts/MainLayout.vue";
import EditCompanies from "@/views/EditCompanies.vue";
import Monitoring from "@/views/Monitoring.vue";
// import AdminMenu from "@/views/AdminMenu.vue";

const routes = [
    {
        path: "/",
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

export default router;
