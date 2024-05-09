import pandas as pd
import matplotlib.pyplot as plt
"""
        "# Introduction\n",
        "\n",
        "Today we'll dive deep into a dataset all about LEGO. From the dataset we can ask whole bunch of interesting questions about the history of the LEGO company, their product offering, and which LEGO set ultimately rules them all:\n",
        "\n",
        "<ul type=\"square\">\n",
        "<li>What is the most enormous LEGO set ever created and how many parts did it have?</li>\n",
        "\n",
        "<li>How did the LEGO company start out? In which year were the first LEGO sets released and how many sets did the company sell when it first launched?</li>\n",
        "\n",
        "<li>Which LEGO theme has the most sets? Is it one of LEGO's own themes like Ninjago or a theme they licensed liked Harry Potter or Marvel Superheroes?</li>\n",
        "\n",
        "<li>When did the LEGO company really expand its product offering? Can we spot a change in the company strategy based on how many themes and sets did it released year-on-year?</li>\n",
        "\n",
        "<li>Did LEGO sets grow in size and complexity over time? Do older LEGO \n",
        "sets tend to have more or fewer parts than newer sets?</li>\n",
        "</ul>\n",
        "\n",
        "**Data Source**\n",
        "\n",
        "[Rebrickable](https://rebrickable.com/downloads/) has compiled data on all the LEGO pieces in existence. I recommend you use download the .csv files provided in this lesson. "
"""
q1 = """
**Challenge**: How many different colours does the LEGO company produce? Read the colors.csv file in the data folder and find the total number of unique colours. Try using the [.nunique() method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.nunique.html?highlight=nunique#pandas.DataFrame.nunique) to accomplish this.
"""

print(q1)
colors_df = pd.read_csv('data/colors.csv')
print(colors_df.nunique())

q2_intro = """
The sets.csv contains a list of LEGO sets. It shows in which year the set was released and the number of parts in the set.

Can you take the first steps in exploring this dataset? Read the .csv and take a look at the columns.

Then try and answer the following questions:
"""
print(q2_intro)
sets_df = pd.read_csv('data/sets.csv')
#set_num name year theme_id num_parts

#print(sets_df)


q2a = "In which year were the first LEGO sets released and what were these sets called?"
print(q2a)
q2a_idx = sets_df.year.idxmin()
#print(sets_df.loc[q2a_idx])
print(sets_df.year.loc[q2a_idx])
print(sets_df[sets_df.year == sets_df.year.min()])
print("")

q2b = "How many different products did the LEGO company sell in their first year of operation?"
print(q2b)
print(sets_df[sets_df.year == sets_df.year.min()].name.count())
print("")

q2c = "What are the top 5 LEGO sets with the most number of parts?"
print(q2c)
print(sets_df.sort_values('num_parts', ascending=False).head())
print("")

q3a = "Now, let's create a new Series called sets_by_year which has the years as the index and the number of sets as the value"
print(q3a)
sets_by_year = sets_df.groupby('year').count()
#print(sets_by_year.set_num.tail())
#print(sets_by_year[:-2].set_num.tail())
#print("")

q3b = "Having summed the number of LEGO sets per year, visualise this data using a line chart with Matplotlib"
print(q3b)
print("")
plt.title("LEGO trends in time (sets and themes)")
ax1 = plt.gca() # get current axes
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of sets', color='green')
ax1.plot(sets_by_year[:-2].set_num, color='g')

q4 = "Calculate the number of different themes by calendar year. This means we have to group the data by year and then count the number of unique theme_ids for that year."
print(q4)
themes_by_year = sets_df.groupby('year').agg({'theme_id':
                                              pd.Series.nunique})
themes_by_year.rename(columns = {'theme_id': 'nr_themes'},
                                 inplace = True)
#print(themes_by_year.head())

#plt.title("Themes of LEGO sets per year")
ax2 = ax1.twinx()
ax2.set_ylabel('Number of themes', color='blue')
ax2.plot(themes_by_year[:-2].nr_themes, color='b')
plt.show()
plt.close()

q5 = "Create a Pandas Series called parts_per_set that has the year as the index and contains the average number of parts per LEGO set in that year."
parts_per_set = sets_df.groupby('year').agg({'num_parts':
                                             pd.Series.mean})
#print(parts_per_set)
plt.title("Scatter plot chart of average number of parts per LEGO set each year")
plt.xlabel('Year')
plt.ylabel('Average number of parts per LEGO set')
plt.scatter(parts_per_set.index[:-2],
            parts_per_set.num_parts[:-2])
plt.show()

q6 = """
How is the themes.csv structured?

Search for the name 'Star Wars'. How many ids correspond to the 'Star Wars' name in the themes.csv?

Use the ids you just found and look for the corresponding sets in the sets.csv
(Hint: you'll need to look for matches in the theme_id column)."""
print(q6)
themes_df = pd.read_csv('data/themes.csv')
print(themes_df.shape)
print(themes_df[themes_df.name == "Star Wars"])
#set_num name year theme_id num_parts
print(sets_df[sets_df.theme_id == 209])

set_theme_count = sets_df["theme_id"].value_counts()
#print(set_theme_count)
#print(type(set_theme_count))
#Create a DF from the Series
set_theme_count = pd.DataFrame({'id': set_theme_count.index,
                                'set_count': set_theme_count.values})
#print(set_theme_count)
#Merge!
merged_df = pd.merge(set_theme_count, themes_df, on='id')
#print(merged_df)
plt.figure(figsize=(14,8))
plt.xticks(fontsize=14, rotation=45)
plt.yticks(fontsize=14)
plt.ylabel('Nr of Sets', fontsize=14)
plt.xlabel('Theme Name', fontsize=14)
plt.title("Different number of sets per theme in LEGO")
plt.bar(merged_df.name[:10], merged_df.set_count[:10])
plt.show()
