@app.route('/api/supplier_full_profile', methods=['GET'])
def get_supplier_full_profile():
    try:
        vendor = request.args.get('vendor', '').strip()

        if not vendor:
            return jsonify({'error': 'Vendor is required'}), 400

        # 1. Obtener datos de Databricks
        connection = sql.connect(
            server_hostname="deere-edl.cloud.databricks.com",
            http_path="/sql/1.0/warehouses/a11c5b83a9f2f69c",
            access_token="dapi7840f46774f679416aa8d409e5e2d676"
        )
        cursor = connection.cursor()

        query = f'''
            SELECT
                PO.PARTNER_VENDOR,
                PO.ORDER_FROM_SUPPLIER_NAME,
                PO_Item.SHORT_TEXT,
                strat.strategy_id,
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
                "strategy_description": "N/A",
                "purchase_profile": "N/A",
                "company_profile": "N/A"
            }), 200

        company_name = rows[0][1]
        strategy_title = next((r[4] for r in rows if r[4]), "N/A")
        strategy_description = next((r[5] for r in rows if r[5]), "N/A")
        purchase_profile = "; ".join([r[2] for r in rows if r[2]]) if rows else "N/A"

        # 2. Preparar mensaje para perfil de empresa
        profile_prompt = [
            {"role": "user", "content": f"Based on public knowledge, write a short VERY SHORT but complete profile of the company '{company_name}' in English. If you don't know it, guess based on the name and industry tone. and what you found in '{purchase_profile}' and '{strategy_description}' dont say nothing more, just the profile, because that info is gonna be placed on a new excel, so DONT say nothing else, dont give me any warnings, etc. if is IMPOSSIBLE only impossible to you to recover this info, guess something about the company, but like it was true, dont put anything else, just de company profile, not give notifications of any type, like I'm sorry, but I don't have the answer to that question or anything else, dont put any style like ** or subtittles. JUST THE PLAIN AN DVERY SHORT TEXT ABOUT THE COMPANY. SO SHORT, AND NO STYLE."}
        ]

        # 3. Preparar mensaje para traducción del purchase profile
        translation_prompt = [
            {"role": "user", "content": f"Translate this to English, in a paragraph, make sure you translate ALL, and dont say nothing else, just translate, dont give notifications or anything: {purchase_profile}"}
        ]

        # 4. Llamadas a IA usando stream_text
        stream_profile = stream_text(profile_prompt)
        stream_translation = stream_text(translation_prompt)

        # 5. Procesar respuestas de IA
        company_profile = ""
        for line in stream_profile:
            if line:
                try:
                    data = json.loads(line)
                    if "choices" in data:
                        delta = data["choices"][0].get("delta", {})
                        company_profile += delta.get("content", "")
                except:
                    continue

        translated_purchase_profile = ""
        for line in stream_translation:
            if line:
                try:
                    data = json.loads(line)
                    if "choices" in data:
                        delta = data["choices"][0].get("delta", {})
                        translated_purchase_profile += delta.get("content", "")
                except:
                    continue

        # 6. Respuesta final
        return jsonify({
            "strategy_title": strategy_title.strip(),
            "strategy_description": strategy_description.strip(),
            "purchase_profile": translated_purchase_profile.strip(),
            "company_profile": company_profile.strip()
        }), 200

    except Exception as e:
        print(f"Error in supplier_full_profile: {str(e)}")
        return jsonify({"error": str(e)}), 500
