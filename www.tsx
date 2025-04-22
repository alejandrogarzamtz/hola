import { useEffect, useState } from 'react'
import axios from 'axios'
import { Box, Input, Typography } from '@deere/fuel-react'

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
    <Box p="4">
      <Typography variant="h4">Supplier for the Purchase Order</Typography>

      {loading && (
        <Typography>Loading suppliers...</Typography>
      )}

      {error && (
        <Typography color="danger">Error loading suppliers</Typography>
      )}

      {!loading && !error && (
        <Box mt="2" border="1px solid #ccc" borderRadius="md" maxHeight="300px" overflowY="scroll">
          {suppliers.map((s, i) => (
            <Box key={i} px="4" py="2" borderBottom="1px solid #eee">
              <Typography>{`${s.vendor} ${s.name}`}</Typography>
            </Box>
          ))}
        </Box>
      )}
    </Box>
  )
}






