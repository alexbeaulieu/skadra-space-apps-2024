<script setup>
import { ref, computed, onMounted } from 'vue'
import { VueDraggableNext } from 'vue-draggable-next'
import { fetchWrapper } from '@/helpers/fetch-wrapper';


const currentPage = ref(1)
const itemsPerPage = 9
const items = [
  '2024-01-01',
  '2024-01-02',
  '2024-01-03',
  '2024-01-04',
  '2024-01-05',
  '2024-01-06',
  '2024-01-07',
  '2024-01-08',
  '2024-01-09',
  '2024-01-10',
  '2024-01-11',
  '2024-01-12'
]
const dico_filter_fully_filled = {
  filter: {
    up_number: 100,
    down_number: 0,
    bool: true,
    string: 'asd'
  }
}

const dico_filter_partially_filled = {
  filter2: {
    up_number: '',
    down_number: null,
    bool: true,
    string: null
  }
}

const dico_filter_not_filled = {
  filter3: {
    up_number: null,
    down_number: null,
    bool: null,
    string: null
  }
}

const list = ref([
  { name: dico_filter_fully_filled, id: 1 },
  { name: dico_filter_partially_filled, id: 2 },
  { name: dico_filter_not_filled, id: 3 }
])

const totalPages = computed(() => Math.ceil(items.length / itemsPerPage))

const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  const slicedItems = items.slice(start, end)
  const rows = []
  
  for (let i = 0; i < slicedItems.length; i += 3) {
    rows.push(slicedItems.slice(i, i + 3))
  }

  if (rows.length && rows[rows.length - 1].length < 3) {
    while (rows[rows.length - 1].length < 3) {
      rows[rows.length - 1].push(null) 
    }
  }

  return rows
})

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const test = (item) => {
  console.log('test', item)
}

const gatherApiData = () => {
  // Mettre les requêtes API ici
}


onMounted(async () => {
  gatherApiData()
})
</script>

<template>
  <div class="d-flex justify-content-left border border-black rounded w-50">
    <div class="m-3">
      <h4>Select a Planet</h4>
      <form>
        <div class="form-check">
          <input
            type="radio"
            id="mars"
            name="planet"
            value="Mars"
            v-model="selectedPlanet"
            class="form-check-input"
          />
          <label for="mars" class="form-check-label">Mars 👽</label>
        </div>

        <div class="form-check">
          <input
            type="radio"
            id="moon"
            name="planet"
            value="Moon"
            v-model="selectedPlanet"
            class="form-check-input"
          />
          <label for="moon" class="form-check-label">Moon 🌘</label>
        </div>
      </form>
    </div>
    <div class="m-3 d-flex flex-column align-items-center">
      <h4>Dates</h4>
      <table class="table table-bordered">
        <tbody>
          <tr v-for="(row, index) in paginatedRows" :key="index">
            <td v-for="(item, idx) in row" :key="idx" class="clickable-cell"  @click="test(item)">{{ item || '—' }}</td>
          </tr>
        </tbody>
      </table>
      <!-- Pagination -->
      <nav>
        <ul class="pagination">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="changePage(currentPage - 1)" :disabled="currentPage === 1">
              Previous
            </button>
          </li>

          <li
            class="page-item"
            v-for="page in totalPages"
            :key="page"
            :class="{ active: currentPage === page }"
          >
            <button class="page-link" @click="changePage(page)">{{ page }}</button>
          </li>

          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <button class="page-link" @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">
              Next
            </button>
          </li>
        </ul>
      </nav>

   


   
    </div>
  </div>
  <div class="flex m-10">
    <h4>Filters</h4>
    <VueDraggableNext class="dragArea list-group w-full w-25" :list="list">
      <div
        class="list-group-item bg-gray m-1 p-3 rounded-md text-center flex items-center"
        v-for="element in list"
        :key="element.id"
      >
        <div v-for="(value, key) in element.name" :key="key">
          <div>
            <h6>{{ key }}</h6>
            <!-- <input type="checkbox" class="mr-2" /> -->
          </div>

          <div v-if="value.up_number !== null" class="d-flex flex-column align-items-center">
            <label for="up_number" class="mr-2">Up number:</label>
            <input type="number" class="form-control w-25" :value="value.up_number" />
          </div>
          <div v-if="value.down_number !== null" class="d-flex flex-column align-items-center">
            <label for="down_number" class="mr-2">Down number:</label>
            <input type="number" class="form-control w-25" :value="value.down_number" />
          </div>
          <div v-if="value.bool !== null">
            <label for="bool" class="mr-2">Bool:</label>
            <input type="checkbox" class="form-check-input m-1" :checked="value.bool" />
          </div>
        </div>
      </div>
    </VueDraggableNext>
  </div>
  <div class="mt-3">
    <h4>Algorithms</h4>
    <div class="form-group">
      <label for="algolist" class="mb-1"> Algorithm list: </label>
      <select name="algolist" id="algolist" class="form-control w-25">
        <option value="algo1">algo1</option>
        <option value="algo2">algo2</option>
        <option value="algo3">algo3</option>
        <option value="algo4">algo4</option>
      </select>
    </div>
  </div>
</template>

<style scoped>
.clickable-cell {
  cursor: pointer;
  transition: background-color 0.3s;
}

.clickable-cell:hover {
  background-color: rgb(222, 222, 222);
}
</style>
