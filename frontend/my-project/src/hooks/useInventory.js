import { useEffect, useMemo, useState } from 'react'
import {
    createInventoryItem,
    getCategoryDistribution,
    getInventory,
    getInventoryStats,
} from '../services/api'

const DEFAULT_CATEGORY = 'All'

export default function useInventory() {
    const [items, setItems] = useState([])
    const [stats, setStats] = useState(null)
    const [categoryDistribution, setCategoryDistribution] = useState([])
    const [selectedCategory, setSelectedCategory] = useState(DEFAULT_CATEGORY)
    const [search, setSearch] = useState('')
    const [loading, setLoading] = useState(true)
    const [submitting, setSubmitting] = useState(false)
    const [error, setError] = useState(null)
    const [submitError, setSubmitError] = useState(null)

    async function loadData() {
        setLoading(true)
        setError(null)

        try {
            const [inventoryData, statsData, distributionData] = await Promise.all([
                getInventory(),
                getInventoryStats(),
                getCategoryDistribution(),
            ])

            setItems(inventoryData)
            setStats(statsData)
            setCategoryDistribution(distributionData)
        } catch (err) {
            console.error('Failed to fetch inventory data', err)
            setError(err?.message || 'Unable to load inventory data')
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        loadData()
    }, [])

    const filteredItems = useMemo(() => {
        return items.filter((item) => {
            const searchTerm = search.trim().toLowerCase()
            const searchMatch =
                !searchTerm ||
                item.name.toLowerCase().includes(searchTerm) ||
                item.sku.toLowerCase().includes(searchTerm) ||
                item.category.toLowerCase().includes(searchTerm)

            const categoryMatch =
                selectedCategory === DEFAULT_CATEGORY ||
                item.category === selectedCategory

            return searchMatch && categoryMatch
        })
    }, [items, search, selectedCategory])

    const categories = useMemo(() => {
        const categoryNames = categoryDistribution.map((item) => item.category)
        return [DEFAULT_CATEGORY, ...categoryNames]
    }, [categoryDistribution])

    const valueByCategory = useMemo(() => {
        const map = {}

        items.forEach((item) => {
            map[item.category] = (map[item.category] || 0) + item.quantity * item.price
        })

        return Object.entries(map).map(([category, value]) => ({
            category,
            value: Math.round(value * 100) / 100,
        }))
    }, [items])

    async function createProduct(product) {
        setSubmitting(true)
        setSubmitError(null)

        try {
            await createInventoryItem(product)
            await loadData()
        } catch (err) {
            console.error('Failed to create inventory item', err)
            const message = err?.message || 'Unable to add product'
            setSubmitError(message)
            throw new Error(message)
        } finally {
            setSubmitting(false)
        }
    }

    return {
        categories,
        filteredItems,
        loading,
        submitting,
        error,
        submitError,
        search,
        selectedCategory,
        stats,
        categoryDistribution,
        valueByCategory,
        setSearch,
        setSelectedCategory,
        createProduct,
    }
}
