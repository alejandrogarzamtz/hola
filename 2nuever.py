app = Flask(__name__)

@app.route('/api/supplier_strategy_details', methods=['GET'])
def get_supplier_strategy_details():
    vendor = request.args.get('vendor')
    if not vendor:
        return jsonify({'error': 'Missing vendor parameter'}), 400

    try:
        connection = sql.connect(
            server_hostname="deere-edl.cloud.databricks.com",
            http_path="/sql/1.0/warehouses/a11c5b83a9f2f69c",
            access_token="dapi7804f46774679416aa8d409e5e2d676"
        )
        cursor = connection.cursor()

        # Query para strategy_title y strategy_desc (solo el primero)
        strategy_query = f'''
            SELECT DISTINCT
                strat.strategy_title,
                strat.strategy_desc
            FROM edl_current.manufacturing_purchasing_documents_header_ag AS PO
            LEFT JOIN edl_current.supplier_strategic_sourcing_ims_supplier AS Supplier
                ON PO.PARTNER_VENDOR = Supplier.supplier_number
            LEFT JOIN edl_current.supplier_strategic_sourcing_ims_strategy AS strat
                ON Supplier.strategy_id = strat.strategy_id
            WHERE PO.PARTNER_VENDOR = '{vendor}'
                AND PO.ORDER_FROM_SUPPLIER_NAME IS NOT NULL
            LIMIT 1
        '''
        cursor.execute(strategy_query)
        strategy_row = cursor.fetchone()

        strategy_title = strategy_row[0] if strategy_row and strategy_row[0] else "N/A"
        strategy_desc = strategy_row[1] if strategy_row and strategy_row[1] else "N/A"

        # Query para SHORT_TEXTS (todos)
        short_texts_query = f'''
            SELECT DISTINCT PO_Item.SHORT_TEXT
            FROM edl_current.manufacturing_purchasing_documents_header_ag AS PO
            INNER JOIN edl_current.manufacturing_purchasing_documents_item_ag AS PO_Item
                ON PO.PURCHASING_DOCUMENT = PO_Item.PURCHASING_DOCUMENT
            WHERE PO.PARTNER_VENDOR = '{vendor}'
                AND PO.ORDER_FROM_SUPPLIER_NAME IS NOT NULL
        '''
        cursor.execute(short_texts_query)
        short_texts = [row[0] for row in cursor.fetchall() if row[0]]

        cursor.close()
        connection.close()

        return jsonify({
            'strategy_title': strategy_title,
            'strategy_description': strategy_desc,
            'short_texts': short_texts
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
