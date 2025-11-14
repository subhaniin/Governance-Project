from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import psycopg2

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://results.eci.gov.in/ResultAcGenNov2025/index.htm")

time.sleep(3)

rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

scraped_data = []   # <── collect your original rows

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    data = [c.text for c in cols]
    print(data)
    scraped_data.append(data)   # <── store for DB

driver.quit()

print("\nSCRAPED DATA STORED:", scraped_data)

# -----------------------------------
# LOAD INTO POSTGRESQL (VARCHAR)
# -----------------------------------

conn = psycopg2.connect(
    host="localhost",
    database="governance",
    user="postgres",
    password="Pqsql",
    port="5432"
)

cur = conn.cursor()

# Create table as VARCHAR
cur.execute("""
    DROP TABLE IF EXISTS party_results;
    CREATE TABLE party_results(
        party VARCHAR,
        won VARCHAR,
        leadings VARCHAR,
        total VARCHAR
    );
""")

# Insert every row exactly as scraped
for row in scraped_data:
    if len(row) == 4:  # ensure correct row
        cur.execute(
            "INSERT INTO party_results (party, won, leadings, total) VALUES (%s, %s, %s, %s)",
            row
        )

conn.commit()
cur.close()
conn.close()

print("\n✔ Data inserted into PostgreSQL successfully!")