import { useEffect, useState } from 'react'
import axios from 'axios'
import { Box, Typography, Card } from '@deere/fuel-react'

interface SupplierData {
  PARTNER_VENDOR: string
  ORDER_FROM_SUPPLIER_NAME: string
  SHORT_TEXT: string
  Strategy_Title: string
  Strategy_Description: string
}

export const SupplierStrategyTest = () => {
  const [data, setData] = useState<SupplierData[] | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    axios.get('http://localhost:8080/api/supplier_strategy_details')
      .then(response => {
        setData(response.data)
        setLoading(false)
      })
      .catch(error => {
        console.error("Error fetching supplier strategy details:", error)
        setError("Hubo un error al cargar los datos.")
        setLoading(false)
      })
  }, [])

  return (
    <Box padding={4}>
      <Typography variant="h2" marginBottom={3}>
        🧾 Supplier Strategy Details
      </Typography>
      {loading && <Typography>Cargando datos...</Typography>}
      {error && <Typography color="error">{error}</Typography>}
      {!loading && data && Array.isArray(data) && data.map((item, index) => (
        <Card key={index} sx={{ padding: 3, marginBottom: 2 }}>
          <Typography variant="h4">{item.ORDER_FROM_SUPPLIER_NAME}</Typography>
          <Typography variant="body1">
            Vendor: {item.PARTNER_VENDOR}<br />
            {item.SHORT_TEXT}<br />
            <strong>{item.Strategy_Title}</strong>: {item.Strategy_Description}
          </Typography>
        </Card>
      ))}
    </Box>
  )
}
