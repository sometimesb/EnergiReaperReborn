import time
import logging
import json
import requests
import colorama
import warnings
import os
import keyboard
import discord
import asyncio

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

# Set user-defined parameters
userSetProfit = "ARBITRAGE DIFFERENCE YOU'RE LOOKING FOR IN USER MODE, COINGECKO AS AN INT"
stableSetProfit = "ARBITRAGE DIFFERENCE YOU'RE LOOKING FOR IN USER MODE, USD AS AN INT"
BOT_TOKEN = "YOUR BOT TOKEN WITH QUOTES"
CG_ID = "ENTER YOUR COINGECKO DISCORD CHANNEL ID HERE WITHOUT QUOTES"
USDE_ID = "ENTER YOUR USD DISCORD CHANNEL ID HERE WITHOUT QUOTES"
LOG_LOCATION = "ENTER LOCATION OF YOUR LOG FILE PATH"

# Initialize iteration counter
IterationCounter = 0

# Ignore DeprecationWarnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set asyncio event loop policy for Windows
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Initialize colorama
colorama.init()

# Configure logging settings
logging.basicConfig(
    level=logging.ERROR,
    filename=LOG_LOCATION + ".txt",
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Define a mapping between API IDs and corresponding symbols
NAME_ID_CONVERTER = [
    ["energi", "Wrapped NRG"],
    ["energi-dollar", "Energi Dollar"],
    ["dai", "Dai Stablecoin"],
    ["ethereum", "Ether"],
    ["bitcoin", "Bitcoin"],
    ["usd-coin", "USD Coin"],
]

# List of stablecoin names
STABLE_LIST = [
    "USDC", 
    "DAI", 
    "USDE"
]
