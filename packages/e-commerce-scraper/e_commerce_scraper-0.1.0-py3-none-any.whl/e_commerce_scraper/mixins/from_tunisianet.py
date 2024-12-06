import json
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, Any

from typing import Dict, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from e_commerce_scraper.mixins.utils import wait_for_element_to_be_clickable, get_text_by_javascript, \
    wait_for_all_elements_to_be_present, wait_for_element_to_be_present


class FromTunisianet:

    tunisianet_website = "tunisianet.com.tn"


    def _sexy_function(self, parent_categ_elem):
        result = []

        all_lis = wait_for_all_elements_to_be_present(
            parent_categ_elem, (By.XPATH, ".//li[contains(@class, 'menu-item')]")
        )

        current_header = None
        current_items = []

        for li in all_lis:
            if "item-header" in li.get_attribute("class"):
                if current_header:
                    result.append({
                        "header": get_text_by_javascript(self._driver, current_header).strip(),
                        "count": len(current_items),
                        "menus": current_items
                    })
                current_header = li
                current_items = []
            else:
                current_items.append(wait_for_element_to_be_present(li, (By.TAG_NAME, "a")).get_attribute('href'))

        if current_header:
            result.append({
                "categ": get_text_by_javascript(self._driver, current_header).strip(),
                "count": len(current_items),
                "menus": current_items
            })
        return result

    def _getSubCategoryMenus_tunisianet(self, levels):

        self.logger.info("start selecting the target categories ...")

        bigs = []
        bigs_categs = wait_for_all_elements_to_be_present(self._driver, (By.XPATH, "//ul[@class = 'menu-content top-menu']/li"))
        for bb in bigs_categs:
            big_categ_name = get_text_by_javascript(self._driver, wait_for_element_to_be_present(bb, (By.XPATH, "./div[@class = 'icon-drop-mobile']"))).strip().replace('  ','').replace('\n','')
            parent_sub_categs = self._sexy_function(bb)

            bigs.append({
                "big": big_categ_name,
                "categs": parent_sub_categs
            })
        target_parent_categ = bigs[levels[0]-1]
        result = []
        for sub, count in zip(target_parent_categ["categs"], levels[1:]):
            result.extend(sub["menus"][:count])
            if count > len(sub["menus"]):
                self.logger.info("sub-category index out of range ... will take the whole list")

        self.logger.info(f"{len(result)} categories selected")
        return result

    def getProductsFromTunisianet(self, levels, nb_product_for_each_subcategory):
        self._driver.get("https://"+self.tunisianet_website)
        menus = self._getSubCategoryMenus_tunisianet(levels=levels)
        yield from self._getProductsCategory_tunisianet(menus, nb_product_for_each_subcategory)

    def _getProductsCategory_tunisianet(self, categs_links, nb_products):
        global_prods_links = []
        for categ_link in categs_links:
            self._driver.get(categ_link)
            prods_links = []
            while True:
                productsDivs = wait_for_all_elements_to_be_present(self._driver, (
                    By.XPATH,
                    "//div[contains(@class,'item-product')]",
                ))
                for elem in productsDivs:
                    prod_link = (
                        elem
                        .find_element(By.XPATH, ".//h2[contains(@class, 'h3 product-title')]//a")
                        .get_attribute("href")
                    )
                    prods_links.append(prod_link)
                if len(prods_links) >= nb_products:
                    prods_links = prods_links[:nb_products]
                    break
                if not self._jump_to_next_page_tunisianet():
                    break
            global_prods_links.extend(prods_links)

        for link in global_prods_links:
            yield self._getSingleProduct_tunisianet(link)

    def _getSingleProduct_tunisianet(self, prod_link):
        self._driver.get(prod_link)

        ''' reference is used is data cleaning phase to removed duplicates  '''
        reference = wait_for_element_to_be_present(self._driver,(By.XPATH, "//span[@itemprop = 'sku']")).text


        name = wait_for_element_to_be_present(self._driver,(By.XPATH, "//h1[@itemprop='name']")).text
        in_stock = (
            True
            if wait_for_element_to_be_present(self._driver,(
                By.XPATH, "//span[@class='in-stock']"
            )).text
            == "En stock"
            else False
        )
        price = wait_for_element_to_be_present(self._driver,(
            By.XPATH,
            "//span[@itemprop = 'price']",
        )).text.replace(" DT", "")
        description = wait_for_element_to_be_present(self._driver,(
            By.XPATH, "//div[@itemprop='description']"
        )).text

        category = wait_for_element_to_be_present(self._driver,(By.XPATH, "//ol[@itemtype='http://schema.org/BreadcrumbList']/li[position()=last()-1]")).text


        data = {
            "website": self.tunisianet_website,
            "product_reference_in_website": reference,
            "product_name": name,
            "product_category": category,
            "product_manufacturer": self._get_manufacturer_tunisianet(),
            "in_stock": in_stock,
            "product_price": price,
            "product_url": prod_link,
            "product_description": description,
            "availability": self._get_availability_tunisianet(),
            "technical_sheet": self._get_technical_sheet_tunisianet(),
            "product_images": self._get_product_images_tunisianet()
        }
        return data

    def _get_availability_tunisianet(self):
        try:
            disp_div = self._driver.find_element(
                By.ID, "product-availability-store-mobile"
            )
            places_avail_cols = wait_for_all_elements_to_be_present(disp_div,
                                                                    (By.XPATH, ".//div[contains(@class, 'stores')]"))
            availabilities = dict()
            places_elems = wait_for_all_elements_to_be_present(places_avail_cols[0], (
            By.XPATH, ".//div[contains(@class, 'store-availability')]"))
            avail_elems = wait_for_all_elements_to_be_present(places_avail_cols[1], (
            By.XPATH, ".//div[contains(@class, 'store-availability')]"))
            for place_elem, avail_elem in zip(places_elems, avail_elems):
                place = get_text_by_javascript(self._driver, place_elem)
                status = get_text_by_javascript(self._driver, avail_elem)
                availabilities[place] = status
            return availabilities
        except:
           self.logger.info('availability data not collected')
           return {}
    def _get_technical_sheet_tunisianet(self):

        try:
            self._driver.execute_script("arguments[0].scrollIntoView(true);",
                                        wait_for_element_to_be_present(self._driver, (
                                        By.XPATH, "//a[@aria-controls = 'product-details']")))
            wait_for_element_to_be_clickable(self._driver, (By.XPATH, "//a[@aria-controls = 'product-details']"))
            sleep(2)
            table = wait_for_all_elements_to_be_present(self._driver, (By.CLASS_NAME, "product-features"))[0]
            self._driver.execute_script("arguments[0].scrollIntoView(true);", table)
            keys = wait_for_all_elements_to_be_present(table, (By.TAG_NAME, "dt"))
            values = wait_for_all_elements_to_be_present(table, (By.TAG_NAME, "dd"))
            technical_data = dict()
            for key, value in zip(keys, values):
                technical_data[key.text] = value.text

            if len(technical_data.keys()) <= 1:
                self.logger.error(f"collected technical sheet:{len(technical_data.keys())} [tunisianet]")
            return technical_data
        except:
            self.logger.info('technical sheet not collected')
            return {}


    def _get_product_images_tunisianet(self):
        try:
            images_elems = wait_for_all_elements_to_be_present(self._driver ,(By.XPATH, "//ul[contains(@class, 'js-qv-product-images')]//img"))
            return [img.get_attribute('src') for img in images_elems]
        except:
            return [wait_for_element_to_be_present(self._driver, (By.CLASS_NAME, "js-qv-product-cover")).get_attribute('src')]
    def _jump_to_next_page_tunisianet(self):
        try:
            wait_for_element_to_be_clickable(self._driver, (By.XPATH, "//ul[contains(@class, 'page-list')]/li[position()=last()]"))
            return True
        except Exception as e:
            self.logger.info(f"failed to jump to next page: {e}")
            return False

    def _get_manufacturer_tunisianet(self):
        try:
            return wait_for_element_to_be_present(self._driver, (By.XPATH, "//div[@class = 'product-manufacturer']//img")).get_attribute('alt')
        except:
            self.logger.info("manufacturer not loaded [mytek]")
            return ""