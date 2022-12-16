from BookRental import BookRental, Customer


def main():
    """
    The main function initiating the objects and the process
    """
    
    book = BookRental(100)
    customer = Customer()
    
       
    while True:
        print("""
        ====== Book Rental Service =======
        1. Display available books
        2. Request books
        3. Return books
        4. Exit
        """)
        choice = input("Enter your choice: ")
        
        try:
            choice = int(choice)
        except ValueError:
            print("Error with data type")
            continue
        
        if choice == 1:
            book.display_books_stock()
        elif choice == 2:
            book.rent_books(customer.request_books())
        elif choice == 3:
            book.return_books(customer.return_books())
        else:
            break

    print("Thank you for using the book rental service.")



if __name__ == '__main__':
    main()