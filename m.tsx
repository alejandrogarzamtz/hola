import { useEffect, useState } from 'react'
import axios from 'axios'

interface SupplierOption {
  vendor: string
  name: string
}

interface SupplierProfile {
  strategy_title: string
  strategy_description: string
  short_texts: string[]
}

export const SupplierStrategyTest = () => {
  const [suppliers, setSuppliers] = useState<SupplierOption[]>([])
  const [filteredSuppliers, setFilteredSuppliers] = useState<SupplierOption[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const [query, setQuery] = useState('')
  const [profile, setProfile] = useState<SupplierProfile | null>(null)

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
    axios.get(`http://localhost:8080/api/supplier_profile?vendor=${vendor}`)
      .then(res => setProfile(res.data))
      .catch(err => console.error('Error fetching profile:', err))
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
            style={{ padding: '8px', marginBottom: '10px', width: '100%', border: '1px solid #ccc', borderRadius: '4px' }}
          />

          <div style={{
            border: '1px solid #ccc',
            borderRadius: '4px',
            maxHeight: '300px',
            overflowY: filteredSuppliers.length > 6 ? 'scroll' : 'hidden'
          }}>
            {filteredSuppliers.map((s, i) => (
              <div
                key={i}
                style={{ padding: '8px', borderBottom: '1px solid #eee', cursor: 'pointer' }}
                onClick={() => handleSelect(s.vendor)}
              >
                {`${s.vendor} ${s.name}`}
              </div>
            ))}
          </div>
        </>
      )}

      {profile && (
        <>
          <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #aaa' }}>
            <h3>Strategy Profile</h3>
            <p><strong>{profile.strategy_title}</strong></p>
            <p>{profile.strategy_description}</p>
          </div>

          <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #aaa' }}>
            <h3>Purchase Profile</h3>
            <ul>
              {profile.short_texts.map((text, i) => (
                <li key={i}>{text}</li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  )
}
