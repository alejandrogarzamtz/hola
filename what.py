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
    PO.PARTNER_VENDOR,
    PO.ORDER_FROM_SUPPLIER_NAME
FROM edl_current.manufacturing_purchasing_documents_header_ag AS PO
INNER JOIN edl_current.manufacturing_purchasing_documents_item_ag AS PO_Item
    ON PO.PURCHASING_DOCUMENT = PO_Item.PURCHASING_DOCUMENT
LEFT JOIN edl_current.supplier_strategic_sourcing_ims_supplier AS Supplier
    ON PO.PARTNER_VENDOR = Supplier.supplier_number
LEFT JOIN edl_current.supplier_strategic_sourcing_ims_strategy AS strat
    ON Supplier.strategy_id = strat.strategy_id
WHERE PO.ORDER_FROM_SUPPLIER_NAME IS NOT NULL
    AND PO.CREATED_ON >= '2023-01-01'
    AND PO.PURCHASING_DOCUMENT_CATEGORY = 'F'
    AND PO_Item.MATERIAL_GROUP_CODE LIKE 'W%'
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
