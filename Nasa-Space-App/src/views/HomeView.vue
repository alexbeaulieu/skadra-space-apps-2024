<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { VueDraggableNext } from 'vue-draggable-next'
import { fetchWrapper } from '@/helpers/fetch-wrapper'

const BASE_URL = 'http://127.0.0.1:5000'
const planets = ref([])
const selectedPlanet = ref(null)
const dates = ref([])
const selectedDate = ref(null)
const algorithms = ref(null)
const selectedAlgorithm = ref(null)
const filters = ref([])
const basePlot = ref(null)

const currentPage = ref(1)
const itemsPerPage = 9

const totalPages = computed(() => Math.ceil(dates.value.length / itemsPerPage))

const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  const slicedItems = dates.value.slice(start, end)
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

const updateFilterParam = (filterIndex, paramKey, newValue) => {
  filters.value[filterIndex].params[paramKey] = newValue
}

const detectInputType = (value) => {
  if (typeof value === 'number') {
    return 'number'
  } else if (Date.parse(value)) {
    return 'date'
  } else {
    return 'text'
  }
}

// Watch for changes to selectedPlanet and fetch dates
watch(selectedPlanet, async (newPlanet) => {
  if (newPlanet) {
    fetchWrapper
      .get(`${BASE_URL}/planets/${newPlanet}/dates/`)
      .then((data) => {
        dates.value = data
      })
      .catch((error) => {
        console.error('Error:', error)
      })
  }
})

// watch for changes to selectedDate and trigger a computation for that date
watch(selectedDate, async (newDate) => {
  if (newDate) {
    fetchWrapper
      .post(
        `${BASE_URL}/planets/${selectedPlanet.value}/${selectedDate.value}/${selectedAlgorithm.value.name}/`,
        filters.value // TODO : voir si ça suffit pour prendre en compte l'ordre des filtres?
      )
      .then((data) => {
        basePlot.value = data.plot_html
      })
      .catch((error) => {
        console.error('Error:', error)
      })
  }
})

const gatherApiData = () => {
  // Mettre les requêtes API ici
  fetchWrapper
    .get(`${BASE_URL}/planets/`)
    .then((data) => {
      planets.value = data
    })
    .then(() => {
      selectedPlanet.value = planets.value[0]
    })
    .catch((error) => {
      console.error('Error:', error)
    })

  fetchWrapper
    .get(`${BASE_URL}/filters/`)
    .then((data) => {
      filters.value = data
    })
    .catch((error) => {
      console.error('Error:', error)
    })

  fetchWrapper
    .get(`${BASE_URL}/algos/`)
    .then((data) => {
      algorithms.value = data
    })
    .then(() => {
      selectedAlgorithm.value = algorithms.value[0]
    })
    .catch((error) => {
      console.error('Error:', error)
    })
}

onMounted(async () => {
  await gatherApiData()
})
</script>

<template>
  <div class="d-flex justify-content-left border border-black rounded w-50">
    <div class="m-3">
      <h4>Select an astral body</h4>
      <form>
        <div v-for="planet in planets" :key="planet" class="form-check">
          <input
            type="radio"
            :id="planet"
            name="planet"
            :value="planet"
            v-model="selectedPlanet"
            class="form-check-input"
          />
          <label :for="planet" class="form-check-label">{{ planet }}</label>
        </div>
      </form>
    </div>
    <div class="m-3 d-flex flex-column align-items-center">
      <h4>Dates</h4>
      <table class="table table-bordered">
        <tbody>
          <tr v-for="(row, index) in paginatedRows" :key="index">
            <td
              v-for="(item, idx) in row"
              :key="idx"
              :class="{
                'clickable-cell': true,
                'table-primary': selectedDate === item
              }"
              @click="selectedDate = item"
            >
              {{ item || '—' }}
            </td>
          </tr>
        </tbody>
      </table>
      <!-- Pagination -->
      <nav>
        <ul class="pagination">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button
              class="page-link"
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
            >
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
            <button
              class="page-link"
              @click="changePage(currentPage + 1)"
              :disabled="currentPage === totalPages"
            >
              Next
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
  <div class="flex-container">
    <div class="data-cleaning flex-item w-full">
      <div class="flex w-full">
        <h4>Data cleaning</h4>
        <VueDraggableNext class="dragArea list-group w-full w-full" v-model="filters">
          <div
            class="list-group-item bg-gray m-1 p-3 rounded-md text-center flex items-center w-full"
            v-for="(filter, filterIndex) in filters"
            :key="filter.name"
          >
            <h6>{{ filter.name }}</h6>
            <div v-for="(value, key) in filter.params" :key="key">
              <div
                v-if="value !== null"
                class="d-flex flex-row align-items-center justify-content-lg-between w-full"
              >
                <label :for="key" class="mr-2">{{ key }}</label>
                <input
                  :type="detectInputType(value)"
                  class="form-control w-25"
                  :id="key"
                  v-model="filters[filterIndex].params[key]"
                />
              </div>
            </div>
          </div>
        </VueDraggableNext>
      </div>
    </div>
    <div class="flex-item flex-box">
      <img :src="'data:image/png;base64,' + basePlot" alt="Plot Image" v-if="basePlot" />
    </div>
  </div>

  <div class="mt-3">
    <h4>Event identification algorithm</h4>
    <div class="form-group">
      <label for="algolist" class="mb-1"> Algorithm list: </label>
      <select name="algolist" id="algolist" class="form-control w-25">
        <option v-for="algorithm in algorithms" :value="algorithm.name">
          {{ algorithm.name }}
        </option>
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

.flex-container {
  display: flex;
  height: 50vh; /* Half of the screen height */
}

.data-cleaning {
  flex: 0 0 auto; /* Take its natural width */
}

.flex-box {
  flex: 1; /* Take the remaining width */
  border: 1px solid #000; /* Optional: Add a border for visual separation */
}
</style>
