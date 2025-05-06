from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

URL = "https://www.amazon.in/Surf-Excel-Detergent-Specially-designed/dp/B0CKW4VGLK/ref=pd_vtp_d_sccl_3_2/261-6842355-2401352?pd_rd_w=M6917&content-id=amzn1.sym.f7d06212-3555-43aa-92e8-0a66aa167653&pf_rd_p=f7d06212-3555-43aa-92e8-0a66aa167653&pf_rd_r=BS19PMM3VNYY3FSSPCYK&pd_rd_wg=NsI3R&pd_rd_r=cefed650-50bb-43b5-bf43-0c43393d7937&pd_rd_i=B0CKW4VGLK&th=1"  # Replace with your product's URL
TARGET_PRICE = 20000

options = Options()
options.add_argument("--headless")  # Optional: run in background
options.add_argument("window-size=1920x1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(options=options)
driver.get(URL)

time.sleep(3)
try:
    # Extract product title
    title = driver.find_element(By.ID, "productTitle").text.strip()
    print(f"Product Title: {title}")

    # Find all price elements on the page
    price_elements = driver.find_elements(By.CSS_SELECTOR, '.a-price')

    for elem in price_elements:
        price_text = elem.text.strip()

        # DEBUG: Print the raw price text for inspection
        print(f"DEBUG - Raw price text: {price_text}")
        
        # Ensure the price contains the ₹ symbol and process it
        if price_text and "₹" in price_text:
            # Clean up: remove any unwanted newlines, spaces, or commas
            cleaned_price = price_text.replace("\n", " ").replace(",", "").strip()

            # Remove "00" after the space, if it's present
            cleaned_price = cleaned_price.split(" ")[0]  # Keep only the part before the space

            # DEBUG: Print cleaned price
            print(f"DEBUG - Cleaned price text: {cleaned_price}")

            # Convert cleaned price to float, after removing ₹ symbol
            price_value = float(cleaned_price.replace("₹", ""))  # Convert to float

            # DEBUG: Print the final price value
            print(f"Current price: ₹{price_value}")
            
            # Compare with target price
            if price_value < TARGET_PRICE:
                print("🔔 Price dropped below target!")
            else:
                print("Price still above target.")
            break  # Exit after processing the first valid price

    else:
        print("❌ Error: No valid price found.")

except Exception as e:
    print("❌ Error:", e)

finally:
    driver.quit()
