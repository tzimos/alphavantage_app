# Author

* Full name: Panagiotis Tzimos
* Email: tzimoss@gmail.com

# Alphavantage api viewer app.

This is a small app api viewer written with Flask and Jquery and powered by
docker. You can easily navigate and view data about indicators like SMA, the
current quotes and analytical historical data splitted into intervals of choice
when applied.

## Installation and Execution

Given that you have acquired a free api
from https://www.alphavantage.co/support/#api-key

Run the following command:

* make start-app
* Visit http://localhost:5000/
* Put your api key to the input.
* Search whatever symbol you want.
* Beware of how fast you are clicking around, because the api has hard rate
  limits (5 calls/hour)

## Destroy the app

Run the following command:

* make stop-app

