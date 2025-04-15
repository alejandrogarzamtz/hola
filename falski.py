@app.route('/api/suppliers', methods=['GET'])
def search_suppliers():
    search = request.args.get('q', '')
    connection = sql.connect(
        server_hostname="deere-edl.cloud.databricks.com",
        http_path="/sql/1.0/warehouses/a11c5b83a9f2f69c",
        access_token="dapiREEMPLAZAME"
    )
    cursor = connection.cursor()

    query = f'''
        SELECT DISTINCT
            PO.PARTNER_VENDOR,
            PO.ORDER_FROM_SUPPLIER_NAME
        FROM edl_current.manufacturing_purchasing_documents_header_ag AS PO
        WHERE PO.ORDER_FROM_SUPPLIER_NAME LIKE '%{search}%'
           OR PO.PARTNER_VENDOR LIKE '%{search}%'
        ORDER BY PO.ORDER_FROM_SUPPLIER_NAME ASC
        LIMIT 20
    '''

    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify([{'vendor': r[0], 'name': r[1]} for r in results])

@app.route('/api/supplier_profile', methods=['GET'])
def get_supplier_profile():
    vendor = request.args.get('vendor')
    connection = sql.connect(
        server_hostname="deere-edl.cloud.databricks.com",
        http_path="/sql/1.0/warehouses/a11c5b83a9f2f69c",
        access_token="dapiREEMPLAZAME"
    )
    cursor = connection.cursor()

    query = f'''
        WITH base_po AS (
            SELECT
                PO.PARTNER_VENDOR,
                PO.ORDER_FROM_SUPPLIER_NAME,
                PO_Item.SHORT_TEXT
            FROM edl_current.manufacturing_purchasing_documents_header_ag AS PO
            INNER JOIN edl_current.manufacturing_purchasing_documents_item_ag AS PO_Item
                ON PO.PURCHASING_DOCUMENT = PO_Item.PURCHASING_DOCUMENT
            WHERE PO.ORDER_FROM_SUPPLIER_NAME IS NOT NULL
              AND PO.PARTNER_VENDOR = '{vendor}'
        ),
        strategy AS (
            SELECT
                supplier.supplier_number,
                strat.strategy_title,
                strat.strategy_desc
            FROM edl_current.supplier_strategic_sourcing_ims_supplier AS supplier
            LEFT JOIN edl_current.supplier_strategic_sourcing_ims_strategy AS strat
                ON supplier.strategy_id = strat.strategy_id
            WHERE supplier.supplier_number = '{vendor}'
        )
        SELECT
            MAX(base.ORDER_FROM_SUPPLIER_NAME),
            MAX(s.strategy_title),
            MAX(s.strategy_desc),
            COLLECT_LIST(base.SHORT_TEXT)
        FROM base_po AS base
        LEFT JOIN strategy AS s
            ON base.PARTNER_VENDOR = s.supplier_number
        GROUP BY base.PARTNER_VENDOR
    '''

    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if not row:
        return jsonify({}), 404

    return jsonify({
        'company': row[0],
        'strategy_title': row[1],
        'strategy_desc': row[2],
        'purchase_profile': row[3] if isinstance(row[3], list) else []
    })
