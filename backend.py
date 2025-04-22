@app.route('/api/supplier_full_profile', methods=['GET'])
def get_supplier_full_profile():
    vendor = request.args.get('vendor')
    if not vendor:
        return jsonify({'error': 'Missing vendor parameter'}), 400

    try:
        # Conexión a Databricks
        connection = sql.connect(
            server_hostname="deere-edl.cloud.databricks.com",
            http_path="/sql/1.0/warehouses/a11c5b83a9f2f69c",
            access_token="dapi7804f46774679416aa8d409e5e2d676"
        )
        cursor = connection.cursor()

        # Query para obtener datos base
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

        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        if not rows:
            return jsonify({'error': 'No data found'}), 404

        # Obtener valores únicos
        company_name = next((r[0] for r in rows if r[0]), "N/A")
        strategy_title = next((r[2] for r in rows if r[2]), "N/A")
        strategy_description = next((r[3] for r in rows if r[3]), "N/A")
        purchase_profile_raw = ' • '.join(r[1] for r in rows if r[1]) or "N/A"

        # --- IA: Generar Company Profile ---
        company_query = [
            {
                "role": "user",
                "content": f"Based on public knowledge, write a short VERY SHORT but complete profile of the company '{company_name}' in English. If you don't know it, guess based on the name and industry tone. and what you found in '{purchase_profile_raw}' and '{strategy_description}' dont say nothing more, just the profile, because that info is gonna be placed on a new excel, so DONT say nothing else, dont give me any warnings, etc. if is IMPOSSIBLE only impossible to you to recover this info, guess something about the company, but like it was true, dont put anything else, just the company profile, not give notifications of any type, like I'm sorry, but I don't have the answer to that question or anything else, dont put any style like ** or subtitles. JUST THE PLAIN AND VERY SHORT TEXT ABOUT THE COMPANY. SO SHORT, AND NO STYLE."
            }
        ]
        r1 = requests.post("http://127.0.0.1:5000/api/chat", data={
            "messages": json.dumps(company_query),
            "model-selection": "Default Model"
        }, stream=True)

        company_profile = ""
        for line in r1.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "choices" in data and data["choices"]:
                    delta = data["choices"][0].get("delta", {})
                    company_profile += delta.get("content", "")

        # --- IA: Traducir purchase profile ---
        translate_query = [
            {
                "role": "user",
                "content": f"Translate this to English, in a paragraph, make sure you translate ALL, and don't say anything else: {purchase_profile_raw}"
            }
        ]
        r2 = requests.post("http://127.0.0.1:5000/api/chat", data={
            "messages": json.dumps(translate_query),
            "model-selection": "Default Model"
        }, stream=True)

        translated_purchase = ""
        for line in r2.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "choices" in data and data["choices"]:
                    delta = data["choices"][0].get("delta", {})
                    translated_purchase += delta.get("content", "")

        return jsonify({
            "strategy_title": strategy_title or "N/A",
            "strategy_description": strategy_description or "N/A",
            "company_profile": company_profile.strip() or "N/A",
            "purchase_profile": translated_purchase.strip() or "N/A"
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
