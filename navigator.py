import time
import logging
import yaml

from selenium import webdriver

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SetupDriver():

    def __init__(self, browser):
        if browser.lower() == 'firefox':
            self.driver = webdriver.Firefox()

    def __enter__(self):
        return self.driver

    def __exit__(self, *args):
        self.driver.quit()

def main():

    with open('config.yaml') as f:
        config = yaml.load(f)

    with open('macros.yaml') as f:
        macros = yaml.load(f)

    defined_actions = set(['open', 'click', 'wait'])

    for macro_counter, macro in enumerate(macros['macros']):
        print('Macro #{c}'.format(c=macro_counter))
        for properties in macro:
            process(macro[properties]['steps'])

def process(steps):
    with SetupDriver('firefox') as driver:
        for i, action in enumerate(steps):
            print(i, action)
            try:
                if action.get('open'):
                    driver.get(action['open'])
                elif action.get('wait'):
                    time.sleep(action['wait'])
                # elif action.get('click'):
                #     driver.click('element')
            except Exception as e:
                logger.error(e)

if __name__ == '__main__':
    main()