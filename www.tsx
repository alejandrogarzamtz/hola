import { useEffect, useState } from 'react'
import axios from 'axios'
import {
  Box,
  Typography,
  Card,
  Input,
  InputGroup,
  InputIcon,
  Scrollbar,
} from '@deere/fuel-react'
import { SearchIcon } from 'lucide-react'

interface SupplierOption {
  PARTNER_VENDOR: string
  ORDER_FROM_SUPPLIER_NAME: string
}

interface SupplierDetails {
  STRATEGY_TITLE: string
  STRATEGY_DESC: string
  SHORT_TEXT: string[]
}

export const SupplierProfile = () => {
  const [query, setQuery] = useState('')
  const [options, setOptions] = useState<SupplierOption[]>([])
  const [selectedVendor, setSelectedVendor] = useState<string>('')
  const [details, setDetails] = useState<SupplierDetails | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (query.length < 1) {
      setOptions([])
      return
    }
    const delayDebounce = setTimeout(() => {
      axios
        .get(`http://localhost:8080/api/search_vendors?query=${query}`)
        .then((res) => {
          setOptions(res.data)
        })
        .catch((err) => {
          console.error('Error loading suggestions', err)
        })
    }, 300)

    return () => clearTimeout(delayDebounce)
  }, [query])

  useEffect(() => {
    if (!selectedVendor) return
    setLoading(true)
    axios
      .get(`http://localhost:8080/api/supplier_profile?vendor=${selectedVendor}`)
      .then((res) => {
        setDetails(res.data)
      })
      .catch((err) => {
        console.error('Error loading vendor details', err)
      })
      .finally(() => setLoading(false))
  }, [selectedVendor])

  return (
    <Box padding={6}>
      <Typography variant="h2" marginBottom={3}>
        📚 Supplier Profile
      </Typography>

      <InputGroup size="lg" marginBottom={4}>
        <InputIcon>
          <SearchIcon size={20} />
        </InputIcon>
        <Input
          placeholder="Search by Vendor Number or Company Name..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </InputGroup>

      <Box marginBottom={5}>
        {options.map((opt) => (
          <Typography
            key={opt.PARTNER_VENDOR}
            onClick={() => setSelectedVendor(opt.PARTNER_VENDOR)}
            sx={{
              cursor: 'pointer',
              marginBottom: 1,
              '&:hover': { textDecoration: 'underline' },
            }}
          >
            {opt.PARTNER_VENDOR} – {opt.ORDER_FROM_SUPPLIER_NAME}
          </Typography>
        ))}
      </Box>

      {loading && <Typography>Loading supplier details...</Typography>}

      {!loading && details && (
        <Box display="flex" gap={4}>
          <Card padding={4} width="30%">
            <Typography variant="h4" marginBottom={2}>
              📄 Strategy Profile
            </Typography>
            <Typography fontWeight="bold">{details.STRATEGY_TITLE}</Typography>
            <Typography>{details.STRATEGY_DESC}</Typography>
          </Card>

          <Card padding={4} width="70%">
            <Typography variant="h4" marginBottom={2}>
              📗 Purchase Profile
            </Typography>
            <Scrollbar height="300px">
              {details.SHORT_TEXT.map((item, index) => (
                <Typography key={index} marginBottom={1}>
                  {item}
                </Typography>
              ))}
            </Scrollbar>
          </Card>
        </Box>
      )}
    </Box>
  )
}

