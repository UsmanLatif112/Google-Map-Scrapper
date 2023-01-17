import time, csv
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Make CSV to write Data


def make_csv(filename: str, data, new=True):
    """make a csv file with the given filename
    and enter the data
    """
    mode = "w" if new else "a"
    with open(filename, mode, newline="") as f:
        f.writelines(data)


make_csv("Google Data.csv", "Google Map Scraping data\n", new=True)
make_csv("Google Data.csv", "Business Name;Address;Website;Phone#\n", new=False)

# open google map

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

# Read Csv to get values

with open("Copy.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        value = row[0]

        # Go to Google Maps

        driver.get("https://www.google.com/maps")
        time.sleep(1)

        search = driver.find_element(By.XPATH, "//*[@id='searchboxinput']").send_keys(
            f"Gym in {value}"
        )
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[@id='searchboxinput']").send_keys(Keys.ENTER)
        time.sleep(1)
        # Scroll or load all data

        while True:
            try:
                Scrol = driver.find_element(By.XPATH, "//div[@role='feed']").send_keys(
                    Keys.SPACE
                )
                time.sleep(3)
                element = WebDriverWait(driver, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@Class='HlvSq']"))
                )
                print(element.text)
                break

            except:
                pass

        # Get the element len after scrol or load all data
        time.sleep(1)

        elementss = driver.find_elements(
            By.XPATH, "//*[@Class='qBF1Pd fontHeadlineSmall']"
        )
        elementss = elementss[2:]

        total_elements = len(elementss)
        print("Total elements", total_elements)

        elementxs = driver.find_elements(
            By.XPATH,
            "//*[@Class='hfpxzc'][@jsan='7.hfpxzc,0.aria-label,8.href,0.jsaction,0.jslog']",
        )

        total_elements = len(elementxs)
        print("Total elements", total_elements)

        # Collect data by clicking one by one

        if len(elementxs) == total_elements:
            for element in elementxs:
                time.sleep(3)
                try:
                    element.click()
            
                    time.sleep(2)
                    Business = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                        (By.XPATH, "//*[@class='DUwDvf fontHeadlineLarge']")
                    )
                    )
                    make_csv("Google Data.csv", f"{Business.text};", new=False)
                    time.sleep(1)
                    Scrol_l = driver.find_element(
                        By.CSS_SELECTOR,
                        "#QA0Szd > div > div > div.w6VYqd > div.bJzME.Hu9e2e.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf",
                    ).send_keys(Keys.SPACE)

                    data = driver.find_elements(By.CSS_SELECTOR, ".AeaXub")

                    detail = ""
                    img_list = [
                        "https://maps.gstatic.com/mapfiles/maps_lite/images/2x/ic_plus_code.png"
                    ]
                    for element in data:
                        try:
                            src = element.find_element(
                                By.CSS_SELECTOR, " img"
                            ).get_attribute("src")
                        except:
                            src = ""
                        if src and src not in img_list:
                            img_list.append(src)
                            text: str = element.text
                            if all(
                                (
                                    not text.__contains__("Located in:"),
                                    not text.__contains__("Send to your phone"),
                                    not text.__contains__("Claim this business"),
                                    not text.__contains__("Identifies as women-owned"),
                                    not text.__contains__("linktr.ee"),
                                    not text.__contains__("LGBTQ+ friendly"),
                                    not text.__contains__("bit.ly"),
                                    not text.__contains__("Menu"),
                                    not text.__contains__("Floor")
                                )
                            ):
                                print(text, src)
                                if text not in detail:
                                    detail += f"{element.text};"
                    detail = detail[:-1]
                    make_csv("Google Data.csv", f"{detail}\n", new=False)
                    time.sleep(1)
                except:
                    pass
time.sleep(5)
driver.quit()
