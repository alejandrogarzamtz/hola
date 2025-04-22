import { useEffect, useState } from 'react'
import axios from 'axios'
import { Box, Input, Typography, Card } from '@deere/fuel-react'

interface SupplierOption {
  vendor: string
  name: string
}

interface SupplierDetails {
  STRATEGY_TITLE: string
  STRATEGY_DESCRIPTION: string
  SHORT_TEXT: string[]
}

export const SupplierStrategyTest = () => {
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState<SupplierOption[]>([])
  const [details, setDetails] = useState<SupplierDetails | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    axios
      .get('http://localhost:8080/api/suppliers')
      .then((res) => {
        setSuggestions(res.data)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Error loading suppliers:', err)
        setError(true)
        setLoading(false)
      })
  }, [])

  const handleSelect = (vendor: string) => {
    setLoading(true)
    setSuggestions([])
    axios
      .get(`http://localhost:8080/api/supplier_profile?vendor=${vendor}`)
      .then((res) => {
        setDetails(res.data)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Error fetching details:', err)
        setLoading(false)
      })
  }

  const filtered = suggestions.filter((s) => {
    const q = query.toLowerCase()
    return s.vendor.toLowerCase().includes(q) || s.name.toLowerCase().includes(q)
  })

  return (
    <Box p={4}>
      <Typography variant="h4">Supplier Profile</Typography>

      {loading && !error && <Typography>Loading suppliers...</Typography>}
      {error && <Typography style={{color: 'red'}}>Error loading suppliers</Typography>}

      {!loading && !error && (
        <>
          <Input
            type="text"
            placeholder="Search by Vendor Number or Name"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <Box>
            {filtered.slice(0, 15).map((s, i) => (
              <Box
                key={i}
                onClick={() => handleSelect(s.vendor)}
                style={{ padding: '4px', cursor: 'pointer' }}
              >
                {s.vendor} {s.name}
              </Box>
            ))}
          </Box>
        </>
      )}

      {details && (
        <Card>
          <Typography variant="h5">{details.STRATEGY_TITLE}</Typography>
          <Typography>{details.STRATEGY_DESCRIPTION}</Typography>
          <ul>
            {details.SHORT_TEXT.map((text, i) => (
              <li key={i}>{text}</li>
            ))}
          </ul>
        </Card>
      )}
    </Box>
  )
}



