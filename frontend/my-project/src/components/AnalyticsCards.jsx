export default function AnalyticsCards({ stats }) {
    if (!stats) {
        return null
    }

    const cards = [
        { label: 'Total Products', value: stats.total_products },
        { label: 'Total Quantity', value: stats.total_quantity },
        { label: 'Inventory Value', value: `$${stats.inventory_value.toLocaleString()}` },
        { label: 'Low Stock Items', value: stats.low_stock_count },
        { label: 'Out of Stock', value: stats.out_of_stock_count },
    ]

    return (
        <section className="analytics-cards">
            {cards.map((card) => (
                <div key={card.label} className="analytics-card">
                    <span>{card.label}</span>
                    <strong>{card.value}</strong>
                </div>
            ))}
        </section>
    )
}
