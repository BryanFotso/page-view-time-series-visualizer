import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df =pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    fig=plt.figure(figsize=(12,6))
    plt.plot(df.index, df["value"], color="blue")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Préparation des données
    df_bar = df.copy()
    df_bar['year'] = df.index.year
    df_bar['month'] = df.index.month
    df_bar['month_name'] = df.index.strftime('%B')

    # Groupement et tri
    df_bar = df_bar.groupby(['year', 'month','month_name'])['value'].mean().reset_index()
    df_bar = df_bar.sort_values(['year', 'month'])

    # Complétez les données manquantes
    months = pd.date_range('2020-01', '2020-12', freq='MS').strftime('%B').tolist()
    
    # Tracé du graphique
    fig = plt.figure(figsize=(12, 6))
    sns.barplot(
        x="year",
        y="value",
        hue="month_name",
        hue_order=months,
        data=df_bar
    )
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', loc='upper left')

    # Sauvegarde et retour
    fig.savefig('bar_plot.png')
    return fig



# def draw_bar_plot():
#     # Copy and modify data for monthly bar plot
#     df_bar = df.copy()
#     df_bar["year"] = df_bar.index.year
#     df_bar["month"] = df_bar.index.month
#     df_bar = df_bar.groupby(["year", "month"])["value"].mean().reset_index()
#     months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
#     # Draw bar plot
#     fig = plt.figure(figsize=(12,6))
#     sns.barplot(
#         x="year",
#         y="value",
#         hue="months",
#         hue_order=months,
#         data=df_bar
#         )
#     plt.title("Average Monthly Page Views by Year")
#     plt.xlabel("Years")
#     plt.ylabel("Average Page Views")
#     plt.legend(title="Months", labels=months)

#     # Save image and return fig (don't change this part)
#     fig.savefig('bar_plot.png')
#     return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    months=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Box plot for the years 
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    
    # Box plot for the months
    sns.boxplot(x="month", y="value", data=df_box, order=months, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
