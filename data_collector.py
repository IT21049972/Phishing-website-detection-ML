# data collection
import requests as re
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

from bs4 import BeautifulSoup
import pandas as pd
import feature_extraction as fe

disable_warnings(InsecureRequestWarning)

URL_filename = "top-1m.csv"
data_frame = pd.read_csv(URL_filename)

URL_list = data_frame['url'].to_list()

# restrict request urls

begin = 0
end = 100

collection_list = URL_list[begin:end]


# tag = "http://"

# collection_list = [tag + url for url in collection_list]

def create_structured_data(url_list):
    data_list = []
    for i in range(0, len(url_list)):
        try:
            url = "http://" + url_list[i]
            response = re.get(url, verify=False,
                              timeout=4)  # to avoid urls with no certs and taking time to load
            if response.status_code != 200:
                print(i, "Http con was unsuccesful for url: ", url)
            else:
                soup = BeautifulSoup(response.content, "html.parser")
                vector = fe.create_vector(soup)
                vector.append(str(url))
                data_list.append(vector)
        except re.exceptions.RequestException as e:
            print(i, "--->", e)
            continue
    return data_list


data = create_structured_data(collection_list)

columns = [
    'has_title',
    'has_input',
    'has_button',
    'has_image',
    'has_submit',
    'has_link',
    'has_password',
    'has_email_input',
    'has_hidden_element',
    'has_audio',
    'has_video',
    'number_of_inputs',
    'number_of_buttons',
    'number_of_images',
    'number_of_option',
    'number_of_list',
    'number_of_th',
    'number_of_tr',
    'number_of_href',
    'number_of_paragraph',
    'number_of_script',
    'length_of_title',
    'has_h1',
    'has_h2',
    'has_h3',
    'length_of_text',
    'number_of_clickable_button',
    'number_of_a',
    'number_of_img',
    'number_of_div',
    'number_of_figure',
    'has_footer',
    'has_form',
    'has_text_area',
    'has_iframe',
    'has_text_input',
    'number_of_meta',
    'has_nav',
    'has_object',
    'has_picture',
    'number_of_sources',
    'number_of_span',
    'number_of_table',
    'URL'
]

df = pd.DataFrame(data=data, columns=columns)

df['label'] = 0

df.to_csv("test.csv", mode='a', index=False)
