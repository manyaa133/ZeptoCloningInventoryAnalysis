export default function SearchBar({ search, category, categories, onSearch, onCategoryChange }) {
    return (
        <div className="search-panel">
            <div className="search-group">
                <label htmlFor="inventory-search">Search</label>
                <input
                    id="inventory-search"
                    value={search}
                    onChange={(event) => onSearch(event.target.value)}
                    placeholder="Search by SKU, item, or category"
                />
            </div>
            <div className="search-group">
                <label htmlFor="category-select">Category</label>
                <select
                    id="category-select"
                    value={category}
                    onChange={(event) => onCategoryChange(event.target.value)}
                >
                    {categories.map((option) => (
                        <option key={option} value={option}>
                            {option}
                        </option>
                    ))}
                </select>
            </div>
        </div>
    )
}
