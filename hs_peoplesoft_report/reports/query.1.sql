WITH people_soft_data AS (
			SELECT
				line.id as id,
				(SELECT AM2.id from account_move as AM2 WHERE line.move_id = AM2.id limit 1) as external_order,
				(SELECT CASE WHEN account.user_type_id = (SELECT id FROM account_account_type WHERE name = 'Income' LIMIT 1) 
				THEN CONCAT(account.stri_fund, ',', account.stri_budget, ',', account.stri_desig, ',', account.stri_dept, ',', account.stri_account, ',', account.stri_class, ',', account.stri_program, ',', account.stri_project, ',', account.stri_activity, ',', account.stri_type)
				ELSE (SELECT CASE WHEN partner.customer_type = 'fund' 
					THEN CONCAT(partner.stri_fund, ',', partner.stri_budget, ',', partner.stri_desig, ',', partner.stri_dept, ',', partner.stri_account, ',', partner.stri_class, ',', partner.stri_program, ',', partner.stri_project, ',', partner.stri_activity, ',', partner.stri_type)
					ELSE (SELECT CONCAT(aa2.stri_fund, ',', aa2.stri_budget, ',', aa2.stri_desig, ',', aa2.stri_dept, ',', aa2.stri_account, ',', aa2.stri_class, ',', aa2.stri_program, ',', aa2.stri_project, ',', aa2.stri_activity, ',', aa2.stri_type) as strifund
						FROM account_account as aa2, account_journal as aj2
						WHERE aa2.id = aj2.default_debit_account_id AND aj2.id = inv.journal_id LIMIT 1)	
					END)
				END) AS chartfield,
				line.partner_id,
				line.invoice_id as invoice,
				inv.number as reference,
				inv.people_soft_registered as registered,
				(SELECT CASE WHEN partner.customer_type = 'fund' THEN -1 ELSE inv.journal_id END) as doc_type,
				(SELECT CASE WHEN inv.type = 'out_invoice' THEN 'invoice' ELSE 'refund' END) AS document,
				(SELECT CASE WHEN account.user_type_id = (SELECT id FROM account_account_type WHERE name = 'Income' LIMIT 1) THEN 0 ELSE 1 END) AS sub_order,
				(SELECT (CASE WHEN credit > 0.00 THEN (credit * -1) WHEN debit > 0.00 THEN debit ELSE 0.00 END )) AS amount
			FROM account_move_line AS line, account_invoice AS inv, res_partner AS partner, account_account AS account, account_journal as journal
			WHERE (line.date BETWEEN '{}' AND '{}') AND line.invoice_id = inv.id AND line.partner_id = partner.id 
			AND inv.journal_id = journal.id AND line.account_id = account.id AND inv.type in ('out_invoice', 'out_refund') AND inv.state = 'open'
			
			UNION

			/*
			Consultamos ahora payment para obtener los rate off.
			Si quisieramos a futuro agregar todo los pagos, esta seccion es el que debe modificarse 
			*/
			SELECT
				line.id as id,
				(SELECT AM2.id from account_move as AM2 WHERE line.move_id = AM2.id limit 1) as external_order,
				(SELECT CASE WHEN account.user_type_id = (SELECT at2.id FROM account_account_type AS at2 WHERE account.user_type_id = at2.id AND at2.name = 'Expenses' limit 1)
				THEN CONCAT(account.stri_fund, ',', account.stri_budget, ',', account.stri_desig, ',', account.stri_dept, ',', account.stri_account, ',', account.stri_class, ',', account.stri_program, ',', account.stri_project, ',', account.stri_activity, ',', account.stri_type)
				ELSE
					(SELECT CONCAT(aa2.stri_fund, ',', aa2.stri_budget, ',', aa2.stri_desig, ',', aa2.stri_dept, ',', aa2.stri_account, ',', aa2.stri_class, ',', aa2.stri_program, ',', aa2.stri_project, ',', aa2.stri_activity, ',', aa2.stri_type) as strifund
					FROM account_invoice_payment_rel AS rel, account_invoice AS inv, account_journal AS aj2, account_account AS aa2 
					WHERE pay.id = rel.payment_id AND rel.invoice_id = inv.id AND inv.journal_id = aj2.id AND aj2.default_debit_account_id = aa2.id LIMIT 1)
				END) AS chartfield,
				line.partner_id,
				0 as invoice,
				pay.name as reference,
				pay.people_soft_registered as registered,
				/*Hacemos una consulta a la factura asociada al pago para obtener el journal 
				y asi identificar si viene de BCI o STRI para luego guardarlo en la columna doc_type*/
				(SELECT CASE WHEN partner.customer_type = 'fund' 
				THEN -1 ELSE (
					SELECT inv.journal_id FROM account_invoice_payment_rel AS rel, account_invoice AS inv 
					WHERE pay.id = rel.payment_id AND rel.invoice_id = inv.id LIMIT 1) 
				END) as doc_type,
				'refund' as document, /* hacemos que el pago sea tratado como una nota credito*/
				(SELECT CASE WHEN account.user_type_id = (SELECT id FROM account_account_type WHERE name = 'Receivable' LIMIT 1) THEN 0 ELSE 1 END) AS sub_order,
				(SELECT (CASE WHEN line.credit > 0.00 THEN (line.credit * -1) WHEN line.debit > 0.00 THEN line.debit ELSE 0.00 END )) AS amount
			FROM account_move_line AS line, account_payment as pay, res_partner AS partner, account_account AS account, account_journal as journal
			WHERE (line.date BETWEEN '{}' AND '{}') AND line.partner_id = partner.id AND line.payment_id = pay.id
				AND pay.journal_id = journal.id AND line.account_id = account.id 
				AND journal.default_debit_account_id in (SELECT AA2.id FROM account_account as AA2, account_account_type AS AT2 WHERE AA2.user_type_id = AT2.id AND AT2.name = 'Expenses')
			ORDER BY id DESC)
		SELECT 'ACTUALS' Ledger, 
		split_part(chartfield, ',', 5) AS account,
		(SELECT CASE WHEN doc_type = -1 THEN (CONCAT('REIMB_', (SELECT CASE WHEN split_part(chartfield, ',', 5) = '6998' THEN '6998' ELSE '6999' END))) ELSE '' END) as entry_event,
		split_part(chartfield, ',', 1) AS fund,
		split_part(chartfield, ',', 3) AS dsgc,
		split_part(chartfield, ',', 2) AS budget_ref,
		split_part(chartfield, ',', 4) AS dept_id,
		ROUND(SUM(amount), 2) as amount,
		'USD' Currency,
		reference,
		split_part(chartfield, ',', 7) AS program,

		(SELECT CASE WHEN split_part(chartfield, ',', 6) != 'CLASSCODE' 
			THEN split_part(chartfield, ',', 6) 
			ELSE (SELECT cc.code FROM class_code AS cc, account_invoice AS ai WHERE ai.id = invoice AND ai.class_code = cc.id)
			END) AS class,

		split_part(chartfield, ',', 8) AS project,
		(SELECT CASE WHEN split_part(chartfield, ',', 8) = '' THEN '' ELSE 'SI000' END) AS proj_unit,
		split_part(chartfield, ',', 9) AS activity,
		split_part(chartfield, ',', 10) AS Analysis
		FROM people_soft_data
		WHERE {} {}
		GROUP BY Ledger, account, entry_event, fund, dsgc, budget_ref, dept_id, Currency, reference, program, class, project, proj_unit,activity, doc_type, Analysis, invoice, external_order, sub_order
		ORDER BY external_order DESC, sub_order DESC