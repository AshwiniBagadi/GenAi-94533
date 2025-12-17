from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

driver.get("https://www.sunbeaminfo.in/internship")
print("Page Title:", driver.title)

driver.implicitly_wait(5)

# Scroll to bottom so dynamic content loads
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Click the "Available Internship Programs" toggle
plus_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
plus_button.click()

# Wait for the table to be visible inside the collapse
table_body = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//div[@id='collapseSix']//tbody")
    )
)

table_rows = table_body.find_elements(By.TAG_NAME, "tr")

for row in table_rows:
    cols = row.find_elements(By.TAG_NAME, "td")

    info = {
        "Technology": cols[0].text,
        "Aim": cols[1].text,
        "Prerequisite": cols[2].text,
        "Learning": cols[3].text,
        "Location": cols[4].text
    }

    print(info)

driver.quit()
