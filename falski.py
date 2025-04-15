@app.route('/api/supplier_strategy_details', methods=['GET'])
def get_supplier_strategy_details():
    try:
        print("👉 Endpoint /api/supplier_strategy_details fue llamado")

        # Conexión a Databricks
        connection = sql.connect(
            server_hostname="deere-edl.cloud.databricks.com",
            http_path="/sql/1.0/warehouses/a11c5b83a9f2f69c",
            access_token=""  # tu nuevo token
        )
        cursor = connection.cursor()

        # Query completa
        query = """
        WITH base_po AS (
            SELECT DISTINCT
                PO.PARTNER_VENDOR,
                PO.ORDER_FROM_SUPPLIER_NAME,
                PO_Item.SHORT_TEXT
            FROM edl_current.manufacturing_purchasing_documents_header_ag AS PO
            INNER JOIN edl_current.manufacturing_purchasing_documents_item_ag AS PO_Item
                ON PO.PURCHASING_DOCUMENT = PO_Item.PURCHASING_DOCUMENT
            WHERE PO.ORDER_FROM_SUPPLIER_NAME IS NOT NULL
                AND PO.PURCHASING_DOCUMENT_CATEGORY = 'F'
                AND PO_Item.MATERIAL_GROUP_CODE LIKE 'N%'
        ),
        supplier_strategy AS (
            SELECT DISTINCT
                supplier.supplier_number,
                strat.strategy_title,
                strat.strategy_desc
            FROM edl_current.supplier_strategic_sourcing_ims_supplier AS supplier
            LEFT JOIN edl_current.supplier_strategic_sourcing_ims_strategy AS strat
                ON supplier.strategy_id = strat.strategy_id
        )
        SELECT
            base.PARTNER_VENDOR,
            base.ORDER_FROM_SUPPLIER_NAME,
            base.SHORT_TEXT,
            ss.strategy_title AS Strategy_Title,
            ss.strategy_desc AS Strategy_Description
        FROM base_po AS base
        LEFT JOIN supplier_strategy AS ss
            ON base.PARTNER_VENDOR = ss.supplier_number
        ORDER BY base.ORDER_FROM_SUPPLIER_NAME ASC
        """

        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        cursor.close()
        connection.close()

        result_list = [dict(zip(columns, row)) for row in results[:50]]  # Solo primeros 50

        print(f"🔍 Resultados: {len(result_list)} registros enviados.")
        return jsonify(result_list), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
