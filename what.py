@app.route('/api/supplierss', methods=['GET'])
def search_suppliers():
    search = request.args.get('q', '')

    connection = sql.connect(
        server_hostname="deere-edl.cloud.databricks.com",
        http_path="/sql/1.0/warehouses/a11c5b83a9f2f69c",
        access_token="dapi86b04f9c73c07e48d3cbb3835c0552b6"
    )
    cursor = connection.cursor()

    base_query = '''
    SELECT DISTINCT
        CONCAT(
            COALESCE(PO.PARTNER_VENDOR, ''), ' ',
            COALESCE(PO.ORDER_FROM_SUPPLIER_NAME, '')
        )
    FROM edl_current.manufacturing_purchasing_documents_header_ag AS PO
    WHERE PO.ORDER_FROM_SUPPLIER_NAME IS NOT NULL
    ORDER BY PO.ORDER_FROM_SUPPLIER_NAME ASC
    LIMIT 5
'''

    cursor.execute(base_query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    final = [
        {
            "vendor": row[0][:10].strip(),
            "name": row[0][10:].strip()
        }
        for row in results
    ]

    print("✅ Final limpio:", final[:5])
    return jsonify(final)
