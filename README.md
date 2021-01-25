# Ejercicio MIGTRA

### Ejercicio N1

Ejercicio desarrollado en Python y con logica de microservicios

Para levantamiento local dirigirse al directorio 

```sh
cd migtra/json_statistics/microservices/ms-bff-json-statistics/src/
```
Luego ejecutar el siguiente comando (es necesario tener Docker instalado)

```sh
docker-compose up --build
```

Luego utilice un cliente API REST (Postman como recomendado) y obtendra los resultados solicitados en el ejercicio en las siguientes rutas cargando JSON base de 3 niveles

- Extraer el promedio de la variable var1 
```sh
localhost:5000/average_var1
```
- Extraer la suma de la variable var2 para la provincia 2
```sh
localhost:5000/sum_var2_prov2
```
- Extraer el máximo de la variable var1 de la región 4
```sh
localhost:5000/max_var1_reg4
```

### Ejercicio N2

Para levantamiento local dirigirse al directorio 

```sh
cd migtra/json_statistics/microservices/ms-bff-work-statistics/src
```
Luego ejecutar el siguiente comando (es necesario tener Docker instalado)

```sh
docker-compose up --build
```

Luego utilice un cliente API REST (Postman como recomendado) y obtendra los resultados solicitados en el ejercicio en las siguientes rutas cargando JSON con registros de faena

- El promedio de tiempo de espera en zonas A y B
```sh
localhost:5000/avg_wait_time
```

- El porcentaje de ciclos de faena que incluyeron alguna área de trabajo tipo 2
```sh
localhost:5000/aw2_bw2
```
- Analisis propuesto: Se busca la zona de trabajo particular con mayor demanda (AW1, AW2, BW1, BW2) y a su vez se entrega la estadistica global de la zona con mayor demanda (AW, BW)
```sh
localhost:5000/aw1_aw2_vs_bw1_bw2
```

### NOTA

En caso de necesitar definicion de variables de ambiente utilizar archivo env.example y renombrarlo a .env

- ms-bff-json-statistics

```sh
cd migtra/json_statistics/microservices/ms-bff-json-statistics/src
mv .env.example .env
```

- ms-bff-work-statistics

```sh
cd migtra/json_statistics/microservices/ms-bff-work-statistics/src
mv .env.example .env
```

