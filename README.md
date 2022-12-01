### Hi there 👋


# Lumnis Crypto Alternative Data API

The LUMNIS Crypto API provides the most comprehensive factor dataset for crypto assets. We provide the following group of factors:

- **Micro-structural Factors** - These are factors derived from **order book data and trade data**. We process terabytes of data to extract the most relevant order book and trade factors that are delivered in real-time
- **Regime Factors** - We provide **regime data** that enables users to observe how strategies perform in different conditions of the market. For example, some strategies work better during high volatile regimes. We use proprietary algorithms for effectively determining regimes.


This data can be used for backtesting and implementing trading strategies.


### Receiving API Token
You can sign up [here](https://docs.lumnis.io) to retreive a lumnis API Key 

Please [e-mail me](mailto:ajaye@lumnis.org) if there is an issue with setting up or retreiving an API Key.

## Getting Started
#### Prerequisites
- Python version 3 installed

#### Installation
The package can easily be installed by running the following command 
```python
pip install lumnisfactors
```


### Usage
```python
#Import the package
from lumnisfactors import LumnisFactors

#Add your API KEY
API_KEY = ""
lumnis = LumnisFactors(API_KEY)

#Retrieve a single days worth of data
df_single_date  = lumnis.get_single_date_data("vpin", "coinbase", "ethusd",  "hour", "2022-01-01")

#Retrieve multiple days worth of data
historical_data = lumnis.get_historical_data("vpin", "coinbase", "ethusd",  "hour", "2022-01-01", "2022-02-01")
```
