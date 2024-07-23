import altair as alt
import joblib
import pandas as pd
import streamlit as st

#  Load ML model
model = joblib.load('./MLPClassifier_model.pkl')

#  (Streamlit): Hide result holder when page first loaded.
if 'message' not in st.session_state:
    st.session_state['message'] = ''

#  Load the dataframe that was used to train the model.
data = pd.read_csv('./datasets/data_final.csv')

#  Variables for Streamlit chart.
filtered_df = data.copy()

#  Change review score to verbose review to make it easy to understand on chart.
review_score = {10: '4 - Very Positive',
                9: '4 - Very Positive',
                8: '3 - Mostly Positive',
                7: '2 - Mixed',
                6: '1 - Negative',
                5: '1 - Negative'}
data['overall_review'] = data['overall_review'].map(review_score)


#  Function for 'Clear' button, to unselect all.
def clear_selections():
    st.session_state['message'] = ''
    st.session_state['Action'] = False
    st.session_state['Adventure'] = False
    st.session_state['Casual'] = False
    st.session_state['Cross-Platform Multiplayer'] = False
    st.session_state['Free to Play'] = False
    st.session_state['Indie'] = False
    st.session_state['Massively Multiplayer'] = False
    st.session_state['Multiplayer'] = False
    st.session_state['RPG'] = False
    st.session_state['Simulation'] = False
    st.session_state['Single-player'] = False
    st.session_state['Sports'] = False
    st.session_state['Strategy'] = False
    st.session_state['VR Supported'] = False
    st.session_state['linux_support'] = False
    st.session_state['mac_support'] = False
    st.session_state['win_support'] = False


#  Main logic for 'Predict' button:
def pred():
    feat = pd.DataFrame([st.session_state])  # (Streamlit): Turn buttons' states (True/False) into a dataframe
    feat.drop(columns=['FormSubmitter:selection_form-Predict', 'message'], inplace=True)

    #  Match the features' order to the model's
    correct_order = ['win_support', 'mac_support', 'linux_support', 'Single-player', 'Cross-Platform Multiplayer',
                     'VR Supported', 'Indie', 'Action', 'Adventure', 'Casual', 'Simulation',
                     'Strategy', 'RPG', 'Free to Play', 'Sports', 'Massively Multiplayer', 'Multiplayer']
    feat = feat[correct_order]

    # Predict
    prediction = model.predict(feat)

    #  Show result to user based on model's prediction.
    if prediction[0] <= 6:
        result = '''Most of the games on Steam with the selected features and genres have negative reviews!
                  We should be careful with this project!'''
    elif prediction[0] == 7:
        result = 'The reviews on this type of games are mixed.'
    elif prediction[0] == 8:
        result = 'Games with these features are popular and have positive reviews'
    else:
        result = '''These games are huge success and received extremely well on Steam!
                 This can't go wrong!'''
        st.balloons()
    st.session_state['message'] = result

    #  Filter, sort and return a filtered dataframe for chart and additional info.
    items = []
    for ft in feat.columns.tolist():
        if feat[ft].bool():
            items.append(ft)
    df = data[data[items].all(axis=1)]

    return df


#  UI with Streamlit
with st.container():
    col1, col2 = st.columns([0.9, 0.1])
    col1.title('Success Prediction')
    col2.button('Clear', on_click=clear_selections)
with st.form('selection_form'):
    with st.container():
        top_col1, top_col2 = st.columns([0.7, 0.3])
        features = top_col1.container()
        platforms = top_col2.container()
        with features:
            st.subheader('Features:', divider='red')
            ft1, ft2 = st.columns(2)
            ft1.toggle('Single-player', key='Single-player')
            ft1.toggle('Cross-Platform Multiplayer', key='Cross-Platform Multiplayer')
            ft1.toggle('VR Supported', key='VR Supported')

            ft2.toggle('Multiplayer', key='Multiplayer')
            ft2.toggle('Free to Play', key='Free to Play')
            ft2.toggle('Massively Multiplayer', key='Massively Multiplayer')

        with platforms:
            st.subheader('Platforms:', divider='red')
            st.toggle('Linux', key='linux_support')
            st.toggle('MacOS', key='mac_support')
            st.toggle('Windows', key='win_support')

    with st.container():
        st.subheader('Genres:', divider='red')
        gen1, gen2, gen3 = st.columns(3)

        gen1.toggle('Indie', key='Indie')
        gen1.toggle('Action', key='Action')
        gen1.toggle('Adventure', key='Adventure')

        gen2.toggle('Casual', key='Casual')
        gen2.toggle('Simulation', key='Simulation')
        gen2.toggle('Strategy', key='Strategy')

        gen3.toggle('RPG', key='RPG')
        gen3.toggle('Sports', key='Sports')
    if st.form_submit_button('Predict', type='primary'):
        filtered_df = pred()

    with st.container():
        st.text(st.session_state['message'])

    exp = st.expander('Details')

    #  (Streamlit): Bar chart shows number of games with selected features vs reviews
    bars = (
        alt.Chart(filtered_df)
        .mark_bar()
        .encode(
            alt.X('overall_review', title='Overall Review'),
            alt.Y('count()', title='Number of Games'),
        )
    )

    #  Sort and pick top 5 games.
    examples = filtered_df.sort_values(by=['overall_review_count', 'overall_review_%'], ascending=False)
    examples = examples.head(5)

    #  (Streamlit): Display details.
    exp.altair_chart(bars, use_container_width=True)
    exp.write('''
            ''')
    exp.write('Top 5 games with similar features and genres: ')
    exp.write(examples[['title', 'overall_review_count', 'overall_review_%']])
