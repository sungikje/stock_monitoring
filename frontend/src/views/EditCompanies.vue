<template>
    <div class="edit-companies">
      <div class="company-list-section"> <div class="section-header"> <h1>📋 관심 회사 목록</h1>
          <button @click="generateGraph" class="generate-graph-button">📈 그래프 생성</button> </div>
  
        <p v-if="favoriteCompanies.length === 0">관심 회사가 없습니다.</p>
        <table v-else class="company-table">
          <thead>
            <tr>
              <th>Index</th>
              <th>회사명</th>
              <th>추가 일자</th>
              <th>관찰 기간</th>
              <th>관리</th>
            </tr>
          </thead>
          <tbody v-if="favoriteCompanies.length != 0">
            <tr v-for="(company, index) in favoriteCompanies" :key="index">
              <td>{{ index }}</td>
              <td>{{ company.company_name }}</td>
              <td>{{ filter_date(company.created_at) }}</td>
              <td>{{ company.industry_period }}</td>
              <td>
                <button @click="editCompany(company)">✏ 수정</button>
                <button @click="deleteCompany(company.company_name)">
                  🗑 삭제
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div> <br /><br /><br />
      <h1>📋 관심 회사 검색</h1>
      <div class="search-section">
        <input v-model="companyName" type="text" placeholder="회사명 검색" />
        <button type="" @click="searchCompany">🔍 검색</button>
        <button type="" @click="addCompany">➕ 추가</button>
      </div>
  
      <p v-if="searchResults.length === 0">관심 회사가 없습니다.</p>
      <table v-else class="search-table">
        <thead>
          <tr>
            <th>✔</th>
            <th>Code</th>
            <th>Unique Code</th>
            <th>회사명</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in searchResults" :key="result.code">
            <td>
              <input
                type="checkbox"
                v-model="selectedResults"
                :value="result.name"
              />
            </td>
            <td>{{ result.code }}</td>
            <td>{{ result.market }}</td>
            <td>{{ result.name }}</td>
          </tr>
        </tbody>
      </table>
  
      <ConfirmDeleteModal
        v-if="showDeleteModal"
        :companyName="selectedCompanyName"
        @confirm="confirmDelete"
        @close="showDeleteModal = false"
      />
  
      <EditCompanyModal
        v-if="showEditModal"
        :company="selectedCompany"
        @confirm="confirmEdit"
        @close="showEditModal = false"
      />
    </div>
  </template>

<script>
import axios from "axios";

import ConfirmDeleteModal from "@/modal/ConfirmDeleteModal.vue";
import EditCompanyModal from "@/modal/EditCompanyModal.vue";

export default {
  components: {
    ConfirmDeleteModal,
    EditCompanyModal,
  },
  data() {
    return {
      companyName: "",
      companies: [],
      favoriteCompanies: [],
      searchResults: [],
      selectedResults: [],
      showDeleteModal: false,
      showEditModal: false,
      selectedCompanyName: "",
      selectedCompany: null,
    };
  },
  methods: {
    async searchCompany() {
        console.log("sibal");
      try {
        const access_token = localStorage.getItem("access_token");
        const res = await axios.post(
          "http://localhost:8000/api/search_company",
          { company_name: this.companyName },
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          },
        );
        if (res.data.status != "error") {
          this.searchResults = res.data;
        } else {
          this.searchResults = [];
        }
      } catch (error) {
        console.error("Request failed:", error);
        this.errorMessage = error.message || "Request failed";
      }
    },

    async searchFavoriteCompany() {
      try {
        const access_token = localStorage.getItem("access_token");
        const res = await axios.post(
          "http://localhost:8000/api/search_favorite_company",
          {},
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          },
        );
        this.favoriteCompanies = res.data;
      } catch (error) {
        console.error("Request failed:", error);
        this.errorMessage = error.message || "Request failed";
      }
    },

    async addCompany() {
      const payload = {
        company_list: this.selectedResults.map((name) => ({
          company_name: name,
        })),
      };

      try {
        const access_token = localStorage.getItem("access_token");
        const res = await axios.post(
          "http://localhost:8000/api/create_favorite_company",
          payload,
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          },
        );
        this.favoriteCompanies = res.data;
        this.$router.go(0);
      } catch (error) {
        console.error("Request failed:", error);
        this.errorMessage = error.message || "Request failed";
      }
    },
    editCompany(company) {
      this.selectedCompany = company;
      this.showEditModal = true;
    },

    async confirmEdit(updatedInfo) {
      try {
        const access_token = localStorage.getItem("access_token");
        const res = await axios.post(
          "http://localhost:8000/api/update_favorite_company_industry_period",
          updatedInfo,
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          },
        );
        this.showEditModal = false;
        this.searchFavoriteCompany(); // 최신 데이터 반영
      } catch (error) {
        console.error("Edit failed:", error);
      }
    },

    deleteCompany(company_name) {
      this.selectedCompanyName = company_name;
      this.showDeleteModal = true;
    },

    async confirmDelete() {
      try {
        const access_token = localStorage.getItem("access_token");
        const res = await axios.post(
          "http://localhost:8000/api/delete_favorite_company",
          { company_name: this.selectedCompanyName },
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          },
        );
        this.showDeleteModal = false;
        this.searchFavoriteCompany();
      } catch (error) {
        console.error("Delete failed:", error);
      }
    },

    async generateGraph() {
        try {
            const res = await axios.post(
                "http://localhost:8000/api/make_stock_monitoring_chart"
            );
            console.log("success request")
        } catch (error) {
            console.error("Delete failed:", error);
        }
    },

    filter_date(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = date.getMonth() + 1; // 0부터 시작하므로 +1
      const day = date.getDate();

      return `${year}년 ${month}월 ${day}일`;
    },
  },

  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.searchFavoriteCompany();
    });
  },
};
</script>

<style scoped>
.edit-companies {
  padding: 20px;
}

h1 {
  color: #34495e;
  margin-bottom: 20px;
  font-size: 24px;
  display: flex; /* ⭐ 제목과 버튼을 같은 줄에 놓기 위해 flex 적용 */
  align-items: center; /* ⭐ 세로 중앙 정렬 */
  justify-content: space-between; /* ⭐ 양쪽 끝 정렬 (제목-버튼) */
}

/* ⭐ 제목과 버튼을 감싸는 div에 대한 스타일 */
.section-header {
  display: flex;
  justify-content: space-between; /* 제목과 버튼을 양쪽 끝으로 */
  align-items: center; /* 세로 중앙 정렬 */
  margin-bottom: 20px;
}

.section-header h1 {
  margin: 0; /* h1의 기본 마진 제거 */
}

.generate-graph-button { /* ⭐ 그래프 생성 버튼 스타일 */
  background-color: #28a745; /* 녹색 */
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.generate-graph-button:hover {
  background-color: #218838;
}


/* 테이블 공통 스타일 */
.company-table,
.search-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.company-table th,
.search-table th {
  background-color: #f2f2f2;
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
  font-weight: bold;
  color: #333;
}

.company-table td,
.search-table td {
  padding: 10px 15px;
  border-bottom: 1px solid #eee;
  color: #555;
}

.company-table tr:hover,
.search-table tr:hover {
  background-color: #f9f9f9;
}

/* 테이블 내 버튼 */
.company-table td button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.company-table td button:hover {
  background-color: #0056b3;
}

.company-table td button:last-child {
  background-color: #dc3545; /* 삭제 버튼 색상 */
}

.company-table td button:last-child:hover {
  background-color: #c82333;
}

/* 검색 섹션 */
.search-section {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.search-section input[type="text"] {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.search-section button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.search-section button:hover {
  background-color: #0056b3;
}

.search-section button:last-child {
  background-color: #28a745; /* 추가 버튼 색상 */
}

.search-section button:last-child:hover {
  background-color: #218838;
}

/* 체크박스 스타일 */
.search-table input[type="checkbox"] {
  transform: scale(1.2); /* 체크박스 크기 조절 */
}
</style>
