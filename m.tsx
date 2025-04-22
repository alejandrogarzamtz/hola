import { useEffect, useState } from 'react'
import axios from 'axios'

interface SupplierOption {
  vendor: string
  name: string
}

interface StrategyDetails {
  strategy_title: string
  strategy_description: string
  purchase_profile: string
}

export const SupplierStrategyTest = () => {
  const [suppliers, setSuppliers] = useState<SupplierOption[]>([])
  const [filteredSuppliers, setFilteredSuppliers] = useState<SupplierOption[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const [query, setQuery] = useState('')
  const [details, setDetails] = useState<StrategyDetails | null>(null)

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
      s.vendor.toLowerCase().includes(query.toLowerCase()) ||
      s.name.toLowerCase().includes(query.toLowerCase())
    )
    setFilteredSuppliers(filtered)
  }, [query, suppliers])

  const handleSelect = (vendor: string) => {
    axios.get(`http://localhost:8080/api/supplier_strategy_details?vendor=${vendor}`)
      .then(res => setDetails(res.data))
      .catch(err => {
        console.error('Error fetching strategy details:', err)
        setDetails(null)
      })
  }

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
              borderRadius: '4px'
            }}
          />
          <div
            style={{
              border: '1px solid #ccc',
              borderRadius: '4px',
              maxHeight: '300px',
              overflowY: filteredSuppliers.length > 6 ? 'scroll' : 'auto'
            }}
          >
            {filteredSuppliers.map((s, i) => (
              <div
                key={i}
                style={{
                  padding: '8px',
                  borderBottom: '1px solid #eee',
                  cursor: 'pointer'
                }}
                onClick={() => handleSelect(s.vendor)}
              >
                {`${s.vendor} ${s.name}`}
              </div>
            ))}
          </div>
        </>
      )}

      {details && (
        <>
          <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #007bff', borderRadius: '6px' }}>
            <h3>Strategy Profile</h3>
            <p><strong>Title:</strong> {details.strategy_title}</p>
            <p><strong>Description:</strong> {details.strategy_description}</p>
          </div>

          <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #28a745', borderRadius: '6px' }}>
            <h3>Purchase Profile</h3>
            <p>{details.purchase_profile}</p>
          </div>
        </>
      )}
    </div>
  )
}
