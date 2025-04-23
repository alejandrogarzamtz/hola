CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "http://localhost:4173",
                "https://unspsc.deere.com",
                "https://unspsc.deere.com/",
            ]
        }
    },
)

axios.get('https://unspsc.deere.com/api/supplierss')
