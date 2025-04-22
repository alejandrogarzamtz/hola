@app.route('/api/supplier_strategy_details')
def get_supplier_strategy_details():
    vendor = request.args.get('vendor')

    connection = get_connection()
    cursor = connection.cursor()

    base_query = f"""
    SELECT
        COALESCE(PO.ORDER_FROM_SUPPLIER_NAME, 'N/A') AS ORDER_FROM_SUPPLIER_NAME,
        COALESCE(PO_Item.SHORT_TEXT, 'N/A') AS SHORT_TEXT,
        COALESCE(strat.strategy_title, 'N/A') AS strategy_title,
        COALESCE(strat.strategy_desc, 'N/A') AS strategy_desc
    FROM edl_current.manufacturing_purchasing_documents_header_ag AS PO
    INNER JOIN edl_current.manufacturing_purchasing_documents_item_ag AS PO_Item
        ON PO.PURCHASING_DOCUMENT = PO_Item.PURCHASING_DOCUMENT
    LEFT JOIN edl_current.supplier_strategic_sourcing_ims_supplier AS Supplier
        ON PO.PARTNER_VENDOR = Supplier.supplier_number
    LEFT JOIN edl_current.supplier_strategic_sourcing_ims_strategy AS strat
        ON Supplier.strategy_id = strat.strategy_id
    WHERE PO.PARTNER_VENDOR = '{vendor}'
      AND PO.ORDER_FROM_SUPPLIER_NAME IS NOT NULL
      AND PO.CREATED_ON > '2025-01-01'
      AND PO.PURCHASING_DOCUMENT_CATEGORY = 'F'
      AND PO_Item.MATERIAL_GROUP_CODE LIKE 'N%'
    ORDER BY PO.ORDER_FROM_SUPPLIER_NAME ASC
    """

    cursor.execute(base_query)
    results = cursor.fetchall()
    connection.close()

    if not results:
        return jsonify({
            "strategy_title": "N/A",
            "strategy_desc": "N/A",
            "short_texts": []
        })

    strategy_title = results[0][2] or "N/A"
    strategy_desc = results[0][3] or "N/A"
    short_texts = list({row[1] for row in results if row[1] is not None})

    return jsonify({
        "strategy_title": strategy_title,
        "strategy_desc": strategy_desc,
        "short_texts": short_texts
    })
