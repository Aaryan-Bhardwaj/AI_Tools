#!/usr/bin/env python

from __future__ import unicode_literals
import os
# from addict import Dict
os.environ["LANG"] = "en_US.UTF-8"

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

TIMEOUT = 45

DEFAULT_INPUTS_PARAMS = {
    "guidance_scale": 7.5,
    "image_dimensions": "768x768",
    "negative_prompt": "nsfw, illogical, ugly, harmful, nudity, text, faces, skin detail, pictures, people",
    "num_inference_steps": 130,
    "num_outputs": 1,
    "scheduler": "K_EULER",
    "seed": ""
}

def get_image_url(prompt, **kwargs):
    input_parameters = DEFAULT_INPUTS_PARAMS
    input_parameters["prompt"] = prompt
    input_parameters.update(kwargs)
    try:
        chrome_options = Options()
        if not input_parameters.get('not_headless', False):
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)
        driver.maximize_window()
        driver.get("https://replicate.com/stability-ai/stable-diffusion/versions/db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")

        form = driver.find_element(By.CSS_SELECTOR, 'body > main > div:nth-child(6) > div > div:nth-child(1) > form')
        select_elements = form.find_elements(By.CLASS_NAME, 'form-select')

        for element in select_elements:
            Select(element).select_by_value(input_parameters[element.get_attribute('name')])

        input_elements = []
        input_elements.extend(form.find_elements(By.CLASS_NAME, 'form-input'))
        input_elements.extend(form.find_elements(By.TAG_NAME, 'input'))

        for element in input_elements:
            element.get_attribute('value')
            element.send_keys("")
            element.clear()
            driver.execute_script("arguments[0].value = '';", element)
            element.send_keys(input_parameters[element.get_attribute('name')])

        driver.find_element(By.CSS_SELECTOR, "body > main > div:nth-child(6) > div > div:nth-child(1) > form > button.form-button.mr-2.relative").click()
        time.sleep(0.5)

        image_element_css_selector = "body > main > div:nth-child(6) > div > div:nth-child(2) > div:nth-child(2) > output > figure > div > div > div > a > img"
        WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, image_element_css_selector))
        )

        image_url = driver.find_element(By.CSS_SELECTOR, image_element_css_selector).get_attribute("src")
        driver.close()
        driver.quit()

        return image_url

    except TimeoutException:
        error_element = driver.find_element(By.CSS_SELECTOR, "body > main > div:nth-child(6) > div > div:nth-child(2) > p")
        driver.quit()
        raise ValueError(error_element.text)
   

