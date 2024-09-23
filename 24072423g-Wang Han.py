import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from io import StringIO  # For handling HTML as strings
from scipy.interpolate import make_interp_spline  # For smoothing the line graph


# Function to scrape data from a given URL
def scrape_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage: {url}")
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all("table")  # Get all tables
    data_frames = []
    for table in tables[:20]:  # Just take the first 20 tables
        html_str = str(table)  # Convert the table to string format
        df = pd.read_html(StringIO(html_str), flavor='bs4')[0]  # Read table into DataFrame
        data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True)  # Combine and reset index


# 1. Scrape the first dataset
url1 = "https://www.hko.gov.hk/tide/eTPKtext2024.html"  # Example webpage link
full_data1 = scrape_data(url1)

# 2. Process the first dataset
if full_data1 is not None:
    selected_data1 = full_data1.iloc[:29, :4]  # Choose the first 29 rows and first 4 columns
    selected_data1.columns = ["Month", 'Date', 'Time', 'Height(m)']
    selected_data1['Time'] = selected_data1['Time'].astype(str)
    selected_data1['YMD'] = selected_data1.apply(lambda row: f"{2024}-{row['Month']:02d}-{row['Date']:02d}", axis=1)
    selected_data1['SJ'] = selected_data1.apply(lambda row: f"{row['Time'].zfill(4)[:2]}:{row['Time'].zfill(4)[2:]}:00",
                                                axis=1)
    selected_data1['YMDSJ'] = pd.to_datetime(selected_data1['YMD'] + ' ' + selected_data1['SJ'],
                                             format='%Y-%m-%d %H:%M:%S', errors='coerce')

# 3. Scrape the second dataset (same URL for demonstration, modify for different data)
url2 = "https://www.hko.gov.hk/tide/eTPKtext2024.html"  # Modify this if you want a different dataset
full_data2 = scrape_data(url2)

# 4. Process the second dataset
if full_data2 is not None:
    selected_data2 = full_data2.iloc[29:58, :4]  # Choose the next 29 rows for comparison
    selected_data2.columns = ["Month", 'Date', 'Time', 'Height(m)']
    selected_data2['Time'] = selected_data2['Time'].astype(str)
    selected_data2['YMD'] = selected_data2.apply(lambda row: f"{2024}-{row['Month']:02d}-{row['Date']:02d}", axis=1)
    selected_data2['SJ'] = selected_data2.apply(lambda row: f"{row['Time'].zfill(4)[:2]}:{row['Time'].zfill(4)[2:]}:00",
                                                axis=1)
    selected_data2['YMDSJ'] = pd.to_datetime(selected_data2['YMD'] + ' ' + selected_data2['SJ'],
                                             format='%Y-%m-%d %H:%M:%S', errors='coerce')

# 5. Scrape the third dataset for a line chart
url3 = "https://www.hko.gov.hk/tide/eTPKtext2024.html"  # Modify this if needed
full_data3 = scrape_data(url3)

# 6. Process the third dataset
if full_data3 is not None:
    selected_data3 = full_data3.iloc[58:87, :4]  # Choose the next 29 rows for the line chart
    selected_data3.columns = ["Month", 'Date', 'Time', 'Height(m)']
    selected_data3['Time'] = selected_data3['Time'].astype(str)
    selected_data3['YMD'] = selected_data3.apply(lambda row: f"{2024}-{row['Month']:02d}-{row['Date']:02d}", axis=1)
    selected_data3['SJ'] = selected_data3.apply(lambda row: f"{row['Time'].zfill(4)[:2]}:{row['Time'].zfill(4)[2:]}:00",
                                                axis=1)
    selected_data3['YMDSJ'] = pd.to_datetime(selected_data3['YMD'] + ' ' + selected_data3['SJ'],
                                             format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Check if the third dataset is not empty
if selected_data3.empty:
    print("The third dataset is empty or invalid.")
else:
    try:
        # Print converted DateTime column for verification for the third dataset
        print("Converted DateTime Column for Dataset 3:", selected_data3['YMDSJ'])

        # Prepare data for smoothing
        x = selected_data3['YMDSJ'].astype(np.int64) // 10 ** 9  # Convert datetime to timestamps in seconds
        y = selected_data3['Height(m)']

        # Create a new x for interpolation
        x_new = np.linspace(x.min(), x.max(), 500)  # 500 points for smoothness
        spl = make_interp_spline(x, y, k=3)  # Cubic spline interpolation
        y_smooth = spl(x_new)

        # Convert back to datetime for plotting
        x_new_datetime = pd.to_datetime(x_new, unit='s')

        # Create a line plot for the third dataset using Matplotlib
        plt.figure(figsize=(12, 6))  # Set the figure size
        plt.plot(x_new_datetime, y_smooth, linestyle='-', color='b', label='Tide Height (Smoothed)')  # Smoothed line

        # Add title and axis labels
        plt.title('Tide Height Data Over Time (Smoothed)', fontweight='bold', fontsize=18)
        plt.xlabel('Date and Time', fontsize=12)
        plt.ylabel('Height (m)', fontsize=12)

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)

        # Add grid and legend
        plt.grid()
        plt.legend()
        plt.tight_layout()  # Adjust layout to fit labels
        plt.show()

    except Exception as e:
        print("Error while processing the third dataset:", str(e))