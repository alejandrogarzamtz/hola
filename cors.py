axios.get('https://unspsc.deere.com/api/supplierss')
  .then(res => {
    console.log('📦 Respuesta de suppliers:', res.data) // 👈 Esto es lo que necesito que me pegues
    if (Array.isArray(res.data)) {
      setSuppliers(res.data)
      setFilteredSuppliers(res.data)
    } else {
      console.error('⚠️ La respuesta no es un arreglo:', res.data)
      setError(true)
    }
    setLoading(false)
  })
  .catch(err => {
    console.error('❌ Error loading suppliers:', err)
    setError(true)
    setLoading(false)
  })

