import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df[df["ConvertedCompYearly"].notnull()]
    df = df.dropna()
    df = df[(df["Employment"] == "Employed, full-time") | (df["Employment"] == "Independent contractor, freelancer, or self-employed") | (df["Employment"] == "Employed, part-time")]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedCompYearly"] <= 250000]
    df = df[df["ConvertedCompYearly"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df.rename({"YearsCodePro": "Experience"}, axis=1)
    
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2020
    """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)
    
    st.write(
        """
    #### Average Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Average Salary Based On Experience
    """
    )

    data = df.groupby(["Experience"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)


    # Define the data
    country_count = df["Country"].value_counts()
    legend_labels = []

    # Calculate the total number of customers
    total_countries = sum(country_count)

    # Create the donut pie chart
    fig, ax = plt.subplots(figsize=(10, 10))
    inner_colors = ['white'] * len(country_count)
    wedges, _, autotexts = plt.pie(country_count, labels=None, autopct='%1.1f%%',
                                textprops={'color': 'white', 'fontsize': 14, 'weight': 'bold'},
                                pctdistance=0.85, wedgeprops=dict(width=0.4, edgecolor='w'))

    # Set aspect ratio to be equal to make the pie circular
    plt.axis('equal')

    # Add the total number of customers in the center of the chart
    plt.text(0, 0, f'Total Countries:\n{total_countries}', horizontalalignment='center',
            verticalalignment='center', fontsize=20, weight='bold')

    # Add the actual number of customers and percentages inside each wedge
    for i, autotext in enumerate(autotexts):
        wedge_center_x = wedges[i].center[0]
        wedge_center_y = wedges[i].center[1]
        text_x = wedge_center_x * 0.85
        text_y = wedge_center_y * 0.85
        autotext.set_text(f'{country_count[i]} ({country_count[i] / total_countries * 100:.1f}%)')
        plt.text(text_x, text_y, f'{country_count[i]}', horizontalalignment='center',
                verticalalignment='center', fontsize=12, color='white', weight='bold')

    # Set title
    plt.title('Distribution of All the Customer Types', fontsize=24, weight='bold')

    # Display the chart
    st.pyplot(fig)
