import mysql.connector
mydb = mysql.connector.connect(host='localhost', user='root', password='Anandakumar_0962', database='amazon')
mycursor = mydb.cursor()

#Function to validate users
def validate_user(mail_id, password):
    mycursor.execute("select * from users where mail_id like %s", (mail_id,))
    user_data = mycursor.fetchall()
    if  user_data and user_data[0][-1] == password:
        print("Login Successful\n")
        print('--------------------------------------------------------------------------')
        return 1

#Function to display products based on their category.
def display_products():
    print('\n--------------------------------------------------------------------------')
    print('Categories:\n1. Mobile Phones \n2. Grocery \n3. Electronics \n4.Furnitures')
    category = int(input("\nChoose the category: "))
    if category == 1:
        mycursor.execute("select * from products where category like %s", ('Mobile Phones',))
        datas = mycursor.fetchall()
    elif category == 2:
        mycursor.execute("select * from products where category like %s", ('Grocery',))
        datas = mycursor.fetchall()
    elif category == 3:
        mycursor.execute("select * from products where category like %s", ('Electronics',))
        datas = mycursor.fetchall()
    elif category == 4:
        mycursor.execute("select * from products where category like %s", ('Furnitures',))
        datas = mycursor.fetchall()
    else:
        print("Invalid option.")
        return None
    print()
    print('--------------------------------------------------------------------------')
    product_ids = []
    for data in datas:
        print(f"{data[0]}. {data[1]} Rs {data[2]}/-", end='\n', sep='\n')
        product_ids.append(data[0])
    return select_products(product_ids)

#Function select products to order
def select_products(product_ids):
    selected_product_id = int(input("\nEnter the product id: "))
    if selected_product_id in product_ids:
        mycursor.execute("select * from products where product_id like %s", (selected_product_id,))
        data = mycursor.fetchall()
        if data:
            quantity = int(input("Enter quantity: "))
            if quantity > 0:
                cost = data[0][2]*quantity
                print('\n--------------------------------------------------------------------------')
                print("Order Preview:\n")
                print(f'Product Name: {data[0][1]} \nQuantity: {quantity} \nCost: {cost}')
                confirm_order = int(input("\nEnter 1 to confirm order: "))
                if confirm_order == 1:
                    return [selected_product_id, quantity, cost]
                else:
                    print('Invalid option')
                    return None
            else:
                print("Invalid Quantity")
                return None
    else:
        print("Invalid Product Id.")
        return None

#Function to confirm order
def place_order(mail_id,selected_product_id, quantity, cost):
    mycursor.execute('insert into orders values(null, %s, %s,%s,%s)', (mail_id, selected_product_id, quantity, cost,))
    mydb.commit()
    mycursor.execute('select * from orders where mail_id like %s', (mail_id,))
    data = mycursor.fetchall()
    mycursor.execute('select product_name from products where product_id like %s', (data[-1][2],))
    product_name = mycursor.fetchall()
    print('\n--------------------------------------------------------------------------')
    print(f'Mail_id: {mail_id} \nProduct Name: {product_name[0][0]} \nTotal Cost: {cost}\n \nOrder Successful')
    print('--------------------------------------------------------------------------')

#Function to display orders
def display_orders(mail_id):
    mycursor.execute('select * from orders where mail_id like %s', (mail_id,))
    data = mycursor.fetchall()
    if data:
        for i in range(len(data)):
            print(f'Order Id: {data[i][0]} | Mail Id: {data[i][1]} | Product Id: {data[i][2]} | Quantity: {data[i][3]} | Cost: {data[i][4]}')
    
    else:
        print("No Orders done.")
        print('--------------------------------------------------------------------------\n')


print("Welcome to Amazon Shopping")
print('--------------------------------------------------------------------------')
choice = input("\nLogin/Signup: ").title()
if choice == 'Login':
    mail_id = input("\nEnter the mail id: ")
    password = input("Enter the password: ")
    if validate_user(mail_id, password):
        stay_in = True
        while stay_in:
            print("1. Place an order \n2. My Orders \n3. Logout\n")
            choice = int(input("Select among the options: "))
            if choice == 1:
                product_details = display_products()
                if product_details:
                    place_order(mail_id, product_details[0], product_details[1], product_details[2])
            if choice == 2:
                display_orders(mail_id)
            if choice == 3:
                print("\nLogout Successfully")
                stay_in = False

    else:
        print("Invalid Mail Id / Password.")

elif choice == 'Signup':
    mail_id = input('\nEnter your mail id: ')
    user_name = input('Enter user name: ')
    phone_number = input('Enter your mobile number: ')
    password = input("Enter a strong password: ")
    #To avoid insertion of duplicate mail ids and errors by using try and except technique.
    try:
        mycursor.execute('insert into users values (null, %s, %s, %s, %s)', (mail_id, user_name, phone_number, password,))
        mydb.commit()
        print('Signed Up Successfully')
    except:
        print("Mail Id already exists.")