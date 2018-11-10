# Audio data source merge project

Took data from legacy filemaker database and from Piction, both super dirty and super flat.

Joining the data involved mega cleanup using OpenRefine.

The initial output was a single CSV that contained one row per recording, with columns representing various attributes that could be associated with a recording, along with an arbitrary number of columns representing film titles being discussed and speakers present on the recording.

The CSV is parsed and a JSON object representing the normalized data is created. The JSON object is the parsed and each item inserted into a corresponding MySQL database.

Currently the data seems destined to live in a new FileMaker database that will be able to feed descriptive data for digital objects into [EDITH](https://github.com/BAM-PFA/edith)

If you are interested in trying it out, I included all our raw data, the final OpenRefine project file after the data sources were merged, and MySQL dumps. It's written in Python 3 and the only dependencies are MySQL and the `mysql.connector` Python library.

* MySQL Connector/Python is used for MySQL access:
    * On a Mac: Try `brew install mysql-connector-c` and `pip3 install mysql-connector`, which may reaquire `brew install protobuf`. If that fails then try `pip3 install mysql-connector==2.1.6` for a version that is not so picky about Protobuf.
    * On Ubuntu 16.04 Just running `pip3 install mysql-connector==2.1.6` seems to work.
* You need MySQL root privileges on the host machine.