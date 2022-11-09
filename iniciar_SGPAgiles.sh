#!/bin/bash
if [[ $(lsof -i -P -n | grep "5432 (LISTEN)" | wc -l) -eq 1 ]]; then
    echo "Apagando POSTGRES LOCAL"
    systemctl stop postgresql
fi

if [[ $(lsof -i -P -n | grep "5432 (LISTEN)" | wc -l) -eq 1 ]]; then
    echo "Apagando proceso usando el puerto 80"
    fuser -k 80/tcp
fi

echo "#######################################"
echo "###########   SGPAgiles    ############"
echo "#######################################"
echo "Elija la iteracion:"
echo "1- v0.0.1"
echo "2- v0.0.2"
echo "3- v0.0.3"
echo "4- v0.0.4"
echo "5- v0.0.5"
echo "6- v0.0.6"
read -p 'Input: ' iteracion

if [[ $iteracion -eq 1 ]]; then
  git checkout v0.0.1
elif [[ $iteracion -eq 2 ]]; then
  docker compose down -v
  docker compose up --build
elif [[ $iteracion -eq 3 ]]; then
  docker compose down -v
  docker compose -f docker-compose-test.yml up --build
elif [[ $iteracion -eq 4 ]]; then
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
else
  echo "no valido"
fi
