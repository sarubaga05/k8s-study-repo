## Описание задания

С помощью ИИ сгенерировал приложение для последующего разворачивания в Kubernetes.  

Было сгенерировано простое приложение: «Система голосования» (Voting App), где backend пишет в базу, frontend читает из нее.  

## Приложение

### Архитектура:

* Frontend: Nginx + простой HTML/JS (отображает голоса)
* Backend: Python (Flask) + Redis (временное хранилище) + PostgreSQL (основное хранилище)
* База данных: PostgreSQL (в кластере, StatefulSet)

Функционал:
* `/vote` — отдать голос за кота или собаку
* `/results` — посмотреть текущую статистику

## Итоговое задание (5 блоков + бонус)
### Блок 1. Подготовка приложения и контейнеров
* Написать Dockerfile для backend (Python/Flask) с использованием переменных окружения для подключения к БД.
* Написать Dockerfile для frontend (Nginx, статика).
* Собрать образы и загрузить их в локальный реестр minikube (minikube image build ...).

### Блок 2. Развертывание базы данных (StatefulSet + PersistentVolume)
* Создать манифесты:
    - StorageClass (standard в minikube)
    - PersistentVolumeClaim для PostgreSQL
    - ConfigMap (инициализационный SQL)
    - Secret (пароль БД)
    - Service (ClusterIP, headless для StatefulSet)
    - StatefulSet PostgreSQL с readinessProbe/livenessProbe

### Блок 3. Backend и Frontend (Deployment + Service + ConfigMap/Secret)
* ConfigMap для переменных окружения backend (адреса сервисов)
* Secret для подключения к PostgreSQL
* Deployment backend с resource requests/limits, probes, SecurityContext (runAsNonRoot)
* ClusterIP Service для backend
* Deployment frontend
* NodePort Service для frontend (или сразу Ingress)

### Блок 4. Сеть, Ingress, автомасштабирование
* Ingress (в minikube надо включить аддон: `minikube addons enable ingress`) для доступа к frontend и API backend по разным хостам/paths
* NetworkPolicy — разрешить доступ к backend только из frontend и к БД только из backend
* HorizontalPodAutoscaler для backend на основе CPU (загрузить его тестовым запросами)

### Блок 5. Мониторинг и управление
* Установить Metrics Server (`minikube addons enable metrics-server`)
* Настроить Prometheus + Grafana (можно через Helm: prometheus-community/kube-prometheus-stack)
* Добавить в backend метрики (например, /metrics в Prometheus формате) и настроить ServiceMonitor
* CronJob, который раз в час чистит старые записи голосований (оставляя последние 1000)

### Бонус (по желанию)
* RBAC: создать ServiceAccount для backend, ограничить его права только на чтение своих Pod’ов
* VerticalPodAutoscaler: установить VPA (`minikube addons enable vertical-pod-autoscaler`) и настроить его для backend в режиме "рекомендации"
* Helm-чарт: завернуть всё приложение в Helm-чарт с возможностью переключения между PostgreSQL в кластере и внешней БД

## Критерии успеха (что должно работать)
* После применения всех манифестов (kubectl apply -f ...) все Pod’ы переходят в Running.
* Через браузер по IP minikube + NodePort (или через Ingress-host) открывается frontend, можно голосовать.
* При перезапуске backend (или БД) данные не теряются (PVC работает).
* kubectl top pod показывает CPU/memory.
* При нагрузке (например, `kubectl run -it --rm load-generator --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://backend-service:5000/vote; done"`) HPA создает новые Pod’ы backend.
* NetworkPolicy блокирует доступ к БД из frontend (проверь через kubectl exec).

## Примерная структура решения

```
vote-app/
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile
│   └── index.html
├── k8s/
│   ├── namespace.yaml
│   ├── storage-class.yaml
│   ├── pvc-postgres.yaml
│   ├── statefulset-postgres.yaml
│   ├── configmap-backend.yaml
│   ├── secret-db.yaml
│   ├── deployment-backend.yaml
│   ├── hpa-backend.yaml
│   ├── networkpolicy.yaml
│   └── ingress.yaml
└── helm/
    └── vote-chart/
```

## Промтп для генерации задания (использовал ИИ DeepSeek)  

Прошел курс по Kubernetes. Хочу проверить и закрепить знания. Сгенерируй мне итоговое задание с такими вводными:  
1. Сгенерируй простенькое приложение (frontend + backend + база данных, например PostgreSQL). Слышал, что базу не обязательно пихать в кластер, это на твое усмотрение
2. Список тем, которые я прошел:
    * Pod, ReplicaSet, Deployment, Service
    * ConfigMap, Secret, Environment variables и volume mounts
    * Volumes, PersistentVolume и PersistentVolumeClaim, StorageClass и StatefulSet
    * Сеть в k8s: Service discovery и DNS, Ingress и NetworkPolicy
    * Resources, HorizontalPodAutoscaler, VerticalPodAutoscaler и Cluster Autoscaler
    * Labels и Annotations, Probes, Jobs и CronJobs
    * Мониторинг: Metrics Server и kubectl top, Введение в Prometheus и Grafana
    * RBAC, ServiceAccount, SecurityContext
    * Helm
3. Проходил курс на домашнем компьтере в minikube

Доп примечание:
- Если хочешь добавить что-то еще в приложение, я не против
- Можешь затронуть темы, неуказанные в списке, я разберусь
- Если хочешь предложить что-то другое помимо minikube, я готов это рассмотреть
