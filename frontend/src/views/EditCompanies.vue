<template>
  <div class="edit-companies">
    <h1>📋 관심 회사 목록</h1>

    <!-- 관심 회사 테이블 -->
    <table class="company-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Unique Code</th>
          <th>회사명</th>
          <th>추가 일자</th>
          <th>관리</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="company in companies" :key="company.id">
          <td>{{ company.id }}</td>
          <td>{{ company.uniqueCode }}</td>
          <td>{{ company.name }}</td>
          <td>{{ company.addedDate }}</td>
          <td>
            <button @click="editCompany(company)">✏ 수정</button>
            <button @click="deleteCompany(company.id)">🗑 삭제</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 검색 기능 -->
    <div class="search-section">
      <input v-model="searchQuery" type="text" placeholder="회사명 검색" />
      <button @click="searchCompany">🔍 검색</button>
      <button @click="addCompany">➕ 추가</button>
    </div>

    <!-- 검색 결과 테이블 -->
    <!-- <table class="search-table" v-if="searchResults.length > 0"> -->
    <table class="search-table">
      <thead>
        <tr>
          <th>✔</th>
          <th>ID</th>
          <th>Unique Code</th>
          <th>회사명</th>
          <th>추가 일자</th>
        </tr>
      </thead>
      <tbody>
        <!-- <tr v-for="result in searchResults" :key="result.id">
          <td><input type="checkbox" v-model="selectedResults" :value="result.id" /></td>
          <td>{{ result.id }}</td>
          <td>{{ result.uniqueCode }}</td>
          <td>{{ result.name }}</td>
          <td>{{ result.addedDate }}</td>
        </tr> -->
        <tr>
          <td><input type="checkbox" /></td>
          <td>2</td>
          <td>123</td>
          <td>대우 전자</td>
          <td>1972.01.11</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
      companies: [
        {
          id: 1,
          uniqueCode: "ABC123",
          name: "삼성전자",
          addedDate: "2024-04-01",
        },
        {
          id: 2,
          uniqueCode: "XYZ789",
          name: "현대자동차",
          addedDate: "2024-04-02",
        },
      ],
      searchResults: [],
      selectedResults: [],
    };
  },
  methods: {
    searchCompany() {
      this.searchResults = this.companies.filter((c) =>
        c.name.includes(this.searchQuery),
      );
    },
    addCompany() {
      console.log("추가 버튼 클릭됨!");
    },
    editCompany(company) {
      console.log("수정:", company);
    },
    deleteCompany(id) {
      console.log("삭제:", id);
      this.companies = this.companies.filter((c) => c.id !== id);
    },
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
