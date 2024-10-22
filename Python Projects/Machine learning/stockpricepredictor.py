import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import yfinance as yf

ticker = 'AAPL'
data = yf.download(ticker, start="2021-01-01", end="2023-01-01")
data.head()

features = pd.DataFrame()
features['Close'] = data['Close']
features['Return'] = data['Close'].pct_change()
features['Moving_average_5'] = data['Close'].rolling(window=5).mean()
features['Moving_Average_20'] = data['Close'].rolling(window=20).mean()
features['Volatility'] = data['Close'].rolling(window=20).std()
features = features.dropna()
features['Target'] = features['Close'].shift(-1)
features = features[:-1]

X = features.drop(['Target'], axis=1)
y = features['Target']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"Root Mean Squared Error: {rmse}")

plt.figure(figsize=(10, 5))
plt.plot(y_test.values, label='Actual Prices', color='blue')
plt.plot(y_pred, label='Predicted Prices', color='orange')
plt.legend()
plt.show()

latest_data = features.iloc[-1].drop('Target').values.reshape(1, -1)
future_price = model.predict(latest_data)
print(f"Predicted price for the next day: {future_price[0]}")