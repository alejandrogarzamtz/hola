import { useEffect, useState } from 'react'
import axios from 'axios'

interface SupplierOption {
  vendor: string
  name: string
}

interface SupplierDetails {
  strategy_title: string
  strategy_description: string
  purchase_profile: string
  strategy_id: string
}

export const SupplierStrategyTest = () => {
  const [suppliers, setSuppliers] = useState<SupplierOption[]>([])
  const [filteredSuppliers, setFilteredSuppliers] = useState<SupplierOption[]>([])
  const [selectedSupplier, setSelectedSupplier] = useState<SupplierOption | null>(null)
  const [details, setDetails] = useState<SupplierDetails | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const [query, setQuery] = useState('')
  const [loadingDetails, setLoadingDetails] = useState(false)

  useEffect(() => {
    axios.get('http://localhost:8080/api/supplierss')
      .then(res => {
        setSuppliers(res.data)
        setFilteredSuppliers(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error('❌ Error loading suppliers:', err)
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
    if (query.length > 0) setSelectedSupplier(null)
  }, [query, suppliers])

  const handleSelect = (supplier: SupplierOption) => {
    setSelectedSupplier(supplier)
    setQuery('')
    setLoadingDetails(true)
    setDetails(null)

    axios.get(`http://localhost:8080/api/supplier_strategy_details?vendor=${supplier.vendor}`)
      .then(res => {
        console.log("🔍 Detalles recibidos:", res.data)
        setDetails(res.data)
        setLoadingDetails(false)
      })
      .catch(err => {
        console.error('❌ Error fetching details:', err)
        setLoadingDetails(false)
      })
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
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

          {!selectedSupplier && filteredSuppliers.length > 0 && (
            <div style={{ border: '1px solid #ccc', borderRadius: '4px', maxHeight: '300px', overflowY: filteredSuppliers.length > 6 ? 'scroll' : 'auto' }}>
              {filteredSuppliers.map((s, i) => (
                <div
                  key={i}
                  onClick={() => handleSelect(s)}
                  style={{ padding: '8px', borderBottom: '1px solid #eee', cursor: 'pointer' }}
                >
                  {`${s.vendor} ${s.name}`}
                </div>
              ))}
            </div>
          )}

          {selectedSupplier && (
            <div style={{ marginTop: '20px' }}>
              <h3 style={{ marginBottom: '10px' }}>
                {selectedSupplier.name}
                {details?.strategy_id && ` #${details.strategy_id}`}
              </h3>

              {loadingDetails && <p>Loading supplier profile...</p>}

              {!loadingDetails && details && (
                <>
                  <div style={{ border: '1px solid #ccc', borderRadius: '6px', padding: '15px', marginBottom: '20px' }}>
                    <h4>📄 Strategy Profile</h4>
                    <p><strong>{details.strategy_title}</strong></p>
                    <p>{details.strategy_description}</p>
                  </div>

                  <div style={{ border: '1px solid #ccc', borderRadius: '6px', padding: '15px' }}>
                    <h4>📦 Purchase Profile</h4>
                    <p>{details.purchase_profile}</p>
                  </div>
                </>
              )}
            </div>
          )}
        </>
      )}
    </div>
  )
}



strategy_title = next((r[3] for r in rows if r[3]), "N/A")
strategy_desc = next((str(r[4]).strip() for r in rows if r[4] and str(r[4]).strip()), "N/A")
strategy_id = next((str(r[5]).strip() for r in rows if r[5]), "N/A")
short_texts = [r[2].strip() for r in rows if r[2]]
purchase_profile = "; ".join(short_texts) if short_texts else "N/A"

return jsonify({
    "strategy_title": strategy_title,
    "strategy_description": strategy_desc,
    "purchase_profile": purchase_profile,
    "strategy_id": strategy_id
})


