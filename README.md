# Video-player

# Configuration (config.ini)

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