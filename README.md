# Introdução

Este projeto trata da implantação de um modelo preditivo de análise de risco de crédito baseado em uma versão adpatada do [Credit Risk Dataset](https://www.kaggle.com/datasets/laotse/credit-risk-dataset), utilizando princípios e técnicas de **Machine Learning Operations (MLOps)**.

# Objetivos
* Analisar e documentar os dados disponíveis para a construção do modelo.
* Propor uma nova arquitetura de MLOps baseada na arquitetura Delta da [Databricks](https://www.databricks.com/blog/2020/11/20/delta-vs-lambda-why-simplicity-trumps-complexity-for-data-pipelines.html).
* Implementar a arquitetura proposta em uma plataforma de nuvem.
* Construir uma aplicação com interface de usuário integrada à infraestrutura implementada.

# Arquitetura da aplicação

A **StructML** é uma arquitetura de MLOps inspirada na arquitetura Delta, projetada para simplificar a implementação de modelos de Machine Learning em ambientes de produção. Ideal para cientistas de dados e engenheiros com experiência limitada em MLOps, a StructML organiza os dados em três camadas - Bronze, Silver e Gold - otimizando o gerenciamento de dados desde a coleta até a análise. Com a integração de ferramentas como Vertex AI para desenvolvimento, PyCaret para automação e MLflow para rastreamento, a arquitetura facilita a aplicação prática de modelos de ML.

<img src="../img/structml-gcp.png" width="800" height="450"/>

Além disso, a StructML aproveita o Cloud Run para operações escaláveis e o Cloud Build para processos de integração e entrega contínuas. A arquitetura também incorpora o Streamlit para criar interfaces de usuário intuitivas, tornando-a versátil para várias aplicações de ML. Inspirada na robustez da arquitetura Delta, a StructML se destaca por sua capacidade de transformar projetos de pesquisa em soluções de ML eficazes e prontas para o mercado.

# Sobre os dados

A base **Credit Risk Dataset** é um conjunto de dados abertos disponíveis no Kaggle e que contém registros que simulam dados existentes em uma agência de crédito. A problemática central relacionada a esta base é saber quais perfis de clientes devem receber o empréstimo solicitado e quais não devem. Além da classificação, é essencial o entendimento sobre quais fatores mais contribuíram para a aprovação ou negação do crédito.

**OBS:** Os dados são simulados e não possuem nenhum tipo de informação sensível que possa comprometer qualquer pessoa.

Um breve resumo dos atributos existentes no conjunto de dados pode ser visto na tabela abaixo.

| Nome do atributo      | Descrição               |
|-----------------------|-------------------------|
| Idade                 | Idade do solicitante    |
| Renda anual           | Renda anual do solicitante (reais) |
| Tipo residência | Tipo da residência do solicitante (ALUGUEL, PRÓPRIA, HIPOTECA, OUTRO)            |
| Tempo no emprego     | Tempo que o solicitante está no emprego atual (anos) |
| Intenção de empréstimo          | A intenção do solicitante com relação ao empréstimo (PESSOAL, EDUCAÇÃO, MÉDICO, INVESTIMENTO, REFORMA, PAGAMENTO DE DIVIDAS)  |
| Valor do empréstimo             | Valor do empréstimo solicitado (reais)     |
| Taxa de juros        | Taxa de juros para o empréstimo (percentual)          |
| Status do empréstimo           | Negado (0) ou Aprovado (1)    |
| Histórico não pagamentos | Se existe histórico de não pagamentos do solicitantes (S ou N)   |
| Tempo histórico de crédito (anos) | Quanto tempo o solicitante possui de histórico de crédito |

# Deploy da aplicação

A aplicação pode ser acessada através deste [link](https://credit-risk-analysis-libg37lupq-uc.a.run.app) (caso ainda esteja no ar). Para realizar a implantação por conta própria, a seguir está um passo a passo sobre como você pode realizar o deploy desta aplicação utilizando os serviços da **Google Cloud Platform**.

## Pré-requisitos
* [CLI gcloud](https://cloud.google.com/sdk/docs/install?hl=pt-br)
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Docker](https://docs.docker.com/engine/install/)

Além desses pré-requisitos, também é necessária a criação de um projeto próprio em uma conta com créditos na GCP. Para isso, siga o [tutorial](https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=pt-br).

## Instruções

No prompt de comando, execute as instruções abaixo.

1- Configurar a CLI do `gcloud`.

```bash
gcloud auth login
gcloud config set project seu-id-de-projeto
```

2- Ativar as APIs necessárias

```bash
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

3- Configurar a autenticação do **Docker** com a GCP.

```bash
gcloud auth configure-docker
```

4- Criar um repositório no **Artifact Registry**.

```bash
gcloud artifacts repositories create seu-repositorio \
    --repository-format=docker \
    --location=local-desejado \
    --description="sua-descricao" \
    --immutable-tags \
    --async
```

Caso tenha dúvidas sobre a criação do repositório no Artifact Registry, consulte este [guia](https://cloud.google.com/artifact-registry/docs/repositories/create-repos?hl=pt-br#gcloud).

5- Clonar o repositório da aplicação.

```bash
git clone https://github.com/AllanSilva156/credit-risk-analysis.git
```

6- Acessar a pasta da aplicação.

```bash
cd credit-risk-analysis/
```

7- Construir a imagem especificada no `Dockerfile`.

```bash
docker build --no-cache -t gcr.io/seu-id-de-projeto/nome-da-imagem:tag .
```

8- Realizar a marcação da imagem local para o repositório no Artifact Registry.

```bash
docker tag gcr.io/seu-id-de-projeto/nome-da-imagem:tag location-docker.pkg.dev/seu-id-de-projeto/seu-repositorio/imagem:tag
```

**OBS:** Lembre-se de substituir `location` pelo `local-desejado` que foi definido na criação do repositório.

9- Enviar a imagem marcada para o repositório no Artifact Registry. 

```bash
docker push location-docker.pkg.dev/seu-id-de-projeto/seu-repositorio/imagem:tag
```

10- Implantar o serviço no **Cloud Run**.

```bash
gcloud run deploy nome-do-servico --image location-docker.pkg.dev/seu-id-de-projeto/seu-repositorio/imagem:tag --platform managed --region regiao-desejada --allow-unauthenticated
```

Caso tenha dúvidas sobre a implantação de serviços no Cloud Run, consulte este [guia](https://cloud.google.com/run/docs/deploying?hl=pt-br#command-line).

11- Configurar pipeline de CI/CD com o **Cloud Build**.

Se quiser atualizar a aplicação de acordo com as modificações feitas no repositório do GitHub, basta seguir este [guia](https://cloud.google.com/run/docs/continuous-deployment-with-cloud-build?hl=pt-br#existing-service).

# Integração com MLflow

Para implantar um serviço de rastreamento de experimentos e registro de modelos utilizando a GCP, este [tutorial](https://dlabs.ai/blog/a-step-by-step-guide-to-setting-up-mlflow-on-the-google-cloud-platform/) fornece orientações detalhadas sobre como realizar.

# Referências

https://pycaret.gitbook.io/docs/

https://towardsdatascience.com/easy-mlops-with-pycaret-mlflow-7fbcbf1e38c6

https://towardsdatascience.com/deploy-machine-learning-app-built-using-streamlit-and-pycaret-on-google-kubernetes-engine-fd7e393d99cb

https://www.restack.io/docs/mlflow-knowledge-mlflow-pycaret-integration

https://github.com/pycaret/pycaret-streamlit-google

https://www.restack.io/docs/mlflow-knowledge-mlflow-on-gcp-integration

https://moez-62905.medium.com/simplify-mlops-with-pycaret-mlflow-and-dagshub-366c768f0dac

https://dlabs.ai/blog/a-step-by-step-guide-to-setting-up-mlflow-on-the-google-cloud-platform/