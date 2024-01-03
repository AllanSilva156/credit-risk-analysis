from pycaret.regression import load_model, predict_model
from PIL import Image
import streamlit as st
import pandas as pd
import os

def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['prediction_label'][0]
    return predictions

def run():
    image = Image.open('./img/logo.png')

    st.sidebar.image(image)

    model_files = (arq.rstrip('.pkl') for arq in os.listdir('pipelines') if arq.endswith('.pkl'))

    model_selection = st.sidebar.selectbox(
    'Selecione o modelo que deseja utilizar:',
    model_files)

    model = load_model(f'./pipelines/{model_selection}', verbose=False)

    pred_mode_selection = st.sidebar.selectbox(
    'Selecione o tipo de previsão:',
    ('Online', 'Batch'))

    st.sidebar.info('Esta aplicação foi criada para simular a previsão da liberação de crédito para clientes de uma instituição financeira')

    st.title("Análise de Risco de Crédito")

    if pred_mode_selection == 'Online':

        age = st.number_input('Idade (em anos)', min_value=18, max_value=100, value=30)
        income = st.number_input('Renda anual (R$)', min_value=0.0, value=50000.0)
        home_ownership = st.selectbox('Tipo residência', ['Aluguel', 'Própria', 'Hipoteca', 'Outro'])
        emp_length = st.number_input('Tempo no emprego (em anos)', min_value=0, value=2)
        loan_intent = st.selectbox('Intenção de empréstimo', ['Pessoal', 'Educação', 'Médico', 'Investimento', 'Reforma', 'Pagamento de Dívidas'])
        loan_amnt = st.number_input('Valor do empréstimo (R$)', min_value=0.0, value=10000.0)
        loan_int_rate = st.number_input('Taxa de juros (% a.a.)', min_value=0.0, value=5.0)
        default_on_file = st.selectbox('Histórico de não pagamentos', ['Sim', 'Não'])
        cred_hist_length = st.number_input('Tempo histórico de crédito (em anos)', min_value=0, value=5)

        input_dict = {'Idade': [age],
        'Renda anual': [income],
        'Tempo no emprego': [emp_length],
        'Valor do empréstimo': [loan_amnt],
        'Taxa de juros': [(loan_int_rate/100)],
        'Tempo histórico de crédito': [cred_hist_length],
        'Tipo residência': [home_ownership],
        'Intenção de empréstimo': [loan_intent],
        'Histórico não pagamentos': [default_on_file[0]]}

        input_df = pd.DataFrame(input_dict)

        output = ''

        if st.button('Analisar'):
            output = predict(model=model, input_df=input_df)

            if output == 1:
                st.success('Crédito Aprovado')

            else:
                st.error('Crédito Negado')

    if pred_mode_selection == 'Batch':

        file_upload = st.file_uploader('Faça o upload do arquivo csv para realizar as previsões', type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model, data=data)
            st.write(predictions)


if __name__ == '__main__':
    run()