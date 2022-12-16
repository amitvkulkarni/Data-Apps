import datetime
import sys

def logged(function):
        def wrapper(*args, **kwargs):
            value = function(*args, **kwargs)
            with open('logfile.txt', '+a') as f:
                fname = function.__name__
                # print(f'{fname} returned value {value}')
                f.write(f'{fname} returned value {value}\n')
            return value
        return wrapper

class BookRental:
    
    def __init__(self, stock = 0):
        self.__stock = stock
    
    @property
    def stock(self):
        """The stock value is readonly

        Returns:
            int: Returns the book stock
        """
        return self.__stock  
    
    @stock.setter
    def stock(self, val):
        """_summary_

        Args:
            val (int): Let user set new value of the book stock
        """
        self.__stock = val
    
    @logged
    def display_books_stock(self):
        """A method to display the books in stock

        Returns:
            int: Returns the update book stock
        """
        print(f'There are {self.stock} books available for rent')
        return self.stock
    
    @logged
    def rent_books(self, n: int):
        """_summary_

        Args:
            n (int): Number books to be rented

        Returns:
            int: Returns the updated book stock
        """
        
        if n <=0:
            print("Number of books should be at least one")
            return None
        elif n > self.stock:
            print(f'Sorry we only have {self.stock} books available to rent')
            return None
        else:
            now = datetime.datetime.now()
            print(f'You have successfully rented {n} books')
            self.stock -= n
            print(f'Current available stock is {self.stock} ')
            # return now
            return self.stock
            
    @logged
    def return_books(self,n):
        """_summary_

        Args:
            n (_type_): _description_

        Returns:
            int: Returns the updated book stock
        """
        self.stock += n
        print(f'You have successfully returned {n} books')
        print(f'Current available stock is {self.stock}')
        # return 0
        return self.stock
        
    

class Customer:
    def __init__(self):
        self.__books = 0
          
    
    @property
    def books(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__books
    
    @books.setter
    def books(self, val):
        self.__books = val
    
    @staticmethod
    def validate_choice(val):
        try:
            val = int(val)
            return val
        except ValueError:
            print("Enter valid input")
            
                    
    @logged    
    def request_books(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        
        books = input("How many books do you wish to rent?: ")
                
        books = Customer.validate_choice(books)
        
        if books < 1:
            print("Please rent at least one book")
            return None
        else:
            self.books = books
            return self.books
    
    @logged
    def return_books(self):
        """_summary_

        Returns:
            int: Number of books to return
        """
        return_books = input("How many books do you wish to return?: ")
               
        return_books = Customer.validate_choice(return_books)
        
        if return_books < 1:
            print("You need at least one book to return")
            return None
        else:
            return return_books
    

                
            
            