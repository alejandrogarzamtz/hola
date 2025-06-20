@app.route('/api/supplier_strategy_details', methods=['GET'])
def get_supplier_strategy_details():
    vendor = request.args.get('vendor')
    if not vendor:
        return jsonify({'error': 'Missing vendor'}), 400

    try:
        connection = sql.connect(
            server_hostname="deere-edl.cloud.databricks.com",
            http_path="/sql/1.0/warehouses/...",
            access_token="..."
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
        ORDER BY PO.ORDER_FROM_SUPPLIER_NAME ASC
        '''

        cursor.execute(query)
        results = cursor.fetchall()

        purchase_profile = ' • '.join(row[1] for row in results if row[1])
        first_with_strategy = next((row for row in results if row[2] or row[3]), None)

        strategy_title = first_with_strategy[2] if first_with_strategy and first_with_strategy[2] else 'N/A'
        strategy_desc = first_with_strategy[3] if first_with_strategy and first_with_strategy[3] else 'N/A'

        return jsonify({
            "strategy_title": strategy_title,
            "strategy_desc": strategy_desc,
            "purchase_profile": purchase_profile
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
