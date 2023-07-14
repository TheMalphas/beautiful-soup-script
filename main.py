import pandas as pd
import logging
import json
from bs4 import BeautifulSoup
import re

logging.basicConfig(filename='html_parse.log', level=logging.INFO)

def extract_data(html_path, class_dict):
    try:
        with open(html_path, 'r', encoding='utf8') as file:
            data = file.read()
    except Exception as e:
        logging.error(f'Error occurred while reading the file: {e}')
        return None

    try:
        soup = BeautifulSoup(data, 'html.parser')
    except Exception as e:
        logging.error(f'Error occurred while parsing the HTML: {e}')
        return None
    results_list = []
    results = {}

    for class_key in class_dict:
        class_name = class_dict[class_key]
        try:
            elements = soup.find_all(class_=class_name)
            for element in elements:
                result_dict = {}
                result_dict[class_key] = (str(element.text).strip().replace("\n",""))
                results_list.append(result_dict)
        except Exception as e:
            logging.error(f'Error occurred while searching for class {class_name}: {e}')

    regex_results = extract_data_regex(results_list)

    with open('findings.txt', 'w') as file:
        for res in regex_results:
            file.write(f'{res}\n')

    return results

def extract_data_regex(data):
    try:
        regex_results = []
        for key, value in data:
            new_dict = {}
            new_dict['Anno'] = None
            new_dict['Tipologia'] = None
            if key == 'info':
                corso = key[value].split("Anno")
                new_dict['Corso'] = corso[0].strip()


    except Exception as e:
        logging.error(f'Error occurred while regexing data: {e}')

def write_to_excel(data, excel_path):
    try:
        df = pd.DataFrame(data)
        df.to_excel(excel_path, index=False)
    except Exception as e:
        logging.error(f'Error occurred while writing data to Excel: {e}')

def read_classes_from_json(json_path):
    try:
        with open(json_path, 'r') as file:
            class_dict = json.load(file)
        return class_dict
    except Exception as e:
        logging.error(f'Error occurred while reading classes from JSON: {e}')
        return None

if __name__ == '__main__':
    html_path = 'index.html' # replace with your file path
    excel_path = 'output.xlsx' # replace with your desired output path
    json_path = 'classes.json' # replace with your json file path

    class_dict = read_classes_from_json(json_path)
    if class_dict is not None:
        # print(f'Loaded classes: {class_dict}')
        data = extract_data(html_path, class_dict)
        if data is not None:
            # print(f'Extracted data: {data}')
            data_df = pd.DataFrame.from_dict(data, orient='index').transpose()  # converting dict to DataFrame
            write_to_excel(data_df, excel_path)
            print(f'Data successfully written to {excel_path}')
        else:
            print('Data extraction failed. Check the log for more details.')
    else:
        print('Failed to load classes. Check the log for more details.')
