import { useState } from 'react'

const defaultProduct = {
  sku: '',
  name: '',
  category: '',
  quantity: 0,
  price: 0.0,
  reorder_level: 0,
  supplier: '',
  last_restock: new Date().toISOString().slice(0, 10),
}

export default function AddProductForm({ categories, onCreate, loading, error }) {
  const [form, setForm] = useState(defaultProduct)
  const [successMessage, setSuccessMessage] = useState('')
  const [formError, setFormError] = useState('')

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((current) => ({
      ...current,
      [name]: value,
    }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setFormError('')
    setSuccessMessage('')

    if (!form.sku || !form.name || !form.category) {
      setFormError('SKU, name and category are required.')
      return
    }

    const payload = {
      sku: form.sku.trim(),
      name: form.name.trim(),
      category: form.category,
      quantity: Number(form.quantity),
      price: Number(form.price),
      reorder_level: Number(form.reorder_level),
      supplier: form.supplier.trim(),
      last_restock: form.last_restock || new Date().toISOString().slice(0, 10),
    }

    try {
      await onCreate(payload)
      setSuccessMessage('Product added successfully.')
      setForm({
        ...defaultProduct,
        category: form.category,
      })
    } catch (err) {
      setFormError(err?.message || 'Failed to add product.')
    }
  }

  const options = categories.length ? categories : ['Uncategorized']

  return (
    <section className="add-product-panel">
      <div className="add-product-header">
        <h3>Add New Product</h3>
      </div>

      <form className="add-product-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          <label>
            SKU
            <input
              name="sku"
              value={form.sku}
              onChange={handleChange}
              placeholder="ZEP101"
            />
          </label>
          <label>
            Name
            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="Fresh Milk"
            />
          </label>
          <label>
            Category
            <select name="category" value={form.category} onChange={handleChange}>
              {options.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>
          <label>
            Quantity
            <input
              name="quantity"
              type="number"
              min="0"
              value={form.quantity}
              onChange={handleChange}
            />
          </label>
          <label>
            Reorder Level
            <input
              name="reorder_level"
              type="number"
              min="0"
              value={form.reorder_level}
              onChange={handleChange}
            />
          </label>
          <label>
            Unit Price
            <input
              name="price"
              type="number"
              min="0"
              step="0.01"
              value={form.price}
              onChange={handleChange}
            />
          </label>
          <label>
            Supplier
            <input
              name="supplier"
              value={form.supplier}
              onChange={handleChange}
              placeholder="Supplier name"
            />
          </label>
          <label>
            Last Restock
            <input
              name="last_restock"
              type="date"
              value={form.last_restock}
              onChange={handleChange}
            />
          </label>
        </div>

        <div className="form-actions">
          <button type="submit" className="button-primary" disabled={loading}>
            {loading ? 'Adding…' : 'Add product'}
          </button>
          {successMessage && <span className="form-success">{successMessage}</span>}
          {(formError || error) && <span className="form-error">{formError || error}</span>}
        </div>
      </form>
    </section>
  )
}
