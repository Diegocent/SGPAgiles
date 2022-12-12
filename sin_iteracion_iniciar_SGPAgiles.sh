#!/bin/bash

sudo systemctl stop postgresql
sudo systemctl stop apache2


echo "#######################################"
echo "###########   SGPAgiles    ############"
echo "#######################################"

echo "Desea levantar el servidor o correr los tests?"
echo "1- Levantar el servidor."
echo "2- Correr los tests."
read -p 'Input: ' accion
if [[ $accion -eq 1 ]]; then
  echo "Desea levantar el servidor de desarrollo o el de produccion?:"
echo "1- Desarrollo."
echo "2- Produccion."
read -p 'Input: ' iteracion

echo "Cómo desea que sea el estado de la base de datos?:"
echo "1- Desde cero."
echo "2- Desde cero, pero con datos precargados."
echo "3- Como lo deje."
read -p 'Input: ' estado

if [[ $iteracion -eq 1 ]]; then
  echo "INICIANDO SERVIDOR DE DESARROLLO"
  if [[ $estado -eq 1 ]]; then
    echo "DESDE CERO"
    sudo docker compose down -v
    sudo docker compose up --build
  elif [[ $estado -eq 2 ]]; then
    echo "DESDE CERO PERO PRECARGADO"
    sudo docker compose down -v
    sudo docker compose -f docker-compose-test.yml up --build
  elif [[ $estado -eq 3 ]]; then
    echo "COMO ESTABA"
    sudo docker compose up --build
  else
    echo "no valido"
  fi
elif [[ $iteracion -eq 2 ]]; then
  echo "INICIANDO SERVIDOR DE PRODUCCION"
  if [[ $estado -eq 1 ]]; then
    echo "DESDE CERO"
    sudo docker compose down -v
    sudo docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
  elif [[ $estado -eq 2 ]]; then
    echo "DESDE CERO PERO PRECARGADO"
    sudo docker compose down -v
    sudo docker compose -f docker-compose.yml -f docker-compose-test.prod.yml up --build
  elif [[ $estado -eq 3 ]]; then
    echo "COMO ESTABA"
    sudo docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
  else
    echo "no valido"
  fi
else
  echo "no valido"
fi
elif [[ $accion -eq 2 ]]; then
  export POSTGRES_HOST=localhost
  export DJANGO_SETTINGS_MODULE=SGPAgiles.settings
  sudo systemctl start postgresql
  pytest
else
  echo "no valido"
fi

