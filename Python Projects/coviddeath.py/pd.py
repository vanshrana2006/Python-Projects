import pandas as pd

try:
    data = pd.read_csv('houses_prices.csv')
    print("File loaded successfully!")
except FileNotFoundError:
    print("File not found. Please check the name and path.")
