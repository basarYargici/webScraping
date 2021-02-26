import time  # to delaying the process
import traceback  # if any error occurs, we will get it with traceback
import winsound  # to get and play the system sounds
import requests  # to connect the website and getting the HTML

from bs4 import BeautifulSoup  # to parse the webpage and search the specific elements

url = "https://www.investing.com/crypto/bitcoin/btc-usd"  # source link of data

# minimum and maximum count that we want pc to play beep sound if the currentValue is between them
minCount = "44,450.0"
maxCount = "46,000.0"

# we use try-except in case of any errors
try:
    # program will never stop until we kill it
    while True:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})  # connects to url
        soup = BeautifulSoup(page.text, 'html.parser')  # parses the page

        currentData = soup.find('div', {"class": "top bold inlineblock"})  # finds specific area that we want

        # our area has &nbsp part and we dont want it. we replace it with space and we remove new lines
        currentData = currentData.text.replace(' ', ' ')
        currentData = currentData.replace('\n ', ' ')

        value = ""
        newList = []

        # divides currentData according to new lines
        for index in range(0, len(currentData)):
            if currentData[index] == '\n' and value != "":
                newList.append(value)
                value = ""
                continue

            if currentData[index] != '\n':
                value += (currentData[index])

        currentValue = newList[0]
        currentChange = newList[1]
        currentPctChange = newList[2]
        txtStr = f"BTC current value \t\t\t\t= {currentValue} \n" \
                 f"BTC current change \t\t\t\t= {currentChange} \n" \
                 f"BTC current percentage change \t= {currentPctChange} "

        # save the scraped text
        with open('scraped_text.txt', 'w') as file:
            file.write(txtStr)

        # if currentValue is between given minCount and maxCount, system will play the beep voice
        print("wait start")
        if minCount < currentValue < maxCount:
            print("play music")
            winsound.Beep(500, 3000)

        print(txtStr)
        time.sleep(5)  # delay 5 seconds of execution of program
        print("wait done")

except:
    traceback.print_exc()
