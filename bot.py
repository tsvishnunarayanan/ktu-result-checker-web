import os
import time
import uuid
import requests
import warnings
import urllib3
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
uc.Chrome.__del__ = lambda self: None

# Env variables
USERNAME = os.getenv("KTU_ID")
PASSWORD = os.getenv("KTU_PASS")
SEMESTER = os.getenv("KTU_SEM", "S4")
TELEGRAM_BOT_TOKEN = os.getenv("TG_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT")

LOGIN_URL = "https://app.ktu.edu.in/login.htm"
RESULT_URL = "https://app.ktu.edu.in/eu/res/semesterGradeCardListing.htm"


def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})
    except:
        pass


def send_telegram_file(file_path, caption=""):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(file_path, "rb") as f:
            requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption}, files={"document": f})
    except:
        pass


def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    return uc.Chrome(options=options)


def wait_for_valid_page(driver, url):
    attempt = 1
    while True:
        try:
            driver.get(url)
            time.sleep(3)
            page = driver.page_source.lower()
            if any(err in page for err in ["504 gateway", "502 bad gateway", "500", "403", "unavailable"]):
                print(f"Server error attempt {attempt}")
            elif "ktu" in page or "username" in page:
                return True
        except:
            pass
        attempt += 1
        time.sleep(3)


def is_logged_out(driver):
    return "login" in driver.current_url or "session expired" in driver.page_source.lower()


def login(driver):
    if not wait_for_valid_page(driver, LOGIN_URL):
        return False
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "btn-login").click()
        time.sleep(3)
        return "login" not in driver.current_url.lower()
    except:
        return False


def go_to_result_page(driver):
    return wait_for_valid_page(driver, RESULT_URL)


def select_semester(driver):
    try:
        if is_logged_out(driver):
            return False
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "semesterGradeCardListingSearchForm_semesterId")))
        driver.find_element(By.ID, "semesterGradeCardListingSearchForm_semesterId").send_keys(SEMESTER)
        return True
    except:
        return False


def search_result(driver):
    try:
        if is_logged_out(driver):
            return False
        driver.find_element(By.ID, "semesterGradeCardListingSearchForm_search").click()
        time.sleep(3)
        return True
    except:
        return False


def is_result_present(driver):
    page = driver.page_source.lower()
    if any(e in page for e in ["504", "502", "500", "403", "unavailable"]):
        return "error"
    if is_logged_out(driver):
        return "expired"
    if 'semester grade card cannot be generated' in page:
        return "incomplete"
    if 'id="errormaindiv"' in page and 'semester grade cards not available' in page:
        return False
    if "<strong>semester grade card</strong>" in page:
        return True
    return False


def fetch_exam_result_from_profile(driver):
    try:
        wait_for_valid_page(driver, "https://app.ktu.edu.in/eu/stu/studentBasicProfile.htm")
        if is_logged_out(driver):
            return "Session expired", None
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "viewProfile"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "examResultTab"))).click()
        time.sleep(2)
        all_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.well.col-sm-12')
        for block in all_blocks:
            label = block.find_element(By.TAG_NAME, "label").text.lower()
            if f"{SEMESTER.lower()} (r,s)" in label:
                link = block.find_element(By.LINK_TEXT, "Examination Grades").get_attribute("href")
                driver.get("https://app.ktu.edu.in" + link if link.startswith("/") else link)
                time.sleep(2)
                filename = f"KTU_{SEMESTER}_{uuid.uuid4().hex}.png"
                path = os.path.join("static", filename)
                os.makedirs("static", exist_ok=True)
                driver.save_screenshot(path)
                return f"Semester {SEMESTER} incomplete — showing grades.", path
        return "No (R,S) exam found.", None
    except Exception as e:
        return f"Error: {e}", None


def export_result(driver):
    try:
        href = driver.find_element(By.ID, "back").get_attribute("href")
        if href.startswith("/"):
            href = "https://app.ktu.edu.in" + href
        session = requests.Session()
        for c in driver.get_cookies():
            session.cookies.set(c['name'], c['value'])
        res = session.get(href, verify=False)
        if res.ok:
            filename = f"KTU_{SEMESTER}_{uuid.uuid4().hex}.pdf"
            path = os.path.join("static", filename)
            os.makedirs("static", exist_ok=True)
            with open(path, "wb") as f:
                f.write(res.content)
            return f"Result available for {SEMESTER}.", path
        return "Download failed.", None
    except Exception as e:
        return f"Export error: {e}", None


def run_checker():
    driver = setup_driver()
    selected = False
    try:
        if not login(driver):
            send_telegram_message("❌ Login failed. Check credentials.")
            return
        if not go_to_result_page(driver):
            send_telegram_message("❌ Failed to reach result page.")
            return

        while True:
            status = is_result_present(driver)
            if status == True:
                msg, file = export_result(driver)
                send_telegram_message(msg)
                send_telegram_file(file, msg)
                break
            elif status == "expired":
                login(driver)
                go_to_result_page(driver)
                selected = False
                continue
            elif status == "error":
                go_to_result_page(driver)
                selected = False
                continue
            elif status == "incomplete":
                msg, file = fetch_exam_result_from_profile(driver)
                if file:
                    send_telegram_message(msg)
                    send_telegram_file(file, msg)
                else:
                    send_telegram_message(msg)
                break

            if not selected:
                if select_semester(driver):
                    selected = True
            search_result(driver)
            time.sleep(15)
    finally:
        try:
            driver.quit()
        except:
            pass


if __name__ == "__main__":
    run_checker()
