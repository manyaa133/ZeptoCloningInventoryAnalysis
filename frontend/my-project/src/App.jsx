import './App.css'
import AnalyticsCards from './components/AnalyticsCards'
import ChartPanel from './components/ChartPanel'
import InventoryTable from './components/InventoryTable'
import LoadingSkeleton from './components/LoadingSkeleton'
import SearchBar from './components/SearchBar'
import useInventory from './hooks/useInventory'

function App() {
  const {
    categories,
    filteredItems,
    loading,
    error,
    search,
    selectedCategory,
    stats,
    categoryDistribution,
    valueByCategory,
    setSearch,
    setSelectedCategory,
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
        <SearchBar
          search={search}
          category={selectedCategory}
          categories={categories}
          onSearch={setSearch}
          onCategoryChange={setSelectedCategory}
        />
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
