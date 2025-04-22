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

  // 🔹 Al cargar la página: traer todos los suppliers
  useEffect(() => {
    axios.get('http://localhost:8080/api/suppliers')
      .then(res => setSuggestions(res.data))
      .catch(err => console.error('Error cargando todos los suppliers:', err))
  }, [])

  const handleSelect = (vendor: string) => {
    setLoading(true)
    setSuggestions([]) // limpia la lista
    axios.get(`http://localhost:8080/api/supplier_profile?vendor=${vendor}`)
      .then(res => {
        setDetails(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error obteniendo detalles:', err)
        setLoading(false)
      })
  }

  return (
    <Box padding={4}>
      <Typography variant="h2" marginBottom={3}>
        📌 Supplier Profile
      </Typography>

      <Box position="relative" marginBottom={2}>
        <Input
          value={query}
          onChange={(e: any) => setQuery(e.target.value)}
          placeholder="Search by Vendor Number or Company Name..."
        />
        {suggestions.length > 0 && (
          <Box sx={{ border: '1px solid #ccc', position: 'absolute', width: '100%', background: 'white', zIndex: 10 }}>
            {suggestions.map((option, index) => (
              <Box
                key={index}
                padding={2}
                sx={{ cursor: 'pointer', '&:hover': { backgroundColor: '#f1f1f1' } }}
                onClick={() => handleSelect(option.vendor)}
              >
                {option.vendor} {option.name}
              </Box>
            ))}
          </Box>
        )}
      </Box>

      {!loading && details && (
        <Box display="flex" gap={4}>
          <Card sx={{ padding: 4, width: '30%' }}>
            <Typography variant="h4" marginBottom={2}>
              📄 Strategy Profile
            </Typography>
            <Typography variant="body1" fontWeight="bold">
              {details.STRATEGY_TITLE}
            </Typography>
            <Typography variant="body2">
              {details.STRATEGY_DESCRIPTION}
            </Typography>
          </Card>

          <Card sx={{ padding: 4, width: '70%' }}>
            <Typography variant="h4" marginBottom={2}>
              📅 Purchase Profile
            </Typography>
            <Box height="300px" sx={{ overflowY: 'scroll' }}>
              {details.SHORT_TEXT.map((item, index) => (
                <Typography key={index} marginBottom={1}>{item}</Typography>
              ))}
            </Box>
          </Card>
        </Box>
      )}
    </Box>
  )
}


