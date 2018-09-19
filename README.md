# Video-player
------
------
Key | Value
------------ | -------------
Name | Video Player
Acronym | VP
Use case | Self-optimization (SO)
Instantiation | Physical Network Function (PNF)
Type | Service
Scope  | Video Flows
Management Protocol | Advanced Message Queuing Protocol (AMQP) messages

------

# Description

The Video Player is a component working as a Physical Network Function (PNF) which is used in the Self-Optimizing use case [3.4](https://github.com/Selfnet-5G/WP3_SO/blob/master/Doku/D3.4/D3.4_master.pdf) . Its main function is to reproduce scalable H.265 (SHVC) video flows.

------
# Interfaces
There is a control interface based on Advanced Message Queuing Protocol (AMQP) for consuming control/manage messages from the video-streamer.
There is also an interface in charge to consuming video from the network datapath.

![VS interfaces](https://github.com/Selfnet-5G/video-player/blob/master/resources/vp_1.png?raw=true)


# Installation 
Following commands will install all required dependencies by the video-player. This component is able to work just over Linux SO.

### Dependencies

```sh
$sudo apt-get install python2.7 python2.7-dev -y
```

```sh
$pip install kombu
```
```sh
# installing OpenHEVC
if [ ! -d "./openHEVC" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  git clone git://github.com/OpenHEVC/openHEVC.git
  cd openHEVC
  git checkout hevc_rext
  mkdir build
  cd build
  cmake -DCMAKE_BUILD_TYPE=RELEASE ..
  make
  make install
  cd ..
  cd ..
 else
 	echo "openHEVC is already installed"
fi


# installing GPAC
if [ ! -d "./gpac" ]; then
    # Control will enter here if $DIRECTORY doesn't exist.
    git clone https://github.com/gpac/gpac
    cd gpac
    git checkout tags/v0.6.1
    ./configure
    make
    make install
    cd ..
else
	echo "gpac is already installed"
fi

```
### Configuration
The first step to start using the VP is to create a proper configuration file. The following table shows all required parameters .

#### Configuration (config.ini)

| Player Parameters | Meaning |
| ------ | ------ |
| Rabbit_server_ip | The IP address where the rabbitMQ server is located |
| Vhost | Virtual Host of the rabbitMQ server (If there is not a Virtual Host defined, "/" should be added here) |
| User | User name of the rabbitMQ server |
| Password | Password of the rabbitMQ server |

| Actions Parameters | Meaning |
| ------ | ------ |
| Exchange | Name of the Exchange for consuming action messages |
| Queue_name | Name of the associated queue created by the video-player for consuming those messages |
| Binding_key | Binding key  |

| Commands Parameters | Meaning |
| ------ | ------ |
| Exchange | Name of the Exchange for consuming video command messages published by the video-streamer |
| Queue_name | Name of the associated queue created by the video-player for consuming those messages |
| Binding_key | Binding key  |

# Usage
```
usage: player.py [-h] [-v] [--start]

video flow player

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  --start        The player client will start to consume messages from actions
                 and commands exchanges
```
# Usage Example
   Example of starting the video-player:
    ```
    $ python2.7 player.py --start
    ```
# License
### Authors
5G Video-Streamer. Copyright (C) 01/03/17 Pablo Salva Garcia, Qi wang, Jose M. Alcaraz Calero, James Nightingale. University of the West of Scotland

### License
Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
  