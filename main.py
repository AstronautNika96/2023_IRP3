import pandas as pd
import os

from matplotlib import pyplot as plt

folder_path = '.'
start = 'List_of_books_banned_by_governments_'
end = '.csv'
# ignored_countries = ['India']
ignored_countries = []
combined_file = 'combined_file.csv'

def generate_merged_file():
    # create a dict of countries
    countries = {}
    with open("countries.txt", "r") as file:
        for i, country in enumerate(file.readlines()):
            countries[i + 1] = country.strip()

    all_files = os.listdir(folder_path)

    # Filter out non-CSV files
    csv_files = [f for f in all_files if f.endswith(end) and f.startswith(start)]

    # Create a list to hold the dataframes
    df_list = []

    for csv in csv_files:
        file_path = os.path.join(folder_path, csv)
        # create country column
        df = pd.read_csv(file_path)
        c = countries[int(csv[len(start):csv.rfind(end)])]
        df2 = df.assign(country=c)
        if c not in ignored_countries:
            df2.columns = map(str.lower, df2.columns)
            df_list.append(df2)

    # Concatenate all data into one DataFrame
    big_df = pd.concat(df_list, ignore_index=True)

    # Save the final result to a new CSV file
    big_df.to_csv(os.path.join(folder_path, combined_file), index=False)

def country_bar_plot():
    file_path = os.path.join(folder_path, combined_file)
    df = pd.read_csv(file_path)
    df_gb = df.groupby('country').size().sort_values(ascending=False).to_frame(name='count')
    s = df_gb[df_gb['count'] > 2]
    s.plot(kind='bar')
    plt.subplots_adjust(bottom=0.35)
    plt.show(block=True)


def book_bar_plot():
    file_path = os.path.join(folder_path, combined_file)
    df = pd.read_csv(file_path)
    df_gb = df.groupby('title').size().sort_values(ascending=False).to_frame(name='count')
    s = df_gb[df_gb['count'] > 2]
    s.plot(kind='bar')
    plt.subplots_adjust(bottom=0.55)
    plt.show(block=True)


def book_bar_authors():
    file_path = os.path.join(folder_path, combined_file)
    df = pd.read_csv(file_path)
    df_gb = df.groupby('author(s)').size().sort_values(ascending=False).to_frame(name='count')
    s = df_gb[df_gb['count'] > 3]
    s.plot(kind='bar')
    plt.subplots_adjust(bottom=0.35)
    plt.show(block=True)


if __name__ == '__main__':
    # TODO add categories for entries in the merged file
    generate_merged_file()
    country_bar_plot()
    book_bar_plot()
    book_bar_authors()
