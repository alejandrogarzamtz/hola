from flask import Flask, request, jsonify
import re

@app.route('/api/supplier_strategy_details')
def get_supplier_strategy_details():
    vendor = request.args.get('vendor', '').strip()
    if not vendor:
        return jsonify({'error': 'Vendor not provided'}), 400

    connection = get_connection()  # Asegúrate de tener tu función para conectar a Databricks
    cursor = connection.cursor()

    query = f"""
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
          AND PO.ORDER_FROM_SUPPLIER_NAME IS NOT NULL
          AND PO.CREATED_ON > '2025-01-01'
          AND PO.PURCHASING_DOCUMENT_CATEGORY = 'F'
          AND PO_Item.MATERIAL_GROUP_CODE LIKE 'N%'
        ORDER BY PO.ORDER_FROM_SUPPLIER_NAME ASC
    """

    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        print("❌ SQL Error:", e)
        return jsonify({'error': 'Database query failed'}), 500
    finally:
        cursor.close()
        connection.close()

    if not results:
        return jsonify({
            'strategy_title': 'N/A',
            'strategy_description': 'N/A',
            'purchase_profile': 'No records found for this vendor.'
        })

    # El primer título y descripción no nulos
    title = next((r[2] for r in results if r[2]), 'N/A')
    desc = next((r[3] for r in results if r[3]), 'N/A')

    # Concatenación de todos los SHORT_TEXT que no sean null
    short_texts = [r[1] for r in results if r[1]]
    concatenated = ', '.join(short_texts) if short_texts else 'No descriptions found.'

    return jsonify({
        'strategy_title': title,
        'strategy_description': desc,
        'purchase_profile': concatenated
    })
