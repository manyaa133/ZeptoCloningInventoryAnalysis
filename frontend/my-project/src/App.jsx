import { useState } from 'react'
import './App.css'
import AnalyticsCards from './components/AnalyticsCards'
import AddProductForm from './components/AddProductForm'
import ChartPanel from './components/ChartPanel'
import InventoryTable from './components/InventoryTable'
import LoadingSkeleton from './components/LoadingSkeleton'
import SearchBar from './components/SearchBar'
import useInventory from './hooks/useInventory'

function App() {
  const [showAddForm, setShowAddForm] = useState(false)

  const {
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
  } = useInventory()

  return (
    <div className="app-shell">
      <header className="page-header">
        <div>
          <span className="section-label">Zepto Inventory Analytics</span>
          <h1>Modern inventory insights for your store</h1>
          <p className="page-subtitle">
            Track stock health, category distribution, and real inventory value in a single dashboard.
          </p>
        </div>
      </header>

      <section className="top-row">
        <div className="search-actions-row">
          <SearchBar
            search={search}
            category={selectedCategory}
            categories={categories}
            onSearch={setSearch}
            onCategoryChange={setSelectedCategory}
          />
          <div className="add-product-action">
            <button type="button" onClick={() => setShowAddForm((current) => !current)}>
              {showAddForm ? 'Hide add product' : 'Add product'}
            </button>
          </div>
        </div>
        {showAddForm && (
          <AddProductForm
            categories={categories.filter((category) => category !== 'All')}
            onCreate={createProduct}
            loading={submitting}
            error={submitError}
          />
        )}
      </section>

      {loading ? (
        <LoadingSkeleton />
      ) : error ? (
        <div className="status-message status-error">{error}</div>
      ) : (
        <>
          <AnalyticsCards stats={stats} />

          <section className="dashboard-grid">
            <ChartPanel
              categoryDistribution={categoryDistribution}
              valueByCategory={valueByCategory}
            />

            <InventoryTable items={filteredItems} />
          </section>
        </>
      )}
    </div>
  )
}

export default App
