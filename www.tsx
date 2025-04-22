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
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(false)

  useEffect(() => {
    if (query.length === 0) {
      setSuggestions([])
      return
    }

    const timeout = setTimeout(() => {
      setLoading(true)
      axios
        .get(`http://localhost:8080/api/suppliers?q=${query}`)
        .then(res => {
          setSuggestions(res.data)
          setError(false)
        })
        .catch(err => {
          console.error('Error fetching suggestions:', err)
          setError(true)
        })
        .finally(() => setLoading(false))
    }, 300)

    return () => clearTimeout(timeout)
  }, [query])

  const handleSelect = (vendor: string) => {
    setLoading(true)
    setSuggestions([])
    axios
      .get(`http://localhost:8080/api/supplier_profile?vendor=${vendor}`)
      .then(res => {
        setDetails(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching details:', err)
        setLoading(false)
      })
  }

  return (
    <Box>
      <Input
        placeholder="Search by Vendor Number"
        value={query}
        onChange={e => setQuery(e.target.value)}
      />

      {loading && <Typography>Loading suppliers...</Typography>}
      {error && <Typography style={{color: 'red'}}>Error loading suppliers</Typography>}

      <Box>
        {suggestions
          .filter(
            s =>
              (s.vendor && s.vendor.includes(query)) ||
              (s.name && s.name.toLowerCase().includes(query.toLowerCase()))
          )
          .map((s, i) => (
            <Box
              key={i}
              onClick={() => handleSelect(s.vendor)}
              style={{ padding: '4px', cursor: 'pointer' }}
            >
              {s.vendor} {s.name}
            </Box>
          ))}
      </Box>

      {details && (
        <Card>
          <Typography variant="h6">{details.STRATEGY_TITLE}</Typography>
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



