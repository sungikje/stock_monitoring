<template>
  <div class="edit-companies">
    <h1>📋 관심 회사 목록</h1>

    <p v-if="favoriteCompanies.length === 0">관심 회사가 없습니다.</p>
    <!-- 관심 회사 테이블 -->
    <table v-else class="company-table">
      <thead>
        <tr>
            <th>Index</th>
          <th>회사명</th>
          <th>추가 일자</th>
          <th>관리</th>
        </tr>
      </thead>
      <tbody v-if="favoriteCompanies.length != 0">
        <tr v-for="(company, index) in favoriteCompanies" :key="index">
          <td>{{ index }}</td>
          <td>{{ company.company_name }}</td>
          <td>{{ filter_date(company.created_at) }}</td>
          <td>
            <button @click="editCompany(company)">✏ 수정</button>
            <button @click="deleteCompany(company.uniqueCode)">🗑 삭제</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 검색 기능 -->
    <br><br><br>
    <h1>📋 관심 회사 검색</h1>
    <div class="search-section">
      <input v-model="companyName" type="text" placeholder="회사명 검색" />
      <button type="" @click="searchCompany">🔍 검색</button>
      <button type="" @click="addCompany">➕ 추가</button>
    </div>

    <!-- 검색 결과 테이블 -->
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
          <td><input type="checkbox" v-model="selectedResults" :value="result.name" /></td>
          <td>{{ result.code }}</td>
          <td>{{ result.market }}</td>
          <td>{{ result.name }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
        companyName: "",
      companies: [],
      favoriteCompanies: [],
      searchResults: [],
      selectedResults: [],
    };
  },
  methods: {
    async searchCompany() {
        try {
            const access_token = localStorage.getItem("access_token");
            const res = await axios.post(
                "http://localhost:8000/api/search_company",
                { company_name: this.companyName },
                {
                    headers: {
                        Authorization: `Bearer ${access_token}`,
                    },
                });
            this.searchResults = res.data;
        } catch (error) {
            console.error('Request failed:', error);
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
        });
        this.favoriteCompanies = res.data;
      } catch (error) {
        console.error('Request failed:', error);
        this.errorMessage = error.message || "Request failed";
      }
    },

    async addCompany() {
        const payload = {
        company_list: this.selectedResults.map(name => ({
            company_name: name
            }))
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
            });
            this.favoriteCompanies = res.data;
            this.$router.go(0);
        } catch (error) {
            console.error('Request failed:', error);
            this.errorMessage = error.message || "Request failed";
      }
    },
    editCompany(company) {
      console.log("수정:", company);
    },
    deleteCompany(id) {
      console.log("삭제:", id);
      this.companies = this.companies.filter((c) => c.id !== id);
    },

    filter_date(dateString) {
        const date = new Date(dateString);
        const year = date.getFullYear();
        const month = date.getMonth() + 1; // 0부터 시작하므로 +1
        const day = date.getDate();

        return `${year}년 ${month}월 ${day}일`;
    }
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

/* 테이블 스타일 */
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

th {
  background-color: #f4f4f4;
}

/* 버튼 스타일 */
button {
  margin: 5px;
  padding: 5px 10px;
  border: none;
  cursor: pointer;
}

button:hover {
  opacity: 0.8;
}

/* 검색 입력 & 버튼 */
.search-section {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-section input {
  flex: 1;
  padding: 8px;
}
</style>
