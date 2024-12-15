@echo on
set DC=docker-compose
set FILE=docker/docker-compose.yaml

if "%1"=="app" (
    %DC% -f %FILE% up -d
) else if "%1"=="drop" (
    %DC% -f %FILE% down
) else (
    echo Unknown target: %1
)
