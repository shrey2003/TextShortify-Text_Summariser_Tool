## Workflows
1. Update config-yaml
2. Update params.yaml
3. Update entity
4. Update the configuration manager in src config
5. update the conponents
6. update the pipeline
7. update the main. py
8. update the app. py

docker build -t docqna.azurecr.io/docqna:latest .

docker login docqna.azurecr.io

docker push docqna.azurecr.io/docqna:latest