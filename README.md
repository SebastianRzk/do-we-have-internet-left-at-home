# Do we have internet left at home

Monitor your home internet connection and report the results into an InfluxDb. Even remotely.


## Features

* Monitors the accessibility of a URL (makes a HEAD request)
* Pushes the result into an InfluxDb
* If the InfluxDb is also not accessible, the result is saved and pushed again the next time
* Uncommitted results are saved even after a container restart. (If a suitable volume is mounted in the container)
* Pre-built images for amd64 ( sebastianrzk/do-we-have-internet-left-at-home:latest-amd64 ) and arm64 ( sebastianrzk/do-we-have-internet-left-at-home:latest-arm64 ) 
* Example docker-compose file for local build (docker-compose.local.yml) and existing images (docker-compose.yml)
* Sorting out down-time measurements if there is a downtime > 2 hours (to reduce disk usage (read / write) on client)
