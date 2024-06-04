# Do we have internet left at home

Monitor your home internet connection and report the results of an InfluxDb. Even remotely.


## Features

* Monitors the accessibility of a URL (makes a HEAD request)
* Pushes the result into an InfluxDb
* If the InfluxDb is also not accessible, the result is saved and pushed again the next time
* Uncommitted results are saved even after a container restart. (If a suitable volume is mounted in the container)
