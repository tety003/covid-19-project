import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


try:
    df = pd.read_csv("owid-covid-data.csv")
except FileNotFoundError:
    print("Error: Dataset not found. Please make sure 'owid-covid-data.csv' is in the working directory.")
    exit()


print("Columns:", df.columns.tolist())
print("First 5 Rows:")
print(df.head())
print("Missing Values:")
print(df.isnull().sum())


countries = ['Brazil', 'Germany', 'South Africa']
df = df[df['location'].isin(countries)]
df = df[['date', 'location', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations']]
df['date'] = pd.to_datetime(df['date'])
df.sort_values(by=['location', 'date'], inplace=True)
df.fillna(0, inplace=True)


colors = plt.get_cmap('tab10')
country_colors = dict(zip(countries, [colors(i) for i in range(len(countries))]))


plt.figure(figsize=(10, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_cases'], label=country, color=country_colors[country])
plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.tight_layout()
plt.show()


latest_date = df['date'].max()
latest_df = df[df['date'] == latest_date]
total_cases_by_country = latest_df.groupby('location')['total_cases'].sum()
bar_colors = [country_colors[c] for c in total_cases_by_country.index]
total_cases_by_country.plot(kind='bar', color=bar_colors)
plt.title(f'Total COVID-19 Cases by Country on {latest_date.date()}')
plt.ylabel('Total Cases')
plt.xlabel('Country')
plt.tight_layout()
plt.show()


plt.figure(figsize=(8, 5))
sns.histplot(df['new_cases'], bins=30, kde=True, color='darkorange')
plt.title('Distribution of Daily New COVID-19 Cases')
plt.xlabel('New Cases')
plt.tight_layout()
plt.show()


plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='total_cases', y='total_deaths', hue='location', palette=country_colors)
plt.title('Total Cases vs Total Deaths')
plt.xlabel('Total Cases')
plt.ylabel('Total Deaths')
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_vaccinations'], label=country, color=country_colors[country])
plt.title('COVID-19 Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend()
plt.tight_layout()
plt.show()


df['death_rate'] = df['total_deaths'] / df['total_cases']
latest_death_rate = df[df['date'] == latest_date][['location', 'death_rate']]
print("Death Rate by Country on Latest Date:")
print(latest_death_rate)


print("Key Insights:")
print("Brazil has shown significant increases in total cases over time.")
print("Germany maintained relatively stable vaccination growth.")
print("South Africa's new case distribution has wide variance, and its death rate remains notable.")
