import datetime
import sys

# def logged(function):
#         def wrapper(*args, **kwargs):
#             value = function(*args, **kwargs)
#             with open('logfile.txt', '+a') as f:
#                 fname = function.__name__
#                 # print(f'{fname} returned value {value}')
#                 f.write(f'{fname} returned value {value}\n')
#             return value
#         return wrapper

class BookRental:
    
    def __init__(self, stock:int = 0):
        self.__stock = stock
    
    @property
    def stock(self) -> int:
        """The stock is a property with default value set to zero

        Args:
            stock: Number of books in stock. The default value is zero
            

        Returns:
            Number of books currently in stock
        """
        return self.__stock  
    
    @stock.setter
    def stock(self, val: int) -> int:
        """_summary_

        Args:
            val (int): Let user set new value of the book stock
        """
        self.__stock = val
    
    # @logged
    def display_books_stock(self):
        """A method to display the books in stock

        Returns:
            int: Returns the update book stock
        """
        print(f'There are {self.stock} books available for rent')
        return self.stock
    
    #@logged
    def rent_books(self, n: int):
        """ Specify the number of books to rent

        Args:
            param1 n (int): Specify the number of books to rent

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
            
    # @logged
    def return_books(self,n: int) -> int:
        """ Update the current stock and return the updated stock.

        Args:
            n (int): Number of books to return

        Returns:
            stock (int): Returns the updated book stock
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
        """ A property

        Returns:
            int: returns the number of books
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
            
                    
    # @logged    
    def request_books(self):
        """ A method to request books

        Returns:
            int : Returns the number of books requested
        """
        
        books = input("How many books do you wish to rent?: ")
                
        books = Customer.validate_choice(books)
        
        if books < 1:
            print("Please rent at least one book")
            return None
        else:
            self.books = books
            return self.books
    
    # @logged
    def return_books(self):
        """ A method to return the books

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
    

                
            
            