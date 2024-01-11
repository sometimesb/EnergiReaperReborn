# 🌐 Energi Reaper Reborn
A second iteration of the energi reaper bot that I built. The first version is sitting somewhere and is deprecated :(

## 📝 Introduction
This Python script functions as a cryptocurrency monitoring bot, leveraging various libraries and APIs to perform comprehensive analyses. The bot employs web scraping capabilities through Selenium, Discord API for communication, and Colorama for pretty terminal output formatting. It operates in two distinct modes: CoinGecko and USD. In CoinGecko mode, the bot compares cryptocurrency prices between EnergiSwap and CoinGecko. Conversely, in USD mode, it focuses on analyzing price differentials among selected stablecoins.

The bot supports full error logging, and resets itself if required. I put a lot of work into this bot and it made me 40x my initial investment at its peak :)

This uses _EnergiSwap_ (a fork of UniSwap).


## 🔧 Technologies Used
* Discord - For bot communication
* Python - Main driver of the script
* Batch - executes script for the user

## 📙 Libraries and Versions Used
* python             3.11.4
* async-timeout      3.0.1
* colorama           0.4.6
* discord.py         1.7.3
* keyboard           0.13.5
* requests           2.31.0
* selenium           4.16.0


## 🚀 Images
![Screenshot of project](https://i.imgur.com/HXcBy1d.png)
![Screenshot of project](https://i.imgur.com/4m38FCK.png)


## 📄 Full rundown & Installation:
1) Must install libraries with specific versions above. Special emphasis on the discord version, or it will not work.
2) Go to the constants.py file and scroll to line 19. Add your constants.

 ```python
userSetProfit = "ARBITRAGE DIFFERENCE YOU'RE LOOKING FOR IN USER MODE, COINGECKO AS AN INT"
stableSetProfit = "ARBITRAGE DIFFERENCE YOU'RE LOOKING FOR IN USER MODE, USD AS AN INT"
BOT_TOKEN = "YOUR BOT TOKEN WITH QUOTES"
CG_ID = "ENTER YOUR COINGECKO DISCORD CHANNEL ID HERE WITHOUT QUOTES"
USDE_ID = "ENTER YOUR USD DISCORD CHANNEL ID HERE WITHOUT QUOTES"
LOG_LOCATION = "ENTER LOCATION OF YOUR LOG FILE PATH"
```

4) Hit runme.bat
5) Profit :)


