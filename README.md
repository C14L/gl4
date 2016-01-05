
Maybe necessary to install before installing pillow

    sudo apt-get install libjpeg-dev libfreetype6-dev

Maybe necessary to add these links into the venv before installing pillow

    ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /opt/elligue/venv/dtr4/lib/
    ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so.6 /opt/elligue/venv/dtr4/lib/
    ln -s /usr/lib/x86_64-linux-gnu/libz.so /opt/elligue/venv/dtr4/lib/

