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

userSetProfit = "ARBRITRAGE DIFFERENCE YOUR LOOKING FOR USER MODE COINGECKO AS AN INT"
stableSetProfit = "ARBRITRAGE DIFFERENCE YOUR LOOKING FOR USER MODE USD AS AN INT"
BOT_TOKEN = "TOKEN OF YOUR BOT WITH QUOTES"
CG_ID = "ENTER YOUR COINGECKO DISCORD CHANNEL ID HERE WITHOUT QUOTES"
USDE_ID = "ENTER YOUR USD DISCORD CHANNEL ID HERE WITHOUT QUOTES"
LOG_LOCATION = "ENTER LOCATION OF YOUR LOG FILE PATH"

IterationCounter = 0
warnings.filterwarnings("ignore", category=DeprecationWarning)
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

colorama.init()

logging.basicConfig(
    level=logging.ERROR,
    filename=LOG_LOCATION + ".txt",
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

NAME_ID_CONVERTER = [
    # API ID, Symbol
    ["energi", "Wrapped NRG"],
    ["energi-dollar", "Energi Dollar"],
    ["dai", "Dai Stablecoin"],
    ["ethereum", "Ether"],
    ["bitcoin", "Bitcoin"],
    ["usd-coin", "USD Coin"],
]

STABLE_LIST = [
    "USDC", 
    "DAI", 
    "USDE"]  # List of stablecoin names


