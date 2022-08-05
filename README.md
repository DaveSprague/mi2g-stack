



# Mosquitto, InfluxDB2, Grafana (MI2G) Stack

Gain the ability to analyze and monitor telemetry data by deploying the TIG stack within minutes using [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/).




## ⚡️ Getting Started

Clone the project

```bash
  git clone https://github.com/huntabyte/mi2g-stack.git
```

Navigate to the project directory

```bash
  cd mi2g-stack
```

##BELOW NEEDS TO BE UPDATED

Change the environment variables define in `.env` that are used to setup and deploy the stack
```bash
├── .env         <---
├── docker-compose.yml
├── entrypoint.sh
└── ...
```

Customize the `telegraf.conf` file which will be mounted to the container as a persistent volume

```bash

├── .env
├── docker-compose.yml
├── entrypoint.sh
└── ...
```

Start the services
```bash
docker-compose up -d
```
## Docker Images Used (Official & Verified)



[**InfluxDB**](https://hub.docker.com/_/influxdb) / `2.3.0`

[**Grafana-OSS**](https://hub.docker.com/r/grafana/grafana-oss) / `8.4.3`



## Contributing

Contributions are always welcome!

