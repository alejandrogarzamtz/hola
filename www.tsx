import { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Input, Typography, Card } from '@deere/fuel-react';

interface SupplierOption {
  vendor: string;
  name: string;
}

interface SupplierDetails {
  STRATEGY_TITLE: string;
  STRATEGY_DESCRIPTION: string;
  SHORT_TEXT: string[];
}

export const SupplierStrategyTest = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<SupplierOption[]>([]);
  const [details, setDetails] = useState<SupplierDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [allLoaded, setAllLoaded] = useState(false);

  useEffect(() => {
    axios.get('http://localhost:8080/api/suppliers')
      .then(res => {
        setSuggestions(res.data);
        setAllLoaded(true);
        setLoading(false);
      })
      .catch(err => {
        console.error('❌ Error loading suppliers:', err);
        setError(true);
        setLoading(false);
      });
  }, []);

  const handleSelect = (vendor: string) => {
    setLoading(true);
    setSuggestions([]);
    axios.get(`http://localhost:8080/api/supplier_profile?vendor=${vendor}`)
      .then(res => {
        setDetails(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching details:', err);
        setLoading(false);
      });
  };

  const filteredSuggestions = suggestions.filter((s) =>
    (s.name?.toLowerCase().includes(query.toLowerCase()) ||
     s.vendor?.toLowerCase().includes(query.toLowerCase()))
  );

  return (
    <Box>
      {loading && !allLoaded && (
        <Typography variant="body">Loading suppliers...</Typography>
      )}

      {error && (
        <Typography color="danger">Error loading suppliers</Typography>
      )}

      {!loading && allLoaded && (
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by Vendor Number or Name"
        />
      )}

      {!loading && allLoaded && query.length > 0 && (
        <Box style={{ maxHeight: '250px', overflowY: 'scroll' }}>
          {filteredSuggestions.map((s, i) => (
            <Box
              key={i}
              onClick={() => handleSelect(s.vendor)}
              style={{ padding: '4px', cursor: 'pointer' }}
            >
              {s.vendor} {s.name}
            </Box>
          ))}
        </Box>
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
  );
};





