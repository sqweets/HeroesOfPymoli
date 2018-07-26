
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# Raw data file
file_to_load = "Resources/purchase_data.csv"

# Read purchasing file and store into pandas data frame
purchases_df = pd.read_csv(file_to_load)


# In[2]:


purchases_df.head(10)


# ## Player Count

# * Display the total number of players
# 

# In[3]:


# The data is for purchases so it will only have players that have made purchases
# and will likely be less than the total active player count stated above since players can make more than one purchase

total_players = len(purchases_df.SN.unique())
print(f'Total # of players that have made purchases: {total_players}')


# ## Purchasing Analysis (Total)

# # * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[4]:


# Create dataFrame of unique products
unique_items_df = purchases_df.loc[purchases_df["Item ID"].unique()].copy()
num_products = unique_items_df['Item ID'].count()
avg_price = purchases_df['Price'].mean()
num_purchases = purchases_df['Purchase ID'].count()
total_revenue = purchases_df['Price'].sum()

summary_df = pd.DataFrame({"Number of Products": [num_products],
                           "Average Price": [avg_price],
                           "Total Purchases": [num_purchases],
                           "Total Revenue": [total_revenue]   
                           })

summary_df["Average Price"] = summary_df["Average Price"].map("${:.2f}".format)
summary_df["Total Revenue"] = summary_df["Total Revenue"].map("${:.2f}".format)

summary_df


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[5]:


# Groupby gender and count unique players
groupedby = purchases_df.groupby(['Gender'])
gender_counts = groupedby['SN'].nunique()
sum_gender_counts = gender_counts.sum()

female_count = gender_counts['Female']
female_percent = (female_count/sum_gender_counts) * 100

male_count = gender_counts['Male']
male_percent = (male_count/sum_gender_counts) * 100

other_count = gender_counts['Other / Non-Disclosed']
other_percent = (other_count/sum_gender_counts) * 100

gender_df = pd.DataFrame(gender_counts)
gender_df['Percents'] = [female_percent, male_percent, other_percent]
gender_df["Percents"] = gender_df["Percents"].map("{:.2f}%".format)
gender_df.columns = ["Total Count", "Percentage"]

gender_df


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[6]:


# see what each player has bought
# By Gender (totals)
total_item_count_by_gender = purchases_df.groupby('Gender')['Item ID'].count()
total_spent_by_gender = purchases_df.groupby('Gender')['Price'].sum()
max_cost_by_gender = purchases_df.groupby('Gender')['Price'].max()
min_cost_by_gender = purchases_df.groupby('Gender')['Price'].min()
avg_cost_by_gender = purchases_df.groupby('Gender')['Price'].mean()

avg_spent_by_female = total_spent_by_gender.Female / gender_counts.Female
avg_spent_by_male = total_spent_by_gender.Male / gender_counts.Male
avg_spent_by_other = total_spent_by_gender["Other / Non-Disclosed"] / gender_counts["Other / Non-Disclosed"]

myList = [{"Total Items": total_item_count_by_gender.Female, "Total Purchases": total_spent_by_gender.Female,
            "Avg Spent per Player": avg_spent_by_female, "Unique Players": gender_counts.Female},
           {"Total Items": total_item_count_by_gender.Male, "Total Purchases": total_spent_by_gender.Male,
            "Avg Spent per Player": avg_spent_by_male, "Unique Players": gender_counts.Male},
           {"Total Items": total_item_count_by_gender["Other / Non-Disclosed"],
            "Total Purchases": total_spent_by_gender["Other / Non-Disclosed"], "Avg Spent per Player": avg_spent_by_other,
            "Unique Players": gender_counts["Other / Non-Disclosed"]}]

gender_totals_df = pd.DataFrame(myList)
gender_totals_df.rename(index={0:'Female', 1:'Male', 2:'Other'}, inplace=True)

gender_totals_df["Total Purchases"] = gender_totals_df["Total Purchases"].map("${:.2f}".format)
gender_totals_df["Avg Spent per Player"] = gender_totals_df["Avg Spent per Player"].map("${:.2f}".format)
# Change column order
gender_totals_df = gender_totals_df[['Unique Players','Total Items', 'Total Purchases', 'Avg Spent per Player']]

gender_totals_df


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[7]:


# Establish bins for ages
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

purchases_df["Age Ranges"] = pd.cut(purchases_df["Age"], age_bins, labels=group_names)

groupedby_ages = purchases_df.groupby('Age Ranges')
age_counts = groupedby_ages['SN'].nunique()   
total_unique_players = age_counts.sum()

age_list = [{"Unique Players": age_counts["<10"], "Percentage": (age_counts["<10"] * 100) / total_unique_players},
            {"Unique Players": age_counts["10-14"], "Percentage": (age_counts["10-14"] * 100) / total_unique_players},
            {"Unique Players": age_counts["15-19"], "Percentage": (age_counts["15-19"] * 100) / total_unique_players},
            {"Unique Players": age_counts["20-24"], "Percentage": (age_counts["20-24"] * 100) / total_unique_players},
            {"Unique Players": age_counts["25-29"], "Percentage": (age_counts["25-29"] * 100) / total_unique_players},
            {"Unique Players": age_counts["30-34"], "Percentage": (age_counts["30-34"] * 100) / total_unique_players},
            {"Unique Players": age_counts["35-39"], "Percentage": (age_counts["35-39"] * 100) / total_unique_players},
            {"Unique Players": age_counts["40+"], "Percentage": (age_counts["40+"] * 100) / total_unique_players}]

summary_ages_df = pd.DataFrame(age_list)
summary_ages_df.rename(index={0:'<10', 1:'10-14', 2:'15-19', 3:'20-24', 4:'25-29', 5:'30-34', 6:'35-39', 7:'40+'}, inplace=True)
summary_ages_df["Percentage"] = summary_ages_df["Percentage"].map("{:.2f}%".format)
summary_ages_df = summary_ages_df[["Unique Players", "Percentage"]]

summary_ages_df


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[8]:


# Can use the previously determined DataFrame
groupedby_age_range = purchases_df.groupby("Age Ranges")
total_item_count_by_age = groupedby_age_range['Item ID'].count()
total_spent_by_age = groupedby_age_range['Price'].sum()
max_cost_by_age = groupedby_age_range['Price'].max()
min_cost_by_age = groupedby_age_range['Price'].min()
avg_cost_by_age = groupedby_age_range['Price'].mean()

# age_counts from In[7]
age_purchase_list = [{"Unique Players": age_counts["<10"], "Purchase Count": total_item_count_by_age["<10"],
                      "Total Purchases": total_spent_by_age["<10"], "Avg Spent per Player": total_spent_by_age["<10"] / age_counts["<10"]},
                     {"Unique Players": age_counts["10-14"], "Purchase Count": total_item_count_by_age["10-14"],
                      "Total Purchases": total_spent_by_age["10-14"], "Avg Spent per Player": total_spent_by_age["10-14"] / age_counts["10-14"]},
                     {"Unique Players": age_counts["15-19"], "Purchase Count": total_item_count_by_age["15-19"],
                      "Total Purchases": total_spent_by_age["15-19"], "Avg Spent per Player": total_spent_by_age["15-19"] / age_counts["15-19"]},
                     {"Unique Players": age_counts["20-24"], "Purchase Count": total_item_count_by_age["20-24"],
                      "Total Purchases": total_spent_by_age["20-24"], "Avg Spent per Player": total_spent_by_age["20-24"] / age_counts["20-24"]},
                     {"Unique Players": age_counts["25-29"], "Purchase Count": total_item_count_by_age["25-29"],
                      "Total Purchases": total_spent_by_age["25-29"], "Avg Spent per Player": total_spent_by_age["25-29"] / age_counts["25-29"]},
                     {"Unique Players": age_counts["30-34"], "Purchase Count": total_item_count_by_age["30-34"],
                      "Total Purchases": total_spent_by_age["30-34"], "Avg Spent per Player": total_spent_by_age["30-34"] / age_counts["30-34"]},
                     {"Unique Players": age_counts["35-39"], "Purchase Count": total_item_count_by_age["35-39"],
                      "Total Purchases": total_spent_by_age["35-39"], "Avg Spent per Player": total_spent_by_age["35-39"] / age_counts["35-39"]},
                     {"Unique Players": age_counts["40+"], "Purchase Count": total_item_count_by_age["40+"],
                      "Total Purchases": total_spent_by_age["40+"], "Avg Spent per Player": total_spent_by_age["40+"] / age_counts["40+"]}]

summary_purchases_by_age_df = pd.DataFrame(age_purchase_list)
# Formatting
summary_purchases_by_age_df["Total Purchases"] = summary_purchases_by_age_df["Total Purchases"].map("${:.2f}".format)
summary_purchases_by_age_df["Avg Spent per Player"] = summary_purchases_by_age_df["Avg Spent per Player"].map("${:.2f}".format)
# Rename indexes
summary_purchases_by_age_df.rename(index={0:'<10', 1:'10-14', 2:'15-19', 3:'20-24', 4:'25-29', 5:'30-34',
                                          6:'35-39', 7:'40+'}, inplace=True)
# change coumn order
summary_purchases_by_age_df = summary_purchases_by_age_df[['Unique Players','Purchase Count', 'Total Purchases',
                                                           'Avg Spent per Player']]

summary_purchases_by_age_df


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[9]:


groupedby_player = purchases_df.groupby(['SN'])
total_spent_player = groupedby_player['Price'].sum()
items_per_player = groupedby_player['Price'].count()

player_list_df = pd.DataFrame(total_spent_player)
player_list_df['Item Count'] = items_per_player
player_list_df['Avg Spent'] = total_spent_player / items_per_player
player_list_df.columns = ["Total Purchases", "Item Count", "Avg Spent"]
player_list_df
# Formatting
player_list_df["Avg Spent"] = player_list_df["Avg Spent"].map("${:.2f}".format)
player_list_df.sort_values(by='Total Purchases', ascending=False, inplace=True)
player_list_df["Total Purchases"] = player_list_df["Total Purchases"].map("${:.2f}".format)

player_list_df.head(5)


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[10]:


popular_item_df = purchases_df.loc[:, 'Item ID':'Price'].copy()
groupedby_popular = popular_item_df.groupby(['Item ID', 'Item Name'])

total_purchases = groupedby_popular['Price'].sum()
num_items_purchased = groupedby_popular['Item ID'].count()

# Create dataframe from groupby values
popular_df = pd.DataFrame(num_items_purchased)
popular_df['Total Purchase Value'] = total_purchases
popular_df.columns = ["Purchase Count", "Total Purchase Value"]
popular_df = popular_df.sort_values(by='Item ID')

# Create prices dataframe
prices_df = purchases_df[['Item ID', 'Item Name', 'Price']]
prices_nodup_df = prices_df.drop_duplicates(['Item ID'], keep = 'last')
prices_post_df = prices_nodup_df.sort_values(by=['Item ID'])
prices_post_df.set_index(['Item ID', 'Item Name'], inplace=True)
# Join the 2 dataframes
popular_df = popular_df.join(prices_post_df)

# Copy for most profitable list below because formatting screws up sorting!)
profit_df = popular_df

# Sort by Purchase Count and format
popular_df = popular_df.sort_values(by='Purchase Count', ascending=False)
popular_df["Price"] = popular_df["Price"].map("${:.2f}".format)
popular_df["Total Purchase Value"] = popular_df["Total Purchase Value"].map("${:.2f}".format)

popular_df.head()


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[11]:


# Sort by Total Purchase Value and format
profit_df = profit_df.sort_values(by='Total Purchase Value', ascending=False)
profit_df["Price"] = profit_df["Price"].map("${:.2f}".format)
profit_df["Total Purchase Value"] = profit_df["Total Purchase Value"].map("${:.2f}".format)

profit_df.head()


# In[ ]:


get_ipython().system('jupyter nbconvert --to script heroes_of_ymoli.ipynb')

