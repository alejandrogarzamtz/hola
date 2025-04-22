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
  const [suppliers, setSuppliers] = useState<SupplierOption[]>([]);
  const [filtered, setFiltered] = useState<SupplierOption[]>([]);
  const [details, setDetails] = useState<SupplierDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    axios.get('http://localhost:8080/api/suppliers')
      .then(res => {
        setSuppliers(res.data);
        setFiltered(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching suppliers:', err);
        setError(true);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    const q = query.toLowerCase();
    setFiltered(
      suppliers.filter(s =>
        s.vendor.toLowerCase().includes(q) ||
        s.name.toLowerCase().includes(q)
      )
    );
  }, [query, suppliers]);

  const handleSelect = (vendor: string) => {
    setDetails(null);
    axios.get(`http://localhost:8080/api/supplier_profile?vendor=${vendor}`)
      .then(res => setDetails(res.data))
      .catch(err => console.error('Error fetching details:', err));
  };

  if (loading) return <Typography>Loading suppliers...</Typography>;
  if (error) return <Typography syle={{color: 'red'}}>Error loading suppliers</Typography>;

  return (
    <Box>
      <Input
        placeholder="Search by Vendor Number or Name"
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <Box>
        {filtered.slice(0, 10).map((s, i) => (
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
          <Typography variant="h5">{details.STRATEGY_TITLE}</Typography>
          <Typography>{details.STRATEGY_DESCRIPTION}</Typography>
          <ul>
            {details.SHORT_TEXT.map((text, i) => <li key={i}>{text}</li>)}
          </ul>
        </Card>
      )}
    </Box>
  );
};




