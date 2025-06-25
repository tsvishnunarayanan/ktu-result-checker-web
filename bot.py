import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
uc.Chrome.__del__ = lambda self: None
import requests
import time
import os
import uuid

def is_logged_out(driver):
    return "login" in driver.current_url or "session expired" in driver.page_source.lower()

def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    chrome_path = os.getenv("GOOGLE_CHROME_BIN", "chrome-linux64/chrome")
    driver_path = "chromedriver-linux64/chromedriver"

    return uc.Chrome(browser_executable_path=chrome_path, driver_executable_path=driver_path, options=options)


def wait_for_valid_page(driver, url):
    attempt = 1
    while True:
        try:
            driver.get(url)
            time.sleep(3)
            page = driver.page_source.lower()
            if any(e in page for e in ["504 gateway", "502 bad gateway", "403 forbidden", "500 internal server", "service unavailable"]):
                print(f"🔁 Server error on attempt {attempt}")
            elif "ktu" in page or "username" in page or "semester" in page:
                return True
        except:
            pass
        attempt += 1
        time.sleep(3)

def login(driver, USERNAME, PASSWORD):
    if not wait_for_valid_page(driver, "https://app.ktu.edu.in/login.htm"):
        return False
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "btn-login").click()
        time.sleep(3)
        return "login" not in driver.current_url.lower()
    except:
        return False

def go_to_result_page(driver):
    return wait_for_valid_page(driver, "https://app.ktu.edu.in/eu/res/semesterGradeCardListing.htm")

def select_semester(driver, SEMESTER):
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
    try:
        page = driver.page_source.lower()
        if any(e in page for e in ["504 gateway", "502 bad gateway", "500 internal", "403 forbidden", "service unavailable"]):
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
    except:
        return "error"

def fetch_exam_result_from_profile(driver, SEMESTER):
    try:
        wait_for_valid_page(driver, "https://app.ktu.edu.in/eu/stu/studentBasicProfile.htm")
        if is_logged_out(driver):
            return "Session expired", None, None
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "viewProfile"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "examResultTab"))).click()
        time.sleep(2)
        all_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.well.col-sm-12')
        for block in all_blocks:
            label = block.find_element(By.TAG_NAME, "label").text.lower()
            if f"{SEMESTER.lower()} (r,s)" in label:
                exam_link = block.find_element(By.LINK_TEXT, "Examination Grades").get_attribute("href")
                driver.get("https://app.ktu.edu.in" + exam_link if exam_link.startswith("/") else exam_link)
                time.sleep(3)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                filename = f"KTU_{SEMESTER}_{uuid.uuid4().hex}.png"
                path = os.path.join("static", filename)
                driver.save_screenshot(path)
                return f"Semester {SEMESTER} incomplete — showing available grades.", None, path
        return "No regular (R,S) exam found.", None, None
    except Exception as e:
        return f"Failed to fetch profile result: {e}", None, None

def export_result(driver, SEMESTER):
    try:
        export_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "back")))
        href = export_button.get_attribute("href")
        if href.startswith("/"):
            href = "https://app.ktu.edu.in" + href
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])
        response = session.get(href, verify=False)
        if response.ok:
            filename = f"KTU_{SEMESTER}_{uuid.uuid4().hex}.pdf"
            path = os.path.join("static", filename)
            os.makedirs("static", exist_ok=True)
            with open(path, "wb") as f:
                f.write(response.content)
            return f"Result available for {SEMESTER}.", path, None
        else:
            return "Failed to download result.", None, None
    except Exception as e:
        return f"Export failed: {e}", None, None

def run_checker_web(USERNAME, PASSWORD, SEMESTER):
    driver = setup_driver()
    has_selected = False
    try:
        if not login(driver, USERNAME, PASSWORD):
            return "Login failed. Check credentials.", None, None
        if not go_to_result_page(driver):
            return "Failed to reach result page.", None, None

        while True:
            status = is_result_present(driver)
            if status == True:
                return export_result(driver, SEMESTER)
            elif status == "expired":
                if not login(driver, USERNAME, PASSWORD):
                    return "Session expired and re-login failed.", None, None
                if not go_to_result_page(driver):
                    return "Re-login successful but failed to reach result page.", None, None
                has_selected = False
                continue
            elif status == "error":
                if not go_to_result_page(driver):
                    return "Server error, retrying failed.", None, None
                has_selected = False
                continue
            elif status == "incomplete":
                return fetch_exam_result_from_profile(driver, SEMESTER)

            if not has_selected:
                if select_semester(driver, SEMESTER):
                    has_selected = True
                else:
                    return "Failed to select semester.", None, None

            if not search_result(driver):
                return "Failed to click search.", None, None
            time.sleep(10)
    finally:
        try:
            driver.quit()
        except:
            pass
