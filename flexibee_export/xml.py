import xml.etree.ElementTree as ElementTree


def export(order_id,
           variable_symbol,
           currency_code,
           currency_string,
           date_created,
           description,
           payment_method_code,
           payment_method_name,
           payment_price,
           shipping_method_code,
           shipping_method_name,
           shipping_price,
           shipping_first_name,
           shipping_last_name,
           shipping_street,
           shipping_city,
           shipping_zip,
           shipping_country,
           phone,
           reg_number,
           vat_number,
           email,
           same_shipping_as_billing,
           billing_first_name,
           billing_last_name,
           billing_company_name,
           billing_street,
           billing_city,
           billing_zip,
           billing_country,
           order_items_dict,
           ):
    root = ElementTree.Element('winstrom', attrib={'version': '1.0'})

    invoice = ElementTree.SubElement(root, 'faktura-vydana')
    ElementTree.SubElement(invoice, 'id').text = "ext:ESHOP:{}".format(order_id)
    ElementTree.SubElement(invoice, 'mena',
                           showAs='{}: {}'.format(currency_code, currency_string)).text = "code:{}".format(
        currency_code)
    ElementTree.SubElement(invoice, 'datObjednavky').text = date_created.isoformat()

    ElementTree.SubElement(invoice, 'varSym').text = str(variable_symbol)
    ElementTree.SubElement(invoice, 'formaUhradyCis').text = "code:{}".format(payment_method_code)
    ElementTree.SubElement(invoice, 'formaDopravy').text = "code:{}".format(shipping_method_code)
    ElementTree.SubElement(invoice, 'popis').text = description
    ElementTree.SubElement(invoice, 'typDokl', showAs="FAKTURA: Faktura - daňový doklad").text = "code:FAKTURA"
    ElementTree.SubElement(invoice, 'nazev').text = "{}{}_{}".format(shipping_first_name,
                                                                  shipping_last_name,
                                                                  variable_symbol)
    ElementTree.SubElement(invoice, 'nazFirmy').text = "{} {}".format(shipping_first_name,
                                                                   shipping_last_name)
    ElementTree.SubElement(invoice, 'ulice').text = "{}".format(shipping_street)
    ElementTree.SubElement(invoice, 'mesto').text = "{}".format(shipping_city)
    ElementTree.SubElement(invoice, 'psc').text = "{}".format(shipping_zip)
    ElementTree.SubElement(invoice, 'stat').text = "code: {}".format(shipping_country)

    ElementTree.SubElement(invoice, 'ic').text = reg_number
    ElementTree.SubElement(invoice, 'dic').text = vat_number
    #
    ElementTree.SubElement(invoice, 'kontaktTel').text = str(phone)
    ElementTree.SubElement(invoice, 'kontaktEmail').text = email

    ElementTree.SubElement(invoice, 'postovniShodna').text = str(same_shipping_as_billing).lower()

    if not same_shipping_as_billing:
        ElementTree.SubElement(invoice,
                               'faNazev').text = billing_company_name or billing_first_name + " " + billing_last_name
        ElementTree.SubElement(invoice, 'faUlice').text = billing_street
        ElementTree.SubElement(invoice, 'faMesto').text = billing_city
        ElementTree.SubElement(invoice, 'faPsc').text = billing_zip
        ElementTree.SubElement(invoice, 'faStat').text = "code: {}".format(billing_country)

    items = ElementTree.SubElement(invoice, "polozkyFaktury", removeAll='True')
    for key, item in order_items_dict.items():
        invoice_item = ElementTree.SubElement(items, "faktura-vydana-polozka")
        ElementTree.SubElement(invoice_item, "typPolozkyK").text = "typPolozky.obecny"
        ElementTree.SubElement(invoice_item, "typCenyDphK", showAs="včetně DPH").text = "typCeny.sDph"
        ElementTree.SubElement(invoice_item, "typSzbDphK").text = "typSzbDph.dphZakl"
        ElementTree.SubElement(invoice_item, "szbDph").text = item.get('tax')
        ElementTree.SubElement(invoice_item, "mena",
                               showAs='{}:{}'.format(currency_code,
                                                      currency_string)).text = "code: {}".format(currency_code)
        ElementTree.SubElement(invoice_item, "typUcOp",
                               showAs="DP1-ZBOŽÍ: Prodej zboží a výrobků").text = "code: DP1-ZBOŽÍ"
        ElementTree.SubElement(invoice_item, "kopDanEvid").text = "True"
        ElementTree.SubElement(invoice_item, "nazev").text = item.get('name')
        ElementTree.SubElement(invoice_item, "kod").text = str(item.get('code'))
        ElementTree.SubElement(invoice_item, "mnozMj").text = str(item.get('quantity'))
        ElementTree.SubElement(invoice_item, "cenaMj").text = str(item.get('price'))
        ElementTree.SubElement(invoice_item, "poznam").text = item.get('note', None)

    # payment and shipping
    payment_and_shipping_price = payment_price + shipping_price
    if payment_and_shipping_price > 0:
        invoice_item = ElementTree.SubElement(items, "faktura-vydana-polozka")
        ElementTree.SubElement(invoice_item, "typPolozkyK").text = "typPolozky.obecny"
        ElementTree.SubElement(invoice_item, "typCenyDphK", showAs="včetně DPH").text = "typCeny.sDph"
        ElementTree.SubElement(invoice_item, "typSzbDphK").text = "typSzbDph.dphZakl"
        ElementTree.SubElement(invoice_item, "szbDph").text = "21"
        ElementTree.SubElement(invoice_item, "mena",
                               showAs="{}:{}".format(currency_code,
                                                      currency_string)).text = "code: {}".format(currency_code)
        ElementTree.SubElement(invoice_item, "typUcOp",
                               showAs="DP1-ZBOŽÍ: Prodej zboží a výrobků").text = "code:DP1-ZBOŽÍ"
        ElementTree.SubElement(invoice_item, "kopDanEvid").text = "True"
        ElementTree.SubElement(invoice_item, "nazev").text = "{} - {} - {}".format(shipping_country,
                                                                                   payment_method_name,
                                                                                   shipping_method_name)
        ElementTree.SubElement(invoice_item, "kod")
        ElementTree.SubElement(invoice_item, "mnozMj").text = "1"
        ElementTree.SubElement(invoice_item, "cenaMj").text = str(payment_and_shipping_price)
        ElementTree.SubElement(invoice_item, "poznam")

    # write file
    mydata = ElementTree.tostring(root, encoding="unicode")
    return mydata
