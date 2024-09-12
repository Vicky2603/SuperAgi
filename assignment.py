from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.amazon.in")

# Enter "lg soundbar" in the search box and click on search button
driver.find_element(By.XPATH, "//input[@id='twotabsearchtextbox']").send_keys("lg soundbar")
driver.find_element(By.XPATH, "//input[@id='nav-search-submit-button']").click()

wait = WebDriverWait(driver, 10)

# Added wait - until the search result page is not loaded
wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='a-color-state a-text-bold']")))

products = driver.find_elements(By.XPATH, "//div[@class='a-section a-spacing-small a-spacing-top-small']")

hashmap = {}

for i in range(1, len(products)):
    price_xpath = f"(//div[@class='a-section a-spacing-small a-spacing-top-small'])[{i+1}]//span[@class='a-price']"
    name_xpath = f"(//div[@class='a-section a-spacing-small a-spacing-top-small'])[{i+1}]//span[@class='a-size-medium a-color-base a-text-normal']"
    try:
        name_is_displayed = driver.find_element(By.XPATH, name_xpath).is_displayed()
        if name_is_displayed:
            product_name = driver.find_element(By.XPATH, name_xpath).text
            hashmap[product_name] = 0   # Initially will assign as zero, because if product_price is not present then by default 0 will be initialized

        element_is_displayed = driver.find_element(By.XPATH, price_xpath).is_displayed()
        if element_is_displayed:
            product_price = driver.find_element(By.XPATH, price_xpath).text.replace("₹", "").replace(",", "")
            hashmap[product_name] = int(product_price)
            
    except Exception as e:
        pass


hashmap = dict(sorted(hashmap.items(), key=lambda item: item[1]))

# Output according to the sample provided in the Google Form
for key, val in hashmap.items():
    print(val, key)
    print()

driver.close()
