The Django application that runs on [Graniteland.com](https://www.graniteland.com/) and [Graniteland.de](https://www.graniteland.de/).


Setup database:

    $ sudo -u postgres createuser -P graniteland
    $ sudo -u postgres createdb gc
    $ sudo -u postgres createdb gd
    $ sudo -u postgres psql gc < db_dump/gc.pgsql
    $ sudo -u postgres psql gd < db_dump/gd.pgsql

