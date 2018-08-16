#start by import the package we need
import os, csv

#define resources path
csv_path = os.path.join("..", "Resources", "budget_data.csv")

#define variables
total_months = 0
total_revenue = 0
revenue_change_list = []
prev_month_revenue = 0
greatest_increase_month = ""
greatest_decrease_month = ""
greatest_increase_revenue = 0
greatest_decrease_revenue = 0


#make csv file an iteratable object, use dictionary type of reader
with open(csv_path, newline="", encoding="UTF-8") as csvfile:
    csv_reader = csv.DictReader(csvfile, delimiter=",")
    
    #looping
    for row in csv_reader:
        #find total months
        total_months += 1
        #find total revenue
        total_revenue = total_revenue + int(row["Profit/Losses"])
        #find revenue change for each month using if statement
        revenue_change = int(row["Profit/Losses"]) - prev_month_revenue
        if total_months > 1:
            revenue_change_list.append(revenue_change)
        
        #pre_month_revenue need to be the new value, not 0
        prev_month_revenue = int(row["Profit/Losses"])

        #find greatest revenue_change increase
        if revenue_change > greatest_increase_revenue:
            greatest_increase_revenue = revenue_change
            #find greatest increase month
            greatest_increase_month = row["Date"]
        #find greatest revenue_change decrease
        if revenue_change < greatest_decrease_revenue:
            greatest_decrease_revenue = revenue_change
            #find greatest decrease month
            greatest_decrease_month = row["Date"]

#find the FINAL revenue change average, sum / length
revenue_average = round(sum(revenue_change_list) / len(revenue_change_list), 2)



#define output format
print("\nFinancial Analysis") 
print("-------------------")
print(f"Total Months: {total_months}")
print(f"Total: ${total_revenue}")
print(f"Average Change: ${revenue_average}")
print(f"Greatest Increase in Profits: {greatest_increase_month} (${greatest_increase_revenue})")
print(f"Greatest Decrease in Profits: {greatest_decrease_month} (${greatest_decrease_revenue})")

#export a text.file
output_path = "../Output/Business_Data_Analysis.txt"
with open(output_path, "w") as text_file:
    text_file.write("Financial Analysis")
    text_file.write("\n")
    text_file.write("-------------------")
    text_file.write("\n")
    text_file.write(f"Total Months: {total_months}")
    text_file.write("\n")
    text_file.write(f"Total: ${total_revenue}")
    text_file.write("\n")
    text_file.write(f"Average Change: ${revenue_average}")
    text_file.write("\n")
    text_file.write(f"Greatest Increase: {greatest_increase_month} (${greatest_increase_revenue})") 
    text_file.write("\n")
    text_file.write(f"Greatest Increase: {greatest_decrease_month} (${greatest_decrease_revenue})")
