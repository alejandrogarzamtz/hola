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

  return (
    <div style={{ padding: '1rem', fontFamily: 'Arial, sans-serif' }}>
      <h2>Supplier for the Purchase Order</h2>

      {loading && (
        <p>Loading suppliers...</p>
      )}

      {error && (
        <p style={{ color: 'red' }}>Error loading suppliers</p>
      )}

      {!loading && !error && (
        <div style={{ border: '1px solid #ccc', borderRadius: '6px', maxHeight: '300px', overflowY: 'auto', marginTop: '1rem' }}>
          {suppliers.map((s, i) => (
            <div key={i} style={{ padding: '8px 16px', borderBottom: '1px solid #eee' }}>
              {`${s.vendor} ${s.name}`}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}






