import { useEffect, useState } from 'react'
import axios from 'axios'

interface SupplierOption {
  vendor: string
  name: string
}

export const SupplierStrategyTest = () => {
  const [suppliers, setSuppliers] = useState<SupplierOption[]>([])
  const [filteredSuppliers, setFilteredSuppliers] = useState<SupplierOption[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const [query, setQuery] = useState('')

  useEffect(() => {
    axios.get('http://localhost:8080/api/supplierss')
      .then(res => {
        setSuppliers(res.data)
        setFilteredSuppliers(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error loading suppliers:', err)
        setError(true)
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    const filtered = suppliers.filter(s =>
      (s.vendor?.toLowerCase() || '').includes(query.toLowerCase()) ||
      (s.name?.toLowerCase() || '').includes(query.toLowerCase())
    )
    setFilteredSuppliers(filtered)
  }, [query, suppliers])

  return (
    <div style={{ padding: '20px' }}>
      <h2>Supplier for the Purchase Order</h2>

      {loading && <p>Loading suppliers...</p>}
      {error && <p style={{ color: 'red' }}>Error loading suppliers</p>}

      {!loading && !error && (
        <>
          <input
            type="text"
            placeholder="Search by vendor or name..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{
              padding: '8px',
              marginBottom: '10px',
              width: '100%',
              border: '1px solid #ccc',
              borderRadius: '4px',
              outline: 'none',
              boxSizing: 'border-box'
            }}
          />
          <div
            style={{
              border: '1px solid #ccc',
              borderRadius: '4px',
              maxHeight: '300px',
              overflowY: filteredSuppliers.length > 8 ? 'auto' : 'hidden'
            }}
          >
            {filteredSuppliers.map((s, i) => (
              <div key={i} style={{ padding: '8px', borderBottom: '1px solid #eee' }}>
                {`${s.vendor} ${s.name}`}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
