def calculate_total(products, discount = 0):
    total = 0
    for product in products:
        total += product['price']
    if discount > 0:
        total -= total * (discount/100)
    return total
    
def test_calculate_total_with_empty_list():
    assert calculate_total([]) == 0

def test_calculate_total_with_single_product():
    products = [
        {
            "Name": "Notebook", "price": 5
        }
    ]
    assert calculate_total(products) == 5

def test_calculate_total_with_multiple_product():
    products = [
        {
            "Name": "Book", "price": 10
        },
        {
            "Name": "Pen", "price": 2
        },
        {
            "Name": "Pencil", "price": 4
        },
        {
            "Name": "Erased", "price": 5
        }
    ]
    assert calculate_total(products) == 21

def test_calculate_total_with_discount():
    products = [
        {
            "Name": "Book", "price": 10
        },
        {
            "Name": "Pen", "price": 2
        },
        {
            "Name": "Pencil", "price": 4
        },
        {
            "Name": "Eraser", "price": 5
        }
    ]
    assert calculate_total(products, discount=10) == 18.9  

if __name__ == "__main__":
    test_calculate_total_with_empty_list()
    test_calculate_total_with_single_product()
    test_calculate_total_with_multiple_product()
    test_calculate_total_with_discount()