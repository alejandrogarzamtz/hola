@app.route('/api/supplier_strategy_details', methods=['GET'])
def get_supplier_strategy_details():
    vendor = request.args.get('vendor', '').strip()

    if not vendor:
        return jsonify({'error': 'Vendor is required'}), 400

    # Conexión directa (ajusta si prefieres función separada)
    connection = sql.connect(
        server_hostname="deere-edl.cloud.databricks.com",
        http_path="/sql/1.0/warehouses/a11c5b83a9f2f69c",
        access_token="tu_token_aquí"
    )
    cursor = connection.cursor()

    query = f'''
        SELECT
            PO.PARTNER_VENDOR,
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
        WHERE PO.PARTNER_VENDOR = '{vendor}'
            AND PO.ORDER_FROM_SUPPLIER_NAME IS NOT NULL
        ORDER BY PO.ORDER_FROM_SUPPLIER_NAME ASC
    '''

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    if not rows:
        return jsonify({
            "strategy_title": "N/A",
            "strategy_desc": "N/A",
            "purchase_profile": "N/A"
        })

    # Toma el primer title/desc no null y concatena todos los SHORT_TEXT
    strategy_title = next((r[3] for r in rows if r[3]), "N/A")
    strategy_desc = next((r[4] for r in rows if r[4]), "N/A")

    short_texts = [r[2].strip() for r in rows if r[2]]
    purchase_profile = "; ".join(short_texts) if short_texts else "N/A"

    return jsonify({
        "strategy_title": strategy_title,
        "strategy_desc": strategy_desc,
        "purchase_profile": purchase_profile
    })
