import streamlit as st
import machine_learning as ml
import feature_extraction as fe
from bs4 import BeautifulSoup
import requests as re
#import matplotlib
#matplotlib.use('Agg')  # Use the 'Agg' backend (replace with an appropriate backend)
import matplotlib.pyplot as plt

st.title('Phishing website detection app')

st.write('This ML-based app has been developed for educational purposes as part of an assignment. '
         'Its primary objective is to detect phishing websites using content data, including HTML attributes. Not URL!'
         'You can see the details of approach, data set, and feature set if you click on _"See The Details"_. ')

with st.expander('Project Details'):
    st.subheader('Approach')
    st.write('For the classification of phishing and legitimate websites, I employed supervised learning methods. '
             'My focus was on content-based analysis, specifically examining the HTML of the websites. '
             'I utilized the scikit-learn library to implement machine learning models for this task.'
             )
    st.write(
        'In the course of this project, I curated my own dataset and engineered features, drawing from existing literature '
        'as well as performing manual analysis. '
        'To collect data, I utilized the requests library, while BeautifulSoup was employed to parse and extract relevant features. ')
    st.write('You can access the source code and datasets on GitHub via the following link:')

    st.subheader('Dataset')
    st.write('The dataset was sourced from "phishtank.org" and "tranco-list.eu."')
    st.write(
        'In total, approximately 100,000 websites were used, although data scraping proved unsuccessful on some websites due to blocking measures.')
    st.write('The majority of the dataset was compiled in May 2023.')



    labels = 'phishing', 'legitimate'
    phishing_rate = int(ml.phishing_df.shape[0] / (ml.phishing_df.shape[0] + ml.legitimate_df.shape[0]) * 100)
    legitimate_rate = 100 - phishing_rate
    sizes = [phishing_rate, legitimate_rate]
    explode = (0.1, 0)
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, shadow=True, startangle=90, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)


    st.write('Features + URL + Label ==> Dataframe')
    st.markdown('label is 1 for phishing, 0 for legitimate')
    number = st.slider("Select row number to display", 0, 100)
    st.dataframe(ml.legitimate_df.head(number))

    @st.cache
    def convert_df(df):
        # Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')


    csv = convert_df(ml.df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='phishing_legitimate_structured_data.csv',
        mime='text/csv',
    )


    st.subheader('Results')
    st.write('I used 7 different ML classifiers of scikit-learn and tested them implementing k-fold cross validation.'
             'Firstly obtained their confusion matrices, then calculated their accuracy, precision and recall scores.'
             'This technique ensure that the model\'s evaluation is robust. '
             'Comparison table is below:')
    st.table(ml.df_results)
    st.write('NB --> Gaussian Naive Bayes')
    st.write('SVM --> Support Vector Machine')
    st.write('DT --> Decision Tree')
    st.write('RF --> Random Forest')
    st.write('AB --> AdaBoost')
    st.write('NN --> Neural Network')
    st.write('KN --> K-Neighbours')



choice = st.selectbox("Please select your machine learning model",
                 [
                     'Gaussian Naive Bayes', 'Support Vector Machine', 'Decision Tree', 'Random Forest',
                     'AdaBoost', 'Neural Network', 'K-Neighbours'
                 ]
                )

model = ml.nb_model

if choice == 'Gaussian Naive Bayes':
    #print(choice)
    model = ml.nb_model
    st.write('GNB model is selected!')
elif choice == 'Support Vector Machine':
    model = ml.svm_model
    st.write('SVM model is selected!')
elif choice == 'Decision Tree':
    model = ml.dt_model
    st.write('DT model is selected!')
elif choice == 'Random Forest':
    model = ml.rf_model
    st.write('RF model is selected!')
elif choice == 'AdaBoost':
    model = ml.ab_model
    st.write('AB model is selected!')
elif choice == 'Neural Network':
    model = ml.nn_model
    st.write('NN model is selected!')
else:
    model = ml.kn_model
    st.write('KN model is selected!')


url = st.text_input('Enter the URL')
# check the url is valid or not
if st.button('Check!'):
    try:
        response = re.get(url, verify=False, timeout=4)
        if response.status_code != 200:
            print(". HTTP connection un successful for the URL: ", url)
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            vector = [fe.create_vector(soup)]  # add [] as its a 2d array
                #print(vector)
            result = model.predict(vector)
            if result[0] == 0:
                st.success("This web page seems a legitimate!")
                st.balloons()
            else:
                st.warning("Attention! This web page is a potential PHISHING!")
                st.snow()

    except re.exceptions.RequestException as e:
        print("--> ", e)