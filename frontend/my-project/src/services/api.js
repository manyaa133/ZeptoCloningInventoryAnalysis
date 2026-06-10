import axios from 'axios'

const rawBase = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
const API_BASE_URL = rawBase.replace(/\/$/, '')

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 12000,
})

// Helpful logging for debugging network issues in development
api.interceptors.request.use((config) => {
    // eslint-disable-next-line no-console
    console.info('[api] Request', config.method?.toUpperCase(), config.baseURL + config.url)
    return config
})

api.interceptors.response.use(
    (response) => {
        // eslint-disable-next-line no-console
        console.info('[api] Response', response.status, response.config.url)
        return response
    },
    (error) => {
        // Normalize error messages so UI can display something helpful
        if (error.response) {
            // Server responded with a status outside 2xx
            const msg = `HTTP ${error.response.status} ${error.response.statusText} - ${error.config?.url}`
            // eslint-disable-next-line no-console
            console.error('[api] Response error', msg, error.response.data)
            return Promise.reject(new Error(msg))
        }

        if (error.request) {
            // Request made but no response received
            // eslint-disable-next-line no-console
            console.error('[api] No response received', error.config?.url, error.message)
            return Promise.reject(new Error('No response from server'))
        }

        // Something happened setting up the request
        // eslint-disable-next-line no-console
        console.error('[api] Request setup error', error.message)
        return Promise.reject(new Error(error.message || 'Network Error'))
    }
)

export function getInventory(search = '', category = 'All') {
    const params = {}

    if (search) params.search = search
    if (category && category !== 'All') params.category = category

    return api.get('/inventory', { params }).then((response) => response.data)
}

export function getInventoryStats() {
    return api.get('/inventory/stats').then((response) => response.data)
}

export function getCategoryDistribution() {
    return api.get('/inventory/categories').then((response) => response.data)
}

export function getLowStockItems() {
    return api.get('/inventory/low-stock').then((response) => response.data)
}

export function createInventoryItem(item) {
    return api.post('/inventory', item).then((response) => response.data)
}
