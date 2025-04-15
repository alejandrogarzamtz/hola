@app.route('/api/supplier_strategy_details', methods=['GET'])
def get_supplier_strategy_details():
    try:
        print("👉 Endpoint /api/supplier_strategy_details fue llamado")

        connection = sql.connect(
            server_hostname="deere-edl.cloud.databricks.com",
            http_path="/sql/1.0/warehouses/a11c5b83a9f2f69c",
            access_token="dapi86b04f9c73c07e48d3cbb3835c0552b6"
        )
        cursor = connection.cursor()

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
        WHERE base.PARTNER_VENDOR IN (
            '0000341561', '0000340828', '0000381569', '0000381620', '0000369781', '000010650',
            '000046980', '000010014', '0000382291', '000079721', '000065964', '000043300',
            '000026429', '0000379900', '0000344032', '000015018', '000078876', '000036446',
            '0000379555', '0000307672', '000026844', '000058372', '000086049', '0000379727',
            '0000349295', '0000352638', '0000378025', '0000329579'
        )
        ORDER BY base.ORDER_FROM_SUPPLIER_NAME ASC
        """

        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        result_list = [dict(zip(columns, row)) for row in results]

        cursor.close()
        connection.close()

        print(f"🔍 Resultados: {len(result_list)} registros enviados.")
        return jsonify(result_list), 200

    except Exception as e:
        print(f"❌ Error en la consulta: {e}")
        return jsonify({"error": str(e)}), 500
