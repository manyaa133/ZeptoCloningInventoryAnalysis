function getStatus(item) {
    if (item.quantity === 0) {
        return { label: 'Out of stock', status: 'danger' }
    }

    if (item.quantity <= item.reorder_level) {
        return { label: 'Low stock', status: 'warning' }
    }

    return { label: 'In stock', status: 'success' }
}

export default function InventoryTable({ items }) {
    return (
        <section className="inventory-panel">
            <div className="inventory-panel-header">
                <h3>Inventory Table</h3>
                <span>{items.length} products</span>
            </div>
            <div className="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>SKU</th>
                            <th>Name</th>
                            <th>Category</th>
                            <th>Quantity</th>
                            <th>Reorder Level</th>
                            <th>Unit Price</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items.map((item) => {
                            const status = getStatus(item)

                            return (
                                <tr key={item.id}>
                                    <td>{item.sku}</td>
                                    <td>{item.name}</td>
                                    <td>{item.category}</td>
                                    <td>{item.quantity}</td>
                                    <td>{item.reorder_level}</td>
                                    <td>${item.price.toFixed(2)}</td>
                                    <td>
                                        <span className={`badge badge-${status.status}`}>
                                            {status.label}
                                        </span>
                                    </td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        </section>
    )
}
