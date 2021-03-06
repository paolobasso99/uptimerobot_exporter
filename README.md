# uptimerobot_exporter
[![Maintainability](https://api.codeclimate.com/v1/badges/0af5fa985013098bc87a/maintainability)](https://codeclimate.com/github/paolobasso99/uptimerobot_exporter/maintainability)
[![codecov](https://codecov.io/gh/paolobasso99/uptimerobot_exporter/branch/main/graph/badge.svg?token=T064WJMK3F)](https://codecov.io/gh/paolobasso99/uptimerobot_exporter/)
[![CodeFactor](https://www.codefactor.io/repository/github/paolobasso99/uptimerobot_exporter/badge)](https://www.codefactor.io/repository/github/paolobasso99/uptimerobot_exporter)
[![Known Vulnerabilities](https://snyk.io/test/github/paolobasso99/uptimerobot_exporter/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/paolobasso99/uptimerobot_exporter?targetFile=requirements.txt)

uptimerobot_exporter is a [Prometheus](https://prometheus.io/) exporter for [Uptimerobot](https://uptimerobot.com/).

## Setup
### Exporter
The easier way to setup this exporter is to use the [Docker image on Docker Hub](https://hub.docker.com/r/paolobasso/uptimerobot_exporter).
Using a `docker-compose.yaml`:

    version: "3"

    services:
    uptimerobot_exporter:
        image: paolobasso/uptimerobot_exporter
        container_name: uptimerobot_exporter
        environment:
        - UPTIMEROBOT_READ_API_KEY=your-api-key
        - INTERVAL_SECONDS=300
        - LOG_LEVEL=INFO
        - PORT=8000
        ports:
        - 8000:8000
        restart: unless-stopped

If Prometheus is in the same server an internal Docker network without exposing the metrics to the internet would be preferred.

### Envirorment variables

| Variable                 | Required | Default | Description                                                                                                                       |
| ------------------------ | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| UPTIMEROBOT_READ_API_KEY | YES      |         | Your Uptimerobot read API key. Found on the Uptimerobot's  My Settings page -> API Settings.                                      |
| INTERVAL_SECONDS         | NO       | 300     | How many seconds to wait between a scrape end and the next scrape.<br>You should use the Uptimerobot monitor's shortest interval. |
| LOG_LEVEL                | NO       | INFO    | The log level.                                                                                                                    |
| PORT                     | NO       | 8000    | The port where metrics will be exposed                                                                                            |

### Prometheus
Add a job to your Prometheus configs:

    - job_name: 'uptimerobot'
       scrape_interval: 5m
       scrape_timeout: 300s # Same as INTERVAL_SECONDS env vars
       static_configs:
         - targets: 
            - 'localhost:8000' # Use the PORT env var (Default is 8000)

## Metrics exposed
| Metric                                                 | Type  | Labels                                 | Description                                                                          |
| ------------------------------------------------------ | ----- | -------------------------------------- | ------------------------------------------------------------------------------------ |
| uptimerobot_up                                         | Gauge |                                        | The last scrape was successful                                                       |
| uptimerobot_scrape_duration_milliseconds               | Gauge |                                        | The duration of the last scrape in seconds                                           |
| uptimerobot_monitor_status                             | Gauge | id, url, name, type            | Status of the monitor: 0 = paused, 1 = not checked, 2 = up, 8 = seems down, 9 = down |
| uptimerobot_monitor_response_time_millisecond          | Gauge | id, url, name, type, status  | Last response time of the monitor in milliseconds                                    |
| uptimerobot_monitor_response_time_average_milliseconds | Gauge | id, url, name, type            | Average response time of the monitor in milliseconds                                 |
| uptimerobot_monitor_log_type                           | Gauge | id, url, name, type            | Last log type of the monitor: 1 = down, 2 = up, 98 = started, 99 = paused            |
| uptimerobot_monitor_log_datetime                       | Gauge | id, url, name, type, logtype | Last log of the monitor datetime                                                     |


## Grafana Dashboard
You can find the Grafana dashboard to visualize the metrics exposed by this exporter [here]([https://to-be-defined/](https://github.com/paolobasso99/uptimerobot_exporter/blob/main/dashboard/dashboard.json?raw=true)) and it looks like this:

![Dashboard](https://github.com/paolobasso99/uptimerobot_exporter/blob/main/dashboard/dashboard.png?raw=true)

## Why 
I needed a Prometheus exporter for Uptimerobot and the existing ones that I found are either old, not updated, poorly documented or they expose not enough metrics. It was also an opportunity to learn more about Prometheus and Python.

## Technologies
1. [Prometheus](https://prometheus.io/)
2. [Uptimerobot](https://uptimerobot.com/)
3. [Grafana](https://grafana.com/)
4. [Python](https://www.python.org/)
5. [Docker](https://www.docker.com/)
6. [GitHub Actions](https://github.com/features/actions)

## Things I learnt
1. Using Uptimerobot to monitor websites uptime
2. Creating a basic Prometheus Exporter with Python
3. Creating a Grafana Dashboard from scratch
4. Dockerizing a simple Python application
5. Auto publishing Docker images to Docker Hub with GitHub actions
6. Tesing a simple python application
7. Self Hosting Prometheus
8. Self Hosting Grafana
9. Python Docstrings

## License
GNU AFFERO GENERAL PUBLIC LICENSE Version 3