## 🐳 Configurações Docker

> **Nota Importante:**  
> O Portainer **não é necessário** para o funcionamento do código.

### **Portainer (Opcional)**

```bash
docker volume create portainer_data2
docker run -d -p 8000:8000 -p 9443:9443 --name portainer2 --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data2:/data \
  portainer/portainer-ce:2.21.4
```

### **Subir Docker-Compose**

```bash
docker compose -f docker-compose.yaml up -d
```

## 🌐 Conexões

|        Application        |URL                          |Credentials                         |
|----------------|-------------------------------|-----------------------------|
|Airflow| [http://localhost:8085](http://localhost:8085) | ``` User: airflow``` <br> ``` Pass: airflow``` |         |
|MinIO| [http://localhost:9001](http://localhost:9001) | ``` User: airflow``` <br> ``` Pass: airflowairflow``` |           |
|Postgres| **Server/Database:** localhost:5432/airflow | ``` User: airflow``` <br> ``` Pass: airflow``` |           |
|Spark (Master) | [http://localhost:8081](http://localhost:8081)|  |         |
