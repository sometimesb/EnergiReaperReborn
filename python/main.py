from constants import *
import constants as constants
from startup import *

async def sendDiscordMessage(channel_id, message, bot_token):
    # Create an instance of the bot
    bot = discord.Client()

    @bot.event
    async def on_ready():
        try:
            # Get the channel object for the desired channel ID
            channel = bot.get_channel(channel_id)

            # Send the customized message to the channel
            await channel.send(message)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            # Stop the bot and close the event loop
            await bot.close()

    # Run the bot using bot_token
    try:
        await bot.start(bot_token)
    except Exception as e:
        print(f"An error occurred while starting the bot: {str(e)}")

    # Run the bot using bot_token
    try:
        await bot.start(bot_token)
    except Exception as e:
        print(f"An error occurred while starting the bot: {str(e)}")

def SeleniumInitializer(driver, css_selector: str, timeout: int = 10):
    driver.set_page_load_timeout(timeout)
    constants.IterationCounter += 1  # Increment the iteration counter
    try:
        driver.get("https://api.energiswap.exchange/v1/assets")
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.XPATH, css_selector)))

        print(colorama.Back.LIGHTBLUE_EX + colorama.Style.BRIGHT + f"PROCEEDING [{constants.IterationCounter}]\n" + colorama.Style.RESET_ALL)

        # Additional code to find the specific HTML element with the given XPath selector
        element = driver.find_element(By.XPATH, css_selector)        
        return element.text
    except TimeoutException:
        print(colorama.Back.RED + "Timed out waiting for page to load" + colorama.Style.RESET_ALL)
        logging.error("Timed out waiting for page to load")
        return None

def convertNameToID(name):
    for item in NAME_ID_CONVERTER:
        if item[1] == name:
            return item[0]
    return None

def printRainbowText(text):
    rainbow_colors = [colorama.Fore.RED, colorama.Fore.YELLOW, colorama.Fore.GREEN,
    colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.CYAN]
    
    reset_color = colorama.Fore.RESET
    for i, char in enumerate(text):
        color = rainbow_colors[i % len(rainbow_colors)]
        print(color + char, end='')
    print(reset_color)

def calculateDifference(last_price, coingecko_price):
    numerator = (coingecko_price-last_price)
    denominator = (last_price + coingecko_price) / 2
    percent_difference = (numerator / denominator) * 100
    return percent_difference

def getCoinPrices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=energi%2Cenergi-dollar%2Cdai%2Cethereum%2Cbitcoin%2Cusd-coin&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error occurred. Status code:", response.status_code)
    return None

def clearTerminal():
    if os.name == 'posix':  # For UNIX-based systems (Linux, macOS)
        _ = os.system('clear')
    else:  # For Windows
        _ = os.system('cls')

def coinGeckoManipulation(element_text, prices):
    asyncio.run(sendDiscordMessage(CG_ID, "`" +  f"PROCEEDING [{constants.IterationCounter}]\n" + "`", BOT_TOKEN))
    try:
        data = json.loads(element_text)
        for key, value in data.items():
            name = value["name"]
            symbol = value["symbol"]
            last_price = value["last_price"]
            api_id = convertNameToID(name)
            if api_id in prices:
                coingecko_price = prices[api_id].get("usd")
                ProfitPercent = calculateDifference(last_price, coingecko_price)
                print(colorama.Back.LIGHTBLACK_EX + str((name)) + colorama.Style.RESET_ALL)
                print("symbol: \t " + symbol)
                print("Coingecko: \t $" + str(coingecko_price))
                print("EnergiSwap: \t $" + str(last_price))

                if ProfitPercent < 0:
                    # Negative value, highlight ProfitPercent in MAGENTA
                    print("%Difference \t " + colorama.Back.MAGENTA + str(ProfitPercent) + "%" + colorama.Style.RESET_ALL)
                elif ProfitPercent > 0 and ProfitPercent < userSetProfit:
                    # Positive value, highlight ProfitPercent in CYAN
                    print("%Difference \t " + colorama.Back.CYAN + str(ProfitPercent) + "%" + colorama.Style.RESET_ALL)

                elif ProfitPercent == 0:
                    # Zero value, print ProfitPercent without highlight
                    print("%Difference \t " + str(ProfitPercent) + "%")

                print()
            
    except json.JSONDecodeError:
        logging.error("Invalid Json Data!")
        print(colorama.Back.RED + "Invalid JSON data" + colorama.Style.RESET_ALL)

def coinGeckoMode():
    clearTerminal()
    try:
        countdown = 60

        while True:
            driver = webdriver.Chrome()
            css_selector = "/html/body"  # Updated XPath selector
            element_text = SeleniumInitializer(driver, css_selector)
            driver.quit()

            if element_text is not None:
                prices = getCoinPrices()  # Retrieve the coin prices
                coinGeckoManipulation(element_text, prices)  # Pass the prices data to the function
            else:
                logging.error("Page wasn't able to load!")

            # Countdown timer
            while countdown > 0:
                print(f"Time left: {countdown} seconds", end='\r')
                time.sleep(1)
                countdown -= 1

            clearTerminal()
            countdown = 60
            break
    except Exception as e:
        # Log the error
        logging.error(str(e))
        print("An error occurred. Please check the error log for more details.")

def USDModeManipulation(element_text, prices):
    STABLE_LIST = ["USDC", "DAI", "USDE"]  # List of stablecoin symbols to compare
    stablecoin_prices = {}  # Dictionary to store stablecoin prices
    asyncio.run(sendDiscordMessage(USDE_ID, "`" +  f"PROCEEDING [{constants.IterationCounter}]\n" + "`", BOT_TOKEN))

    try:
        data = json.loads(element_text)
        for key, value in data.items():
            symbol = value["symbol"]
            last_price = value["last_price"]
            if symbol in STABLE_LIST:
                stablecoin_prices[symbol] = last_price

        comparisons = [
            ("USDC", "DAI"),
            ("USDC", "USDE"),
            ("DAI", "USDE")
        ]

        for stable1, stable2 in comparisons:
            if stable1 in stablecoin_prices and stable2 in stablecoin_prices:
                price1 = stablecoin_prices[stable1]
                price2 = stablecoin_prices[stable2]
                ProfitPercent = calculateDifference(price1, price2)
                print(colorama.Back.LIGHTBLACK_EX + f"{stable1} vs {stable2}" + colorama.Style.RESET_ALL)
                print(f"{stable1} \t\t ${price1}")
                print(f"{stable2} \t\t ${price2}")
                asyncio.run(sendDiscordMessage(USDE_ID, f"{stable1} vs {stable2}\n" + f"{stable1} \t\t ${price1}\n" + f"{stable2} \t\t ${price2} " + "\n-----------------", BOT_TOKEN))

                if ProfitPercent < 0:
                    # Negative value, highlight ProfitPercent in MAGENTA
                    print("%Difference \t " + colorama.Back.MAGENTA + str(ProfitPercent) + "%" + colorama.Style.RESET_ALL)
                    # print("Purchase  \t" +  " "  + colorama.Back.MAGENTA + stable2 + colorama.Style.RESET_ALL)
                elif ProfitPercent > 0 and ProfitPercent < stableSetProfit:
                    # Positive value, highlight ProfitPercent in CYAN
                    print("%Difference \t " + colorama.Back.CYAN + str(ProfitPercent) + "%" + colorama.Style.RESET_ALL)
                    # print("Purchase  \t" +  " " + colorama.Back.CYAN + stable1 + colorama.Style.RESET_ALL)
                elif ProfitPercent == 0:
                    # Zero value, print ProfitPercent without highlight
                    print("%Difference \t " + str(ProfitPercent) + "%")
                if ProfitPercent > stableSetProfit:
                    print("%Difference \t " + colorama.Back.GREEN + str(ProfitPercent) + "%" + colorama.Style.RESET_ALL)
                    printRainbowText("Trade Found!")
                    # asyncio.run(sendDiscordMessage(USDE_ID, f"{stable1} vs {stable2}\n " + f"{stable1} \t\t ${price1}\n " + f"{stable2} \t\t ${price2} " + "\n-----------------", BOT_TOKEN))

                print()

    except json.JSONDecodeError:
        logging.error("Invalid JSON Data!")
        print(colorama.Back.RED + "Invalid JSON data" + colorama.Style.RESET_ALL)


def usdMode():
    clearTerminal()
    try:
        countdown = 60

        while True:
            driver = webdriver.Chrome()
            css_selector = "/html/body"  # Updated XPath selector
            element_text = SeleniumInitializer(driver, css_selector)
            driver.quit()

            if element_text is not None:
                prices = getCoinPrices()  # Retrieve the coin prices
                USDModeManipulation(element_text, prices)  # Pass the prices data to the function
            else:
                logging.error("Page wasn't able to load!")

            # Countdown timer
            while countdown > 0:
                print(f"Time left: {countdown} seconds", end='\r')
                time.sleep(1)
                countdown -= 1

            clearTerminal()
            countdown = 60
            break
    except Exception as e:
        # Log the error
        logging.error(str(e))
        print("An error occurred. Please check the error log for more details.")

    
def display_menu():
    print(f"{Back.GREEN}{Style.BRIGHT}Menu:{Style.RESET_ALL}")
    print("1) CoinGecko Mode")
    print("2) USD Mode")

def main():
    clearTerminal()
    display_ascii_art()
    display_menu()
    choice = input("Select an option (1-2): ")

    while True:
        if choice == "1":
            coinGeckoMode()
        elif choice == "2":
            usdMode()
        else:
            print("Invalid choice. Please select again.\n")

            

main()
