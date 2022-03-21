from src.utils.item_price import item_price

def get_store_message(store_data):

    store_faved_msg = "STORE PREFERITI\n\n"
    for store in store_data:
                
        item = store['item']['item_id']
        minor_units = store['item']['price_including_taxes']['minor_units']
        decimal = store['item']['price_including_taxes']['decimals']
        price = item_price(minor_units, decimal)
        store_id = store['store']['store_id']
        store_name = store['store']['store_name']

        items_available = store['items_available']
                    
        store_faved_msg += "%s [%s]\n" % (store_name, store_id)
        store_faved_msg += "Prezzo: %s€\n" % price
        store_faved_msg += "Magicbox disponibili: %s\n\n" % items_available

    return store_faved_msg