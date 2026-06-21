#Travel Agency Data Analysis Program

import mysql.connector
import matplotlib.pyplot as plt


#array for data
data = []

#functions

#load data from database
def loadData():

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sasha101!",
            database="TravelAgency"
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT Destination,
                   Bookings,
                   Revenue,
                   Rating
            FROM Destinations
        """)

        rows = cursor.fetchall()

        data.clear()

        for row in rows:
            data.append({
                "destination": row[0],
                "bookings": row[1],
                "revenue": float(row[2]),
                "rating": row[3]
            })

        print("Database data loaded successfully!")

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print("Database Error:", err)


#Menu Display function
def displayMenu():
    print("\n==========================================")
    print("\nTravel Agency Data Analysis Menu")
    print("\n==========================================")
    print("\n1. Return Destination Results")
    print("\n2. Display Highest Revenue Results")
    print("\n3. Display Average Revenue Results")
    print("\n4. Display Customer Type Report")
    print("\n5. Show Bookings Pie Chart")
    print("\n6. Show Customer Ratings Bar Graph")
    print("\n7. Show all destination data")
    print("\n8. Exit")

    choice = int(input("\nEnter your choice: "))
    return choice

#option 1: Return destination results
def destinationResults():
    destination = input("\nEnter Destination Name: ")

    found = False

    for trip in data:
        if trip["destination"].lower() == destination.lower():
            print("\nDestination:", trip["destination"])
            print("Bookings: ", trip["bookings"])
            print("Revenue: ", trip["revenue"])
            print("Rating: ", trip["rating"])

            found = True

            if not found:
                print("Destination not found")

#option 2: Display highest revenue results
def highestRev():
    highestRev = max(data, key=lambda x: x["revenue"])

    print("\nHighest Revenue Destination")
    print("==============================")
    print("Destination: ", highestRev["destination"])
    print("Revenue: $", (highestRev["revenue"])*(highestRev["bookings"]))

#Option 3: Display average revenue results
def averageRev():
    totalRev = sum(item["revenue"] for item in data)
    averageRev = round(totalRev / len(data), 2)

    print("\nAverage Revenue: $", averageRev)

#Option 4: Display Customer Type Report
def customerTypeReport():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sasha101!",
        database="TravelAgency"
    )
    cursor = connection.cursor()

    query = """
    SELECT CustomerType,
           COUNT(*) AS Travelers
    FROM Customers
    GROUP BY CustomerType
    ORDER BY Travelers DESC
    """

    cursor.execute(query)

    print("\nCustomer Type Report")
    print("====================")

    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")

    cursor.close()
    connection.close()

#option 5: Bookings Pie Chart
def bookingsPieChart():
    destinations = [items["destination"] for items in data]
    bookings = [items["bookings"] for items in data]

    plt.pie(bookings, labels=destinations, autopct='%1.1f%%')
    plt.title("Bookings by Destination")
    plt.show()

#Option 6: Customer Ratings Bar Graph
def ratingsBarGraph():
    destinations = [items["destination"] for items in data]
    ratings = [items["rating"] for items in data]

    plt.figure(figsize=(8, 6))

    plt.barh(destinations, ratings)

    plt.title("Ratings by Destination")
    plt.xlabel("Rating")
    plt.ylabel("Destination")
    plt.xlim(0, 5)

    plt.tight_layout()
    plt.show()

#Opt 7: Show all data
def showAllData():
    print("All Destination Data:")
    print("Destination | Booking | Revenue | Rating")
    print("=========================================================")

    for item in data:
        print(item['destination'],"|", item['bookings'],"|", item['revenue'],"|", item['rating'])



#Main program
def main():
    loadData()

    while True:
        choice = displayMenu()

        if choice == 1:
            destinationResults()

        elif choice == 2:
            highestRev()

        elif choice == 3:
            averageRev()

        elif choice == 4:
            customerTypeReport()

        elif choice == 5:
            bookingsPieChart()

        elif choice == 6:
            ratingsBarGraph()

        elif choice == 7:
            showAllData()

        elif choice == 8:
            print("Thank you for using Travel Management")
            break

        else:
            print("Invalid choice. Please enter a valid choice.")


main()