@app.route('/api/supplier_strategy_details', methods=['GET'])
def get_supplier_strategy_details():
    vendor = request.args.get('vendor')
    if not vendor:
        return jsonify({'error': 'Vendor number is required'}), 400

    connection = sql.connect(
        server_hostname="deere-edl.cloud.databricks.com",
        http_path="/sql/1.0/warehouses/a11c5b83a9f2f69c",
        access_token="dapi7804f46774679416aa8d409e5e2d676"
    )
    cursor = connection.cursor()

    query = f'''
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
        WHERE PO.PARTNER_VENDOR = '{vendor}'
    '''

    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        print("❌ SQL Error:", e)
        return jsonify({'error': 'Query failed'}), 500
    finally:
        cursor.close()
        connection.close()

    if not results:
        return jsonify({
            "strategy_title": "N/A",
            "strategy_desc": "N/A",
            "short_texts": "N/A"
        })

    strategy_title = next((r[2] for r in results if r[2]), "N/A")
    strategy_desc = next((r[3] for r in results if r[3]), "N/A")
    short_texts = [r[1] for r in results if r[1]]
    concatenated = ', '.join(short_texts) if short_texts else "N/A"

    return jsonify({
        "strategy_title": strategy_title,
        "strategy_desc": strategy_desc,
        "short_texts": concatenated
    })
