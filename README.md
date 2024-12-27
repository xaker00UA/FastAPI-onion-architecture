Создайте файл **dev.env** пример такой  
port=5432  
host=localhost  
db_name=mvm  
user=user  
password=password  
debug=True True|Fasle  
mode=DEV # DEV|TEST  
Пропишете в docker/docker-compose.yaml конфиг вашей бд  
Затем выполните:  
```docker-compose -f docker\docker-compose.yaml up db ```    
Затем выполните:    
```alembic upgrade heads```  
После выполните команду:  
```docker-compose -f docker\docker-compose.yaml down && docker-compose -f docker\docker-compose.yaml up```