import pandas as pd

# Load the dataset
try:
    df = pd.read_csv("owid-covid-data.csv")
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("File not found. Please ensure 'owid-covid-data.csv' is in the working directory.")

# Preview the dataset
df.head()

# View column names
print(df.columns)

# Check for missing values
df.isnull().sum().sort_values(ascending=False).head(10)

# Check data types
df.info()

#data cleaning
# Filter for selected countries
countries = ['Kenya', 'United States', 'India']
df_filtered = df[df['location'].isin(countries)].copy()

# Convert 'date' column to datetime
df_filtered['date'] = pd.to_datetime(df_filtered['date'])

# Handle missing numeric values with interpolation
numeric_cols = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'total_vaccinations']
df_filtered[numeric_cols] = df_filtered[numeric_cols].interpolate()

# Drop rows where date or total_cases are still missing (just in case)
df_filtered = df_filtered.dropna(subset=['date', 'total_cases'])

# Check cleaned data
df_filtered.head()


# exploring the data
import matplotlib.pyplot as plt
import seaborn as sns

# Set plot style
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# Plot total cases over time
for country in countries:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)

plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot total deaths over time
for country in countries:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['total_deaths'], label=country)

plt.title('Total COVID-19 Deaths Over Time')
plt.xlabel('Date')
plt.ylabel('Total Deaths')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Compare new daily cases
sns.lineplot(data=df_filtered, x="date", y="new_cases", hue="location")
plt.title(" New Daily COVID-19 Cases")
plt.ylabel("New Cases")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Calculate and visualize death rate
df_filtered["death_rate"] = df_filtered["total_deaths"] / df_filtered["total_cases"]

sns.lineplot(data=df_filtered, x="date", y="death_rate", hue="location")
plt.title("COVID-19 Death Rate Over Time")
plt.ylabel("Death Rate")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Cumulative vaccinations over time
sns.lineplot(data=df_filtered, x="date", y="total_vaccinations", hue="location")
plt.title("Total Vaccinations Over Time")
plt.ylabel("Cumulative Vaccinations")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Most recent % vaccinated population
latest = df_filtered.sort_values('date').groupby('location').tail(1)
latest = latest.set_index('location')
latest['% vaccinated'] = (latest['total_vaccinations'] / latest['population']) * 100

latest[['% vaccinated']].plot(kind='bar', color='green')
plt.title("🌍 Percentage of Population Vaccinated")
plt.ylabel("% Vaccinated")
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

