# minidlna_exporter.py

A prometheus exporter for minidlna written in Python 3.
The exporter scrapes minidlna's status site and exposes it as prometheus metrics.

![Grafana Dashboard](grafana.png)
See [grafana_dashboard.json](grafana_dashboard.json)


## Content
- [minidlna_exporter.py](#minidlnaexporterpy)
	- [Metrics](#metrics)
	- [Setup](#setup)
		- [pip](#pip)
		- [manual](#manual)
		- [Docker](#docker)
			- [docker-hub](#docker-hub)
			- [manual](#manual)
	- [Usage](#usage)
		- [Usage Example](#usage-example)



## Metrics

    # HELP python_info Python platform information
    # TYPE python_info gauge
    python_info{implementation="CPython",major="3",minor="7",patchlevel="0",version="3.7.0"} 1.0
    # HELP minidlna_files file metrcis
    # TYPE minidlna_files gauge
    minidlna_files{type="audio_files"} 3624.0
    minidlna_files{type="video_files"} 1865.0
    minidlna_files{type="image_files"} 60241.0
    # HELP minidlna_clients client metrics
    # TYPE minidlna_clients gauge
    minidlna_clients{hw_address="00:71:47:40:36:c5",ip_address="192.168.0.186",type="generic upnp 1.0"} 1.0
    minidlna_clients{hw_address="74:75:48:57:3f:21",ip_address="192.168.0.107",type="generic upnp 1.0"} 1.0
    minidlna_clients{hw_address="ff:ff:ff:ff:ff:ff",ip_address="127.0.0.1",type="unknown"} 1.0

## Setup

### pip
    pip3 install --upgrade git+https://github.com/dr1s/minidlna_exporter.py.git

### manual
    git clone https://github.com/dr1s/minidlna_exporter.py.git
    cd minidlna_exporter.py
    pip3 install -r requirements.txt
    cd minidlna_exporter
    ./minidlna_exporter.py

### Docker

#### docker-hub
    docker pull dr1s/minidlna_exporter:latest
    docker run --net=host -t dr1s/minidlna_exporter

#### manual
    git clone https://github.com/dr1s/minidlna_exporter.py.git
    docker build -t dr1s/minidlna_exporter .
    docker run -d --net=host -t dr1s/minidlna_exporter

## Usage
    usage: minidlna_exporter.py [-h] [-m MINIDLNA] [-p PORT] [-i INTERFACE]

    minidlna_exporter

    optional arguments:
      -h, --help            show this help message and exit
      -m MINIDLNA, --minidlna MINIDLNA
                            minidlna adress
      -p PORT, --port PORT  port minidlna_exporter is listening on
      -i INTERFACE, --interface INTERFACE
                            interface minidlna_exporter will listen on

### Usage Example

    minidlna_exporter --minidlna localhost:8200 --interface 0.0.0.0 --port 9312

The previous used arguements are the default options. If nothing needs to be changed, minidlna_exporter can be started without arguments.
