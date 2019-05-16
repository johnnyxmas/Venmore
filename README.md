# Venmore
Scripts for scraping the Venmo v1 and v5 APIs 

##NOTE: THESE NO LONGER WORK FOR HISTORICAL DATA.
Venmo has disabled pagination in their APIs, which means no more scraping backwards in time. They may still work for camping / scraping real-time data with some hacking.


These scripts leverage one-time use account creation to generate API access tokens, which are for some reason placed in HTTP response headers when the New Account Confirmation page is delivered. 

API v1 seems to be the most stable, whereas v5 seems to lock out extremely fast, regardless of token. 

See Johnny Xmas' talk "Shut Up and Take My Money: Scraping the Venmo Public Feed" from Hackfest Canada 10 (2018) for detailed info. 

Slide deck from the above talk located in the [Talk_Decks](https://github.com/johnnyxmas/Talk_Decks/tree/master/2018/Scraping%20the%20Venmo%20Public%20Feed) repository 