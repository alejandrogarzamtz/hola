@app.route('/api/supplier_profile', methods=['GET'])
def supplier_profile():
    vendor = request.args.get('vendor')
    if not vendor:
        return jsonify({"error": "Vendor not provided"}), 400

    connection = sql.connect(
        server_hostname="deere-edl.cloud.databricks.com",
        http_path="/sql/1.0/warehouses/tu-warehouse-id",
        access_token="tu-token"
    )
    cursor = connection.cursor()

    query = '''
        SELECT
            PO.ORDER_FROM_SUPPLIER_NAME,
            PO_Item.SHORT_TEXT,
            strat.strategy_title,
            strat.strategy_desc
        FROM edl_current.manufacturing_purchasing_documents_header_ag AS PO
        INNER JOIN edl_current.manufacturing_purchasing_documents_item_ag AS PO_Item
            ON PO.PURCHASING_DOCUMENT = PO_Item.PURCHASING_DOCUMENT
        LEFT JOIN edl_current.supplier_strategic_sourcing_ims_supplier AS Supplier
            ON PO.PARTNER_VENDOR = Supplier.supplier_number
        LEFT JOIN edl_current.supplier_strategic_sourcing_ims_strategy AS strat
            ON Supplier.strategy_id = strat.strategy_id
        WHERE PO.PARTNER_VENDOR = ?
        AND PO.ORDER_FROM_SUPPLIER_NAME IS NOT NULL
        AND PO.CREATED_ON > '2025-01-01'
        AND PO.PURCHASING_DOCUMENT_CATEGORY = 'F'
        AND PO_Item.MATERIAL_GROUP_CODE LIKE 'N%'
        ORDER BY PO.ORDER_FROM_SUPPLIER_NAME ASC
    '''

    cursor.execute(query, (vendor,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    if not results:
        return jsonify({"error": "No results found"}), 404

    strategy_title = None
    strategy_description = None
    short_texts = []

    for row in results:
        if not strategy_title and row[2]:
            strategy_title = row[2]
        if not strategy_description and row[3]:
            strategy_description = row[3]
        if row[1]:
            short_texts.append(row[1])

    return jsonify({
        "strategy_title": strategy_title,
        "strategy_description": strategy_description,
        "short_texts": short_texts
    })
