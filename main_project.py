import pandas as pd
import matplotlib.pyplot as plt

print("Pandas imported successfully!")
print("Matplotlib imported successfully!")

read = pd.read_csv("hotel_sales.csv")

print(read)


# Check the data
read["RoomsSold"] = pd.to_numeric(read["RoomsSold"], errors="coerce")
read["Rate"] = pd.to_numeric(read["Rate"], errors="coerce")
read["Date"] = pd.to_datetime(read["Date"], errors="coerce")

# Find incorrect rows
invalid = (
    read["RoomsSold"].isna() |
    read["Rate"].isna() |
    read["Date"].isna() |
    (read["RoomsSold"] < 0) |
    (read["Rate"] < 0) |
    read["RoomType"].isna() |
    (read["RoomType"].astype("string").str.strip() == "")
)

# Show warning
for index in read[invalid].index:
    print("Warning: Row", index + 2, "skipped.")

# Remove incorrect rows
read = read[~invalid].copy()

print("Valid records analysed:", len(read))

if read.empty:
    print("No valid records found.")
    raise SystemExit

read["Date"] = read["Date"].dt.strftime("%Y-%m-%d")



# Calculate revenue for each room
read["Revenue"] = read["RoomsSold"] * read["Rate"]

print("\nHotel Revenue:")
print(read)


# Calculate total revenue
total = read["Revenue"].sum()

print("\nTotal Hotel Revenue: Rs.", total)


# Calculate revenue for each day
daily = read.groupby("Date")["Revenue"].sum()

print("\nDaily Revenue:")
print(daily)


# Find the day with the highest revenue
if len(daily) > 0:
    best_day = daily.idxmax()

    print("\nBest Performing Day:")
    print(best_day)
    print("Revenue: Rs.", daily.max())


# Calculate revenue for each room type
room_type = read.groupby("RoomType")["Revenue"].sum()

print("\nRevenue by Room Type:")
print(room_type)


# Calculate percentage of revenue
if total > 0:
    percentage = (room_type / total) * 100

    print("\nRevenue Percentage:")
    print(percentage.round(2))
else:
    print("\nRevenue percentage cannot be calculated.")


# Main Menu
while True:
    print("\n===== HOTEL REVENUE ANALYZER =====")
    print("1. Daily Revenue")
    print("2. Revenue by Room Type")
    print("3. Show Charts")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\nDaily Revenue:")
        print(daily)
        print("Total Revenue: Rs.", total)
        print("Best Day:", daily.idxmax())
        print("Best Revenue: Rs.", daily.max())

    elif choice == "2":
        print("\nRevenue by Room Type:")
        print(room_type)
        print("\nRevenue Percentage:")
        print(percentage.round(2))

    elif choice == "3":
        print("Showing Hotel Revenue Charts...")

        daily.plot(kind="bar", title="Daily Revenue")
        plt.xlabel("Date")
        plt.ylabel("Revenue (Rs.)")
        plt.tight_layout()
        plt.show()

        if total > 0:
            room_type.plot(kind="pie", autopct="%1.2f%%")
            plt.title("Revenue by Room Type")
            plt.ylabel("")
            plt.show()

    elif choice == "4":
        print("Thank you for using Hotel Revenue Analyzer!")
        break

    else:
        print("Invalid choice. Try again.") 
