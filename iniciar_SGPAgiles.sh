#!/bin/bash
if [[ $(lsof -i -P -n | grep "5432 (LISTEN)" | wc -l) -eq 1 ]]; then
    echo "Apagando POSTGRES LOCAL"
    systemctl stop postgresql
fi
echo "Elija cómo se va a iniciar el proyecto:"
echo "1 - Como lo dejé."
echo "2 - Desde cero."
echo "3 - Desde cero pero con datos pre-cargados."
read -p 'Input: ' eleccion

if [[ $eleccion -eq 1 ]]; then
  docker compose up --build
elif [[ $eleccion -eq 2 ]]; then
  docker compose down -v
  docker compose up --build
elif [[ $eleccion -eq 3 ]]; then
  docker compose down -v
  docker compose -f docker-compose-test.yml up --build
else
  echo "no valido"
fi
