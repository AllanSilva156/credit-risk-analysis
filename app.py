from pycaret.regression import load_model, predict_model
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np

# Nome do experimento realizado para obtenção do pipeline desejado
EXPERIMENT_NAME = 'dataset completo'

# Carregando o pipeline já salvo
model = load_model(f'./pipelines/{EXPERIMENT_NAME}_pipeline', verbose=False)

def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['prediction_label'][0]
    return predictions

def run():
    image = Image.open('./img/logo.png')

    st.sidebar.image(image)

    add_selectbox = st.sidebar.selectbox(
    'Selecione o tipo de previsão:',
    ('Online', 'Batch'))

    st.sidebar.info('Esta aplicação foi criada para prever a liberação de crédito para clientes de uma instituição financeira')

    st.title("Análise de Risco de Crédito")

    if add_selectbox == 'Online':

        idade = st.number_input('Idade (em anos)', min_value=18, max_value=100, value=30)
        renda = st.number_input('Renda anual (R$)', min_value=0, value=50000)
        tipo_residencia = st.selectbox('Tipo residência', ['Aluguel', 'Própria', 'Hipoteca', 'Outro'])
        tempo_emprego = st.number_input('Tempo no emprego (em anos)', min_value=0, value=2)
        intencao_emprestimo = st.selectbox('Intenção de empréstimo', ['Pessoal', 'Educação', 'Médico', 'Investimento', 'Reforma', 'Pagamento de Dívidas'])
        valor_emprestimo = st.number_input('Valor do empréstimo (R$)', min_value=0, value=10000)
        taxa_juros = st.number_input('Taxa de juros (% a.a.)', min_value=0, value=5)
        historico_nao_pagamentos = st.selectbox('Histórico de não pagamentos', ['Sim', 'Não'])
        tempo_historico_credito = st.number_input('Tempo histórico de crédito (em anos)', min_value=0, value=5)

        input_dict = {'Idade': [idade],
        'Renda anual': [renda],
        'Tempo no emprego': [tempo_emprego],
        'Valor do empréstimo': [valor_emprestimo],
        'Taxa de juros': [(taxa_juros/100)],
        'Tempo histórico de crédito': [tempo_historico_credito],
        'Tipo residência': [tipo_residencia],
        'Intenção de empréstimo': [intencao_emprestimo],
        'Histórico não pagamentos': [historico_nao_pagamentos[0]]}

        input_df = pd.DataFrame(input_dict)

        output = ''

        if st.button('Analisar'):
            output = predict(model=model, input_df=input_df)

            if output == 1:
                st.success('Crédito Aprovado')

            else:
                st.error('Crédito Negado')

    if add_selectbox == 'Batch':

        file_upload = st.file_uploader('Faça o upload do arquivo csv para realizar as previsões', type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model, data=data)
            st.write(predictions)


if __name__ == '__main__':
    run()