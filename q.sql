SELECT DISTINCT
  PO.PARTNER_VENDOR,
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
WHERE PO.PARTNER_VENDOR = '0000302355'
