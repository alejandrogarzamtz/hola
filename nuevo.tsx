import { useEffect, useState } from 'react'
import axios from 'axios'

interface SupplierOption {
  vendor: string
  name: string
}

export const SupplierStrategyTest = () => {
  const [suppliers, setSuppliers] = useState<SupplierOption[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const [query, setQuery] = useState('')

  useEffect(() => {
    axios.get('http://localhost:8080/api/suppliers')
      .then(res => {
        setSuppliers(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error loading suppliers:', err)
        setError(true)
        setLoading(false)
      })
  }, [])

  const filteredSuppliers = suppliers.filter(s => {
    return (
      s.vendor.toLowerCase().includes(query.toLowerCase()) ||
      (s.name || '').toLowerCase().includes(query.toLowerCase())
    )
  })

  return (
    <div style={{ padding: '1rem', fontFamily: 'Arial, sans-serif' }}>
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
            style={{ padding: '0.5rem', marginBottom: '1rem', width: '100%' }}
          />

          <div style={{ border: '1px solid #ccc', borderRadius: '4px', maxHeight: '300px', overflowY: 'scroll' }}>
            {filteredSuppliers.map((s, i) => (
              <div key={i} style={{ padding: '0.5rem', borderBottom: '1px solid #eee' }}>
                {`${s.vendor} ${s.name}`}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
