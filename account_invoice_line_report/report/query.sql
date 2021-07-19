
select detalle.account_id,
invoice.partner_id,
invoice.user_id,
detalle.product_id,
('-' || detalle.quantity) AS quantity,
detalle.price_unit,
detalle.price_subtotal,
invoice.number,
invoice.date_invoice

from account_invoice_line As detalle , account_invoice as invoice, res_partner as cliente, account_account as cuenta
where detalle.invoice_id = invoice.id and invoice.partner_id = cliente.id and invoice.account_id = cuenta.id
and invoice.type IN('out_invoice','out_refund')
limit 15;


select cuenta.name,
cliente.name,
sale.login,
item.default_code,
tem.name,
case when (invoice.type = 'out_refund') then CONCAT('-',detalle.quantity) end AS quantity1,
detalle.quantity,
detalle.price_unit,
detalle.price_subtotal,
invoice.number,
invoice.date_invoice,
CONCAT (cuenta.stri_fund,',', cuenta.stri_budget,',',cuenta.stri_desig,',',cuenta.stri_dept,',',cuenta.stri_account,',',cuenta.stri_class,',',cuenta.stri_program,',',cuenta.stri_project,',',cuenta.stri_activity,',',cuenta.stri_type) as chartfield
from account_invoice_line As detalle , account_invoice as invoice, res_partner as cliente, account_account as cuenta, res_users as sale, product_product as item, product_template as tem
where detalle.invoice_id = invoice.id and invoice.partner_id = cliente.id and detalle.account_id = cuenta.id and invoice.user_id = sale.id
and invoice.type IN('out_invoice','out_refund') and detalle.product_id = item.id and item.product_tmpl_id = tem.id
limit 15;

select CONCAT (cuenta.code,' ',cuenta.name),
cliente.name,
sale.name,
categ.complete_name, 
item.default_code,
tem.name,
case when (invoice.type = 'out_invoice') then detalle.quantity
else (detalle.quantity*-1) end AS quantity,
case when (invoice.type = 'out_invoice') then detalle.price_unit
else (detalle.price_unit*-1) end AS price,
case when (invoice.type = 'out_invoice') then detalle.price_subtotal
else (detalle.price_subtotal*-1) end AS total,
invoice.number,
invoice.date_invoice,
CONCAT (cuenta.stri_fund,',', cuenta.stri_budget,',',cuenta.stri_desig,',',cuenta.stri_dept,',',cuenta.stri_account,',',cuenta.stri_class,',',cuenta.stri_program,',',cuenta.stri_project,',',cuenta.stri_activity,',',cuenta.stri_type) as chartfield
from account_invoice_line As detalle , account_invoice as invoice, res_partner as cliente, account_account as cuenta, res_partner as sale, res_users as ur, product_product as item, product_template as tem, product_category as categ
where detalle.invoice_id = invoice.id and invoice.partner_id = cliente.id and detalle.account_id = cuenta.id and invoice.user_id = ur.id and ur.partner_id = sale.id
and invoice.type IN('out_invoice','out_refund') and invoice.state NOT IN ('draft','cancel') and detalle.product_id = item.id and item.product_tmpl_id = tem.id and tem.categ_id = categ.id;
group by invoice.date_invoice;
select rp.name, ru.login from res_users as ru, res_partner as rp where ru.partner_id = rp.id order by rp.name asc;