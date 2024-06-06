%%writefile app.py
import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import squarify
import textwrap
import numpy as np
from matplotlib.patheffects import withStroke
from matplotlib import pyplot as plt
import seaborn as sns


KeyBERT_final_df = pd.read_csv("KeyBERT_final_df.csv")
final_keywords_aligned = []
with open("final_keywords_aligned.txt", "r") as file:
    # Read each line of the file
    for line in file:
        # Remove newline character and whitespace, then convert to a list
        line_list = eval(line.strip())
        # Append the item to the documents_labels list
        final_keywords_aligned.append(line_list)

print(len(final_keywords_aligned))

# Assuming `KeyBERT_final_df` and `final_keywords_aligned` are defined
# Create a dictionary
data = {
    "Abstract": KeyBERT_final_df["Abstract"],
    "Year": KeyBERT_final_df["Year"],
    "Keywords": final_keywords_aligned,
    "Journal": KeyBERT_final_df["Journal"]
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)

################################################################################

## treemap
st.title("Physics Concepts Data Dashboard")
# Year Selector
years = df["Year"].unique()
year = st.slider("Select Year for Treemap", min_value=min(years), max_value=max(years), value=2021, key='treemap_slider')

# Filter dataframe based on selected year
filtered_df = df[df["Year"] == year]

# Extract keywords from the filtered dataframe and flatten the list of lists
keywords = [keyword for sublist in filtered_df["Keywords"] for keyword in sublist]

# Get unique keywords
unique_keywords = set(keywords)

################################################################################

# Display the treemap
classes = []
popularity = []
count_classes = {}
for keyword in keywords:
    if keyword in count_classes:
        count_classes[keyword] += 1
    else:
        count_classes[keyword] = 1

counter_others = 0
for key, value in count_classes.items():
    if value > 50:
        classes.append(key)
        popularity.append(value)
    else:
        counter_others += 1
classes.append("Others")
popularity.append(counter_others)
data_classes = {"Class": classes, "Popularity": popularity}

st.title("Class Popularity Treemap")

# Generate lighter colors using a colormap
cmap = plt.cm.Blues  # You can change this to other colormaps
norm = mcolors.Normalize(vmin=min(popularity), vmax=max(popularity))
colors = [cmap(norm(value)) for value in popularity]

# Define a path effect for the text outline
path_effects = [withStroke(linewidth=2, foreground='white')]

# Wrap text for labels
wrapped_labels = [textwrap.fill(label, width=15) for label in classes]

# Create the treemap
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
squarify.plot(
    sizes=popularity,
    label=wrapped_labels,
    color=colors,
    alpha=0.7,
    text_kwargs={'fontsize': 8, 'wrap': True, 'path_effects': path_effects}
)
plt.axis('off')
plt.title('Class Popularity Treemap')
st.pyplot(fig)

################################################################################

year_2 = st.slider("Select Year for Journal Analysis", min_value=min(years), max_value=max(years), value=2021, key='journal_slider')

st.title("Journal Published through Time")

# Defining threshold
threshold = 50

# Define the year to filter by
filter_year = year_2

# Filter DataFrame by year
df_filtered = df[df['Year'] == filter_year]

# Group by 'Journal' and count occurrences
journal_counts = df_filtered.groupby('Journal').size()

# Filter to only include counts greater than the threshold
filtered_counts = journal_counts[journal_counts > threshold]

if not filtered_counts.empty:
    # Truncate long names
    max_length = 20
    shortened_index = filtered_counts.index.to_series().apply(lambda x: x if len(x) <= max_length else x[:max_length-3] + '...')
    
    # Plot the filtered data with shortened names
    filtered_counts.index = shortened_index
    
    # Use Streamlit to display the plot
    fig2, ax2 = plt.subplots()
    filtered_counts.plot(kind='barh', color=sns.color_palette('Dark2'), ax=ax2)
    
    # Customize the plot
    ax2.spines[['top', 'right']].set_visible(False)
    ax2.set_xlabel('Number of articles')
    ax2.set_ylabel('Journal')
    ax2.set_title('Most Published Journal for Year {}'.format(filter_year))
    
    st.pyplot(fig2)
else:
    st.write("No journals have more than {} articles published in the selected year.".format(threshold))

