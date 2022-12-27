import pytest
from BookRental import Customer, BookRental

STOCK = 100

def test_display_books_stock():
    """ Test for negative value
    There should be minimum one book to return. It cannot be less than one.

    """
    
    book1 = BookRental(STOCK)
    assert STOCK == book1.display_books_stock()
    
    book2 = BookRental(0)
    assert 0 == book2.display_books_stock()
    
    book3 = BookRental(-1)
    assert -1 == book3.display_books_stock()


def test_rent_books():
    """ Test for negative value
    There should be minimum one book to return. It cannot be less than one.

    """
    rent = BookRental(STOCK)
    InStock = STOCK - rent.rent_books(50)
    assert 50 == InStock
    
    
def test_rent_books_negative():
    """ Test for negative value
    There should be minimum one book to return. It cannot be less than one.

    """
    rent = BookRental(STOCK)
    assert None == rent.rent_books(-5)
    
def test_rent_books_zero():
    """ Test for negative value
    There should be minimum one book to return. It cannot be less than one.

    """
    rent = BookRental(STOCK)
    assert None == rent.rent_books(0)
     
    
def test_return_books():
    """ Test for negative value
    There should be minimum one book to return. It cannot be less than one.

    """
    ret_book = BookRental(STOCK)
    assert 110 == ret_book.return_books(10)    

def test_return_books_negative():
    """ Test for negative value
    There should be minimum one book to return. It cannot be less than one.

    """
    ret_book = BookRental(STOCK)
    assert 95 == ret_book.return_books(-5)


def test_return_books_zero():
    """ Test for negative value
    There should be minimum one book to return. It cannot be less than one.

    """
    return_book = BookRental(STOCK)
    assert 100 == return_book.return_books(0)