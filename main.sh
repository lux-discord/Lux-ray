# Install needed build dependencies
install-pkg build-essential zlib1g-dev \
        libncurses5-dev libgdbm-dev libnss3-dev \
        libssl-dev libreadline-dev libffi-dev curl

python_version="3.9.5"

# Grab the latest version of Python
wget https://www.python.org/ftp/python/${python_version}/Python-${python_version}.tar.xz
tar -xf Python-${python_version}.tar.xz

# Configure Python
DIR=$(pwd)

cd Python-${python_version}
./configure --enable-optimizations --prefix=${DIR}/python

# Install
make install

# Clean up
cd ~/$REPL_SLUG
rm Python-${python_version}.tar.xz
rm -rf Python-${python_version}
