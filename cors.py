useEffect(() => {
  axios.get('https://unspsc-api.deere.com/api/supplierss')
    .then(res => {
      console.log("✅ Recibido correctamente:", res.data)
    })
    .catch(err => {
      console.error("❌ Error en la API:", err)
    })
}, [])


