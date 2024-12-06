select "Item Code" as article_id, "Item Name" as article_name, "Company" as company,  "Assortment Type" as assortment_typ,
"Active SE" as active_se, "Active Web SE" as active_web_se, "Role Coordinator" as product_coordinator, 
"Life Cycle Status" as life_cycle_status, CURRENT_DATE AS date, "Retail Price" as retail_price, "Actual Price" as actual_price,
"Comp Value" as comp_value, "Department" as department, "Sales Area" as sales_area
 from rusta_dw.public."Item" where "Company" = 10 and "Active Web SE" = 'Yes' and "Life Cycle Status" = 'Active' and
 "Assortment Type" not in ('SD,SP,AT')  //and "Item Code" in ('506012910105','506012910105','506012910106','957013890101','859017450104','859017450103')

