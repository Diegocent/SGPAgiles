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
echo "Elija cual iteracion del proyecto usar:"
echo "$(git tag -l)"
echo "origin master"
read -p 'Nombre de la iteracion: ' iteracion

git checkout $iteracion --force

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
  if [[ $estado -eq 1 ]]; then
    docker compose down -v
    docker compose up --build
  elif [[ $estado -eq 2 ]]; then
    docker compose down -v
    docker compose -f docker-compose-test.yml up --build
  elif [[ $estado -eq 3 ]]; then
    docker compose up --build
  fi
elif [[ $iteracion -eq 2 ]]; then
  docker compose down -v
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
elif [[ $iteracion -eq 3 ]]; then
  docker compose down -v
  docker compose -f docker-compose.yml -f docker-compose-test.prod.yml up --build
elif [[ $iteracion -eq 4 ]]; then
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
else
  echo "no valido"
fi
