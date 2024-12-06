# Base R environment - you can specify your R version here
FROM r-base:4.3.2
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
# Install a python distribution on top of this - specify the Python ersion here
RUN apt-get install -y --no-install-recommends build-essential libpq-dev python3.12 python3-pip python3-setuptools python3-dev
# Some libraries you need to compile important R packages. You might need to add/remove stuff here, if your docker environment does not build
RUN apt-get install -y libcurl4-openssl-dev libxml2-dev libfontconfig1-dev libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev libhdf5-serial-dev libgit2-dev

WORKDIR .

# Paths to requirements files for Python and R
ADD requirements.txt .
ADD requirements.r .

# installing python libraries
RUN pip3 install setuptools --break-system-packages
RUN pip3 install -r requirements.txt --break-system-packages

# installing r libraries
RUN Rscript requirements.r



