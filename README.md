STOCKSEE by Sanjay Senthilkumar:

Description: This is a project where users are able to keep track of any stock that they are currently interested in. If they are interested enough to buy it, StockSee will be able to capture their transactions under a secure database in which they can view at any time. 

Features:
1.Alerts that show a certain stock has crossed your threshold
2.Transactions to keep track of all of the stock that are in your portfolio.
3. Watchlist to keep track of potenial stocks that you want.
4. Caching to keep request at a minimum. Resets the stale price after 30 seconds to the current one shown by yfinance.
5. Logging to keep track of the server system. When it starts, takes in requests, and when it stops.
6. Implemented a Background scheduler to make sure that an authethicated email to send to specific user if their threhold is crossed.
7. Uses Fastapi to make endpoints that retrieve data related to transactions, watchlists, and alerts.
8. Has a algorithmic intelligence layer that lets users calculate a RSI score for a stock and gives them a recommendation based on it.
9. Each user is verified and checked using JSON Web Tokens.

How To Run:
1.Git clone the repo using "git clone https://github.com/Sanj84-co/Stockproj.git"
2. Then create your own virtual environment using python -m venv venv.
3. Create your own .env to add your email credentials(EMAIL_ID EMAIL_PASSWORD,SECRET_KEY).
4. use pip install -r requirements.txt in order to install all of the dependencies.
5. In the project root, run uvicorn src.main.api:app --reload to run the application.

Tech Stack: Python, FastApi, matplotlib, yfinance, logging, SQlite, APScheduler, smtplib,passlib,python-jose,pytest