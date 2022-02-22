# learn-fastapi-prometheus-grafana
Repositório ensinando como implementar um coletor de métricas Prometheus em um sistema com FastAPI.

# Requisitos
* [Python 3.6+](https://www.python.org/downloads/)
* [Docker Compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-pt)
* [Python venv](https://docs.python.org/3/library/venv.html)

# Estrutura do repositório
* `backend/main.py`: Arquivo python com backend em FastAPI configurado para enviar métricas para o Prometheus.
* `prometheus/prometheus.yml`: Arquivo de configuração do Prometheus utilizado pelo `docker-compose.yaml` na hora de subir o prometheus.
* `docker-compose.yaml`: Arquivo para subir as imagens do Prometheus e Grafana na máquina local.
* `requirements.txt`: Requisitos Python para o backend funcionar.

# Setup
## Prometheus + Grafana
### 1. Criando volume persistente para o grafana
Primeiro vamos criar um volume no docker para o grafana armazenar seus dados fora do container.
>docker volume create grafana-storage

### 2. Chamando o docker-compose.yaml
Execute:
>docker-compose up -d

Para levantar o Prometheus e o Grafana.

Se você receber um erro de $PWD, troque a linha :

`- /$PWD/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml` para o seu diretório onde está esses arquivos, como o exemplo abaixo:

 `- /home/lucas-sossai/dev-pessoal/learn-fastapi-prometheus-grafana/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml`

### 3. Verificando se o Prometheus e Grafana estão de pé
Execute:
> docker-compose ps
E verifique se o output é:
```
                    Name                                   Command               State   Ports
----------------------------------------------------------------------------------------------
learn-fastapi-prometheus-grafana_grafana_1      /run.sh                          Up           
learn-fastapi-prometheus-grafana_prometheus_1   /bin/prometheus --config.f ...   Up   
```
#### 3.1: Prometheus
Acesse http://127.0.0.1:9090 para ver se a UI do Prometheus está funcionando.

#### 3.2: Grafana

Acesse http://127.0.0.1:3000 para ver se a UI do Grafana está funcionando.

Dados padrão de acesso:
* Usuário: `admin`
* Senha: `admin`
### 4. Configurando o Prometheus como Data Source no Grafana
Após realizar login no Grafana, vá para:

Configuration -> Data Sources -> Add Data Sources

Selecione Prometheus, mude a url para http://localhost:9090

Clique em `Save & Test` para validar se o novo Data Source está funcionando.

### 5. Verifique se o Grafana está recebendo dados do Prometheus.

* Clique na opção `Explore`
* Coloque a métrica `process_cpu_seconds_total` e execute a query
* Verifique se foi gerado um gráfico com dados de uso da CPU

## FastAPI
### 1. Criando o ambiente e instalando os requisitos
Primeiro vamos criar um ambiente virtual:

> python3 -m venv. env

Para entrar dentro do ambiente:

> source .env/bin/activate

E agora instalando os requisitos:

> pip install -r requirements.txt


### 2. Deploy na FastAPI
Dentro do venv execute o seguinte comando:
> uvicorn backend.main:app --reload

Acesse http://127.0.0.1:8000 e verifique se recebe o seguinte output:

`{"Hello":"World"}`
# Inserindo métricas do Prometheus via FastAPI:
Podemos ver todos endpoints criados na docs criadas automaticamente pela FastAPI no seguinte link: http://127.0.0.1:8000/docs

As métricas do Prometheus estão configuradas para serem coletadas no endpoint: http://127.0.0.1:8000/metrics

É possível verificar a quantidade de requests por endpoint no Grafana na sessão `Explore` realizando a query na métrica `starlette_requests_created`.

## Counter

## Gauge

## Summary

## Histogram
