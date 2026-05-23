## Описание задания

С помощью ИИ сгенерировал приложение для последующего разворачивания в Kubernetes.   

### Промтп для генерации задания (использовал ИИ DeepSeek)  

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
