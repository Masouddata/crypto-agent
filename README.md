Crypto Intelligence Scanner Pro — update notes

Files:
- app.py: updated Streamlit app, based on the supplied project file.
- requirements.txt: runtime dependencies.

Render environment variables:
- COINGECKO_API_KEY (keep the existing value)
- CRYPTOMETER_API_KEY (the new CryptoMeter key)

Deploy:
1. Replace app.py in the existing GitHub repository with this file.
2. Add requirements.txt if the repository does not already have one. If one already exists, merge the dependencies instead of overwriting it.
3. Commit and push to the existing main branch; Render should deploy from the connected repository.
4. In the app, click “Fetch CryptoMeter intelligence”. Free feeds are requested then. Select paid feeds only if they are enabled/purchased in the CryptoMeter plan.

Security:
- Do not paste API keys into source code or commit them to GitHub.
- Store keys only in Render Environment Variables.

Notes:
- CryptoMeter data is cached for five minutes in the app.
- Whale trades, Volume Flow, Liquidity Lens, Funding Rates and Gainers/Losers are configured as optional paid endpoint calls; they are not requested unless selected by the user.
- The watchlist score is a transparent research heuristic, not a calibrated pump probability or trading instruction.
