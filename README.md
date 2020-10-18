# uptimerobot_exporter
uptimerobot_exporter is a [Prometheus](https://prometheus.io/) exporter for [UptimeRobot](https://uptimerobot.com/).

## TO DO
1. [ ] Add setup to readme
2. [ ] Add more metrics
3. [x] General refactor
4. [ ] Test, test, testttttt
5. [ ] Code coverage

## Grafana Dashboard
You can find the Grafana dashboard to visualize the metrics exposed by this exporter [here](https://to-be-defined/) and it looks like this:

![Dashboard](https://github.com/paolobasso99/uptimerobot_exporter/blob/main/dashboard.png?raw=true)

## Why 
I needed a Prometheus exporter for UptimeRobot and the existing ones that I found are either old, not updated, poorly documented or they expose not enough metrics. It was also an opportunity to learn more about Prometheus.

## Technologies
1. [Prometheus](https://prometheus.io/)
2. [UptimeRobot](https://uptimerobot.com/)
3. [Grafana](https://grafana.com/)
4. [Python](https://www.python.org/)
5. [Docker](https://www.docker.com/)
6. [GitHub Actions](https://github.com/features/actions)

## Things I learnt
1. Using UptimeRobot to monitor websites uptime
2. Creating a basic Prometheus Exporter with Python
3. Creating a Grafana Dashboard from scratch
4. Dockerizing a simple Python application
5. Auto publishing Docker images to Docker Hub with GitHub actions
6. Tesing a simple python application
7. Self Hosting Prometheus
8. Self Hosting Grafana

## License
GNU AFFERO GENERAL PUBLIC LICENSE Version 3