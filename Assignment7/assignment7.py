import pyodbc
import uuid ## for unique review id

#################################################################
# Connect to database
conn = pyodbc.connect ('driver={SQL Server};Server=cypress.csil.sfu.ca;user=s_minzhih; password=2n4ytfQ7RnL3hHre;Trusted_Connection=yes;')
# Create a cursor
cur = conn.cursor()

# Create the table
print ("")
print("Connection To Yelp Database Successfully Established")
## Helper function for login function
def verifyLogin(userid):
    query="SELECT user_id, name FROM user_yelp WHERE user_id=?"
    cur.execute(query, (userid,))
    user = cur.fetchone()
    if user:
        return user
    else:
        return False

#Function1: login
def Login():
    print ("")
    print(" ----------- ** Welcome to login page, user ** ----------- ")

    while True:
        print ("")
        user_id = input("Please provide your Yelp user id or type exit to exit: ")
        if user_id.lower() == "exit":
            break
        user = verifyLogin(user_id)
        if user:
            print ("")
            print(f"Hi {user[1]}, welcome to Yelp!")
            global curr_user
            curr_user = user[0]
            print ("")
            print(f"System Tracking: Current global userid is {user[0]}")
            return user[0]
        else:
            print ("")
            print("Invalid user ID. Any enter else than exit would ask you to provide the user id again.")

#Function2: Search Business
def SearchBusiness():
    print ("")
    
    min_star_valid = False
    max_star_valid = False
    
    # Assign a default minimum stars value to use
    min_star_query = "SELECT MIN(stars) FROM business"
    cur.execute(min_star_query)
    default_min = cur.fetchone()[0]

    # Assign a default maximum stars value to use
    max_star_query = "SELECT MAX(stars) FROM business"
    cur.execute(max_star_query)
    default_max = cur.fetchone()[0]

    while not min_star_valid:
        min_star = input('Please give me the minimal stars, or press Enter to skip : ')
        print('*Note minimal stars would be 0 if skip*')

        if not min_star:
            min_star_query= "SELECT MIN(stars) FROM business"
            cur.execute(min_star_query)
            min_star= cur.fetchone()[0]

        else:
            if (not min_star.isnumeric()) or (int(min_star) < 1) or (int(min_star) > 5):
                print("Error: The stars must be a valid number from 1 to 5")
            else:
                min_star_valid = True
    
    print ("")
    while not max_star_valid:
        max_star = input('Please give me the maximum stars, or press Enter to skip: ')
        print('*Note maximum stars would be 5 if skip*')
        
        if not max_star:
            max_star_query= "SELECT MAX(stars) FROM business"
            cur.execute(max_star_query)
            max_star= cur.fetchone()[0]

        else:
            if (not max_star.isnumeric()) or (int(max_star)>5) or (int(max_star)<1):
                print("Error: The stars must be a valid number from 1 to 5")
            else:
                max_star_valid = True
    
    print ("")
    city = input('Please provide the name of the city, or hit enter to skip: ')
    if not city:
        city = "%"
    else:
        city = '%'+ city +'%'

    print ("")
    name = input('Please provide the name of the business, or hit enter to skip: ')
    if not name:
        name = '%'
    else:
        name = '%' + name +'%'

    query = "SELECT business_id, name, address, city, stars FROM business WHERE city LIKE ? AND name LIKE ? AND stars <=? AND stars >=? ORDER BY name;"
    cur.execute(query, (city, name, max_star, min_star))

    all_bus = cur.fetchall()

    if not all_bus:
        print ("")
        print("No businesses found.")
        return "----------Done----------"

    for row in all_bus:
        print(f"Business ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Address: {row[2]}")
        print(f"City: {row[3]}")
        print(f"Stars: {row[4]}\n")

    return "---------Done----------"

## Helper function for Seach User function
def attribute(attribute_name):
    valid = False
    while not valid:
        print ("")
        attr_value = input(f"Please provide if the user is {attribute_name} or not (Yes/No), Note: Yes for {attribute_name} value greater than zero, No for not: ")
        try:
            attr_value = str(attr_value)
            attr_value = attr_value.strip().lower()
            if attr_value.lower() == 'yes':
                valid = True
                return f"{attribute_name} > 0"
            elif attr_value == 'no':
                valid = True
                return f"{attribute_name} = 0"
            else:
                print("Invalid input. Please enter 'Yes' or 'No'.")

        except ValueError:
            if not attr_value:
                return f"{attribute_name} = 0"
            print(f"Invalid input. Please enter 'Yes' or 'No'.")

#Function3: Search User
def SearchUsers():
    print ("")
    name = input('Please provide the user name key word:').strip()
    name = f"%{name.lower()}%" if name else '%'

    query = f"""SELECT user_id, name, useful, funny, cool, yelping_since FROM user_yelp WHERE name LIKE ? and {attribute('useful')}
                and {attribute('funny')} and {attribute('cool')} ORDER BY name;"""
    cur.execute(query, [name,])
    global all_user
    all_user = cur.fetchall()

    if len(all_user) == 0:
        print ("")
        print("No user found.")
        return '----------Done----------'

    else:
        print('-' * 80)
        for row in all_user:
            print(f"User ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Useful: {row[2]}")
            print(f"Funny: {row[3]}")
            print(f"Cool: {row[4]}\n")
            print(f"Yelping_Since: {row[5]}\n")
        print ("")
        return '----------Done----------'

#Function 4 Make friend
def MakeFriend():
    print ("")

    """
    try:
        if len(all_user) != 0:
            print("Here are the user you searched before!")
            for row in all_user:
                print ("")
                print(f"User ID: {row[0]}")
                print(f"Name: {row[1]}")
            print('----------Done----------')
    
        else:
            print("You did have any pervious searched friend. Please search again and then make friend!")
            return 'Please select function Search User again.'

    except NameError:
        print("You have not searched for any user yet. Please search for a user first.")
        return 'Please select function Search User first.'
    """

    while True:
        print ("")
        friend = input('Hi, which user do you want to make friend with? Please provide their user ID: ')
        if not friend:
            print ("")
            print('Empty input. Please enter a valid user ID.')
            continue
        
        query_user = "SELECT user_id FROM user_yelp WHERE user_id=?"
        cur.execute(query_user, (friend,))
        if not cur.fetchone():
            print ("")
            print(f'No such user found. Please enter a valid user ID.')
            continue

        query = "INSERT INTO friendship VALUES (?, (SELECT user_id FROM user_yelp WHERE user_id=?))"
        
        try:
            cur.execute(query, (curr_user, friend))
            conn.commit()
            print ("")
            return f'Hi, {friend} is a friend with you now!'
        except Exception as e:
            print ("")
            return 'You could not make friend with someone already your friend.'

# Funciton 5: Write Review
def WriteReview():
    while True:
        print ("")
        business_id = input('Please enter the business ID of the business you want to review for:')
        if business_id:
            # Check if business_id is valid
            query = "SELECT COUNT(*) FROM business WHERE business_id = ?"
            cur.execute(query, [business_id])
            row = cur.fetchone()[0]
            if not row:
                print ("")
                print('Invalid business_id. Please try again.')
            else:
                break
        else:
            print ("")
            print('Must enter a business_id for review. Please try again.')

    while True:
        print ("")
        stars = input('Please give a star rating, range from 1 to 5: ')
        try:
            stars = float(stars)
            if 0 < stars <= 5:
                break
            else:
                print ("")
                print('Star rating must be between 1 and 5. Please try again.')
        except ValueError:
            print('Invalid input. Please enter a number between 1 and 5 for rating.')

    review_id = ''
    while len(review_id) == 0:
        temp =  str(uuid.uuid4())[:22]
        query = "SELECT review_id FROM review WHERE review_id=?"
        cur.execute(query, [temp])
        row = cur.fetchone()
        if not row:
            review_id = temp
            break
    
    query = "INSERT INTO review (review_id, business_id, user_id, stars) values ('{0}', '{1}', '{2}', {3})".format(review_id,business_id,curr_user,stars)
    cur.execute(query)
    conn.commit()
    print ("")
    return 'Review inserted succussfully!'

def main():
    if not Login():
        print ("")
        print("Goodbye!")
        return

    running = True
    while running:
        print ("")
        print('Please select one of the following function')
        print ("")
        print('0. Exit')
        print('1. Search Busniess')
        print('2. Search User')
        print('3. Make Friend')
        print('4. Write Reivew')
        print ("")
        user_input = input('Please select from 0 to 4: ')
        print ("")
        print('You selected function: '+user_input)
        if int(user_input)==0:
            print ("")
            print('Exited. Goodbye.')
            running=False
        elif int(user_input) == 1:
            print ("")
            print('Going to Search Busniess function')
            print (SearchBusiness())
        elif int(user_input) ==2:
            print ("")
            print('Going to Search Users function')
            print(SearchUsers())
        elif int(user_input)==3:
            print ("")
            print('Going to Make Friend function')
            print(MakeFriend())
        elif int(user_input) == 4:
            print ("")
            print('Going to Write Reivew function')
            print(WriteReview())
        else:
            print ("")
            print('Invalid input, please select from 0-4.')

main()

conn.close()
print("Connection closed")
# close connection
