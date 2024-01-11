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

            if channel:
                # Send the customized message to the channel
                await channel.send(message)
            else:
                print(f"Error: Channel with ID {channel_id} not found.")
        except Exception as e:
            print(f"An error occurred with the bot: {str(e)}")
        finally:
            # Stop the bot and close the event loop
            await bot.close()

def SeleniumInitializer(driver, css_selector: str, timeout: int = 10):
    # Set the page load timeout for the WebDriver instance
    driver.set_page_load_timeout(timeout)

    # Increment the iteration counter
    constants.IterationCounter += 1

    try:
        # Open the specified URL in the WebDriver
        driver.get("https://api.energiswap.exchange/v1/assets")

        # Wait for the specified element to be present in the DOM
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.XPATH, css_selector)))

        # Print status information for the current iteration
        print(colorama.Back.LIGHTBLUE_EX + colorama.Style.BRIGHT + f"PROCEEDING [{constants.IterationCounter}]\n" + colorama.Style.RESET_ALL)

        # Additional code to find the specific HTML element with the given XPath selector
        element = driver.find_element(By.XPATH, css_selector)
        return element.text

    except TimeoutException:
        # Handle timeout exception, print error message, and log the error
        print(colorama.Back.RED + "Timed out waiting for page to load" + colorama.Style.RESET_ALL)
        logging.error("Timed out waiting for page to load")
        return None

def convertNameToID(name):
    # Iterate through the NAME_ID_CONVERTER list to find a matching name
    for item in NAME_ID_CONVERTER:
        if item[1] == name:
            # Return the corresponding API ID if a match is found
            return item[0]

    # Return None if no matching name is found
    return None

def printRainbowText(text):
    # Define a list of rainbow colors
    rainbow_colors = [colorama.Fore.RED, colorama.Fore.YELLOW, colorama.Fore.GREEN,
                      colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.CYAN]

    # Set the color for resetting after printing
    reset_color = colorama.Fore.RESET

    # Iterate through each character in the text and print with alternating rainbow colors
    for i, char in enumerate(text):
        color = rainbow_colors[i % len(rainbow_colors)]
        print(color + char, end='')

    # Reset the color after printing the entire text
    print(reset_color)

def calculateDifference(last_price, coingecko_price):
    # Calculate the numerator and denominator for percent difference
    numerator = (coingecko_price - last_price)
    denominator = (last_price + coingecko_price) / 2

    # Calculate the percent difference
    percent_difference = (numerator / denominator) * 100

    # Return the calculated percent difference
    return percent_difference

def getCoinPrices():
    # Define the URL for retrieving coin prices from CoinGecko API
    url = "https://api.coingecko.com/api/v3/simple/price?ids=energi%2Cenergi-dollar%2Cdai%2Cethereum%2Cbitcoin%2Cusd-coin&vs_currencies=usd"

    # Make a GET request to the API endpoint
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the JSON data from the response
        return response.json()
    else:
        # Print an error message if the request was not successful
        print("Error occurred. Status code:", response.status_code)

    # Return None in case of an error
    return None

def clearTerminal():
    # Check the operating system and clear the terminal screen accordingly
    if os.name == 'posix':  # For UNIX-based systems (Linux, macOS)
        _ = os.system('clear')
    else:  # For Windows
        _ = os.system('cls')

def coinGeckoManipulation(element_text, prices):
    # Use asyncio to send a Discord message with iteration information
    asyncio.run(sendDiscordMessage(CG_ID, "`" + f"PROCEEDING [{constants.IterationCounter}]\n" + "`", BOT_TOKEN))

    try:
        # Load JSON data from the provided element_text
        data = json.loads(element_text)

        # Iterate through the data and extract relevant information
        for key, value in data.items():
            name = value["name"]
            symbol = value["symbol"]
            last_price = value["last_price"]
            api_id = convertNameToID(name)

            # Check if the coin's API ID is present in the prices data
            if api_id in prices:
                coingecko_price = prices[api_id].get("usd")

                # Calculate the percentage difference between Coingecko and EnergiSwap prices
                ProfitPercent = calculateDifference(last_price, coingecko_price)

                # Print coin information with appropriate formatting and highlighting
                print(colorama.Back.LIGHTBLACK_EX + str((name)) + colorama.Style.RESET_ALL)
                print("symbol: \t " + symbol)
                print("Coingecko: \t $" + str(coingecko_price))
                print("EnergiSwap: \t $" + str(last_price))

                if ProfitPercent < 0:
                    # Negative value, highlight ProfitPercent in MAGENTA
                    print("%Difference \t " + colorama.Back.MAGENTA + str(ProfitPercent) + "%" + colorama.Style.RESET_ALL)
                elif 0 < ProfitPercent < userSetProfit:
                    # Positive value within user-defined limit, highlight ProfitPercent in CYAN
                    print("%Difference \t " + colorama.Back.CYAN + str(ProfitPercent) + "%" + colorama.Style.RESET_ALL)
                elif ProfitPercent == 0:
                    # Zero value, print ProfitPercent without highlight
                    print("%Difference \t " + str(ProfitPercent) + "%")

                # Print an empty line for better readability
                print()

    except json.JSONDecodeError:
        # Log an error for invalid JSON data
        logging.error("Invalid JSON Data!")
        print(colorama.Back.RED + "Invalid JSON data" + colorama.Style.RESET_ALL)

def coinGeckoMode():
    # Clear the terminal screen
    clearTerminal()

    try:
        # Initialize countdown timer
        countdown = 60

        while True:
            # Initialize a new Chrome WebDriver instance
            driver = webdriver.Chrome()

            # Define the CSS selector for the target element
            css_selector = "/html/body"

            # Retrieve the text content of the specified element using a helper function
            element_text = SeleniumInitializer(driver, css_selector)

            # Close the WebDriver instance
            driver.quit()

            # Check if the element text was successfully retrieved
            if element_text is not None:
                # Retrieve current coin prices
                prices = getCoinPrices()

                # Execute manipulation function with the retrieved data
                coinGeckoManipulation(element_text, prices)
            else:
                # Log an error if the page fails to load
                logging.error("Page wasn't able to load!")

            # Countdown timer for refreshing the process
            while countdown > 0:
                print(f"Time left: {countdown} seconds", end='\r')
                time.sleep(1)
                countdown -= 1

            # Reset the countdown and clear the terminal for the next iteration
            clearTerminal()
            countdown = 60

            # Exit the loop after each iteration
            break

    except Exception as e:
        # Log any encountered exceptions
        logging.error(str(e))
        print("An error occurred. Please check the error log for more details.")

def USDModeManipulation(element_text, prices):
    # List of stablecoin symbols to compare
    STABLE_LIST = ["USDC", "DAI", "USDE"]

    # Dictionary to store stablecoin prices
    stablecoin_prices = {}

    # Use asyncio to send a Discord message with iteration information
    asyncio.run(sendDiscordMessage(USDE_ID, "`" + f"PROCEEDING [{constants.IterationCounter}]\n" + "`", BOT_TOKEN))

    try:
        # Load JSON data from the provided element_text
        data = json.loads(element_text)

        # Extract relevant information for stablecoins from the data
        for key, value in data.items():
            symbol = value["symbol"]
            last_price = value["last_price"]
            if symbol in STABLE_LIST:
                stablecoin_prices[symbol] = last_price

        # Define pairs of stablecoins for comparison
        comparisons = [
            ("USDC", "DAI"),
            ("USDC", "USDE"),
            ("DAI", "USDE")
        ]

        # Iterate through stablecoin pairs and compare their prices
        for stable1, stable2 in comparisons:
            if stable1 in stablecoin_prices and stable2 in stablecoin_prices:
                price1 = stablecoin_prices[stable1]
                price2 = stablecoin_prices[stable2]
                ProfitPercent = calculateDifference(price1, price2)

                # Print comparison information with appropriate formatting and highlighting
                print(colorama.Back.LIGHTBLACK_EX + f"{stable1} vs {stable2}" + colorama.Style.RESET_ALL)
                print(f"{stable1} \t\t ${price1}")
                print(f"{stable2} \t\t ${price2}")

                # Use asyncio to send a Discord message with comparison details
                asyncio.run(sendDiscordMessage(USDE_ID, f"{stable1} vs {stable2}\n" + f"{stable1} \t\t ${price1}\n" + f"{stable2} \t\t ${price2} " + "\n-----------------", BOT_TOKEN))

                if ProfitPercent < 0:
                    # Negative value, highlight ProfitPercent in MAGENTA
                    print("%Difference \t " + colorama.Back.MAGENTA + str(ProfitPercent) + "%" + colorama.Style.RESET_ALL)
                elif 0 < ProfitPercent < stableSetProfit:
                    # Positive value within user-defined limit, highlight ProfitPercent in CYAN
                    print("%Difference \t " + colorama.Back.CYAN + str(ProfitPercent) + "%" + colorama.Style.RESET_ALL)
                elif ProfitPercent == 0:
                    # Zero value, print ProfitPercent without highlight
                    print("%Difference \t " + str(ProfitPercent) + "%")

                if ProfitPercent > stableSetProfit:
                    # ProfitPercent greater than stableSetProfit, highlight in GREEN and print a success message
                    print("%Difference \t " + colorama.Back.GREEN + str(ProfitPercent) + "%" + colorama.Style.RESET_ALL)
                    printRainbowText("Trade Found!")

                # Print an empty line for better readability
                print()

    except json.JSONDecodeError:
        # Log an error for invalid JSON data
        logging.error("Invalid JSON Data!")
        print(colorama.Back.RED + "Invalid JSON data" + colorama.Style.RESET_ALL)

def usdMode():
    try:
        # Clear the terminal screen
        clearTerminal()

        # Initialize countdown timer
        countdown = 60

        while True:
            # Initialize a new Chrome WebDriver instance
            driver = webdriver.Chrome()

            # Define the CSS selector for the target element
            css_selector = "/html/body"

            # Retrieve the text content of the specified element using a helper function
            element_text = SeleniumInitializer(driver, css_selector)

            # Close the WebDriver instance
            driver.quit()

            # Check if the element text was successfully retrieved
            if element_text is not None:
                # Retrieve current coin prices
                prices = getCoinPrices()

                # Execute manipulation function with the retrieved data
                USDModeManipulation(element_text, prices)
            else:
                # Log an error if the page fails to load
                logging.error("Page wasn't able to load!")

            # Countdown timer for refreshing the process
            while countdown > 0:
                print(f"Time left: {countdown} seconds", end='\r')
                time.sleep(1)
                countdown -= 1

            # Reset the countdown and clear the terminal for the next iteration
            clearTerminal()
            countdown = 60

            # Exit the loop after each iteration
            break

    except Exception as e:
        # Log any encountered exceptions
        logging.error(str(e))
        print("An error occurred. Please check the error log for more details.")
 
def display_menu():
    # Display a menu with CoinGecko and USD modes
    print(f"{Back.GREEN}{Style.BRIGHT}Menu:{Style.RESET_ALL}")
    print("1) CoinGecko Mode")
    print("2) USD Mode")

def main():
    # Clear the terminal screen
    clearTerminal()

    # Display ASCII art representing the program
    display_ascii_art()

    # Display the menu for user selection
    display_menu()

    # Prompt the user to select an option (1-2)
    choice = input("Select an option (1-2): ")

    # Continue looping until a valid option is selected
    while True:
        # Check the user's choice and execute the corresponding mode
        if choice == "1":
            coinGeckoMode()  # Execute CoinGecko mode
        elif choice == "2":
            usdMode()  # Execute USD mode
        else:
            # Display an error message for invalid choices
            print("Invalid choice. Please select again.\n")

main()
