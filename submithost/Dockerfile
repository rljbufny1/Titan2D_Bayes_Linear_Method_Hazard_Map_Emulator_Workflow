# Install submit host docker image for Pegasus WMS pegasus-aws-batch.

# References:
# https://pegasus.isi.edu/documentation/user-guide/tutorial.html
# https://pegasus.isi.edu/documentation/user-guide/execution-environments.html
# https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job

# Pegasus WMS requires three credential files for Pegasus AWS Batch:
#
# .aws/conf, example:
# [default]
# region = us-east-2
#
# .aws/credentials, example:
# [default]
# aws_access_key_id = *
# aws_secret_access_key = *
#
# .pegasus/credentials.conf, example:
# [amazon]
# endpoint = https://s3.amazonaws.com
# # Max object size in MB
# max_object_size = 1024
# multipart_uploads = True
# ranged_downloads = True
# [user@amazon]
# access_key = *
# secret_key = *
#
# where * is replaced with your Amazon AWS credential information.

# https://docs.docker.com/engine/reference/commandline/build/
# --tag,-t Name
# build:
#   docker image build -t submithostimage . 2>&1 | tee build.log

# https://docs.docker.com/engine/reference/commandline/run/
# --interactive,-i Keep STDIN open even if not attached
# --tty,-t Allocate a pseudo-TTY
# run:
#   For testing:
#   docker run -it submithostimage /bin/sh
#
#   Use this form:
#   docker run --privileged --rm -p 9999:8888 submithostimage
#   When the Sending DC_SET_READY message appears,
#   open a web browser and enter the url submithost:9999, enter the password emulator and open emulator.ipynb
#
#   This form maintains previous information:
#   docker run --privileged --rm --name submithostimage-container -p 9999:8888 submithostimage

# On Mac, Docker containers and images are stored in a single file, large file named Docker.raw.
# See:
# ~/Library/Containers/Docker/Data/vms/0/data/Docker.raw
# On Linux,  Docker containers and images are usually stored in the /var/lib/docker directory.

# System packages

# Rocky Linux is an open-source enterprise operating system compatible with Red Hat Enterprise Linux.
FROM rockylinux:8

RUN groupadd --gid 808 submithost-group
RUN useradd --gid 808 --uid 550 --create-home --password '$6$ouJkMasm5X8E4Aye$QTFH2cHk4b8/TmzAcCxbTz7Y84xyNFs.gqm/HWEykdngmOgELums1qOi3e6r8Z.j7GEA9bObS/2pTN1WArGNf0' submithost

RUN dnf -y update && \
    dnf -y install 'dnf-command(config-manager)' && \
    dnf -y config-manager --set-enabled powertools && \
    dnf -y config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo && \
    dnf -y install epel-release

# gcc, gcc-c++ plus others
RUN dnf -y groupinstall "Development Tools"

RUN dnf -y install --allowerasing --nobest \
     curl \
     gcc \
     docker-ce \
     emacs \
     geos-devel \
     gdal \
     gdal-devel \
     glibc-langpack-en \
     graphviz \
     grass \
     grass-devel \
     java-11-openjdk-devel \
     langpacks-en \
     nano \
     perl-Getopt-Long \
     proj \
     proj-devel \
     python3-devel \
     python3-GitPython \
     python3-pika \
     python3-pip \
     python3-cryptography \
     python3-PyYAML \
     python3-matplotlib \
     python3-numpy \
     python3-pandas \
     python3-pyproj \
     python3-scipy \
     python3-shapely \
     sudo \
     supervisor \
     tar \
     vim \
     wget

ADD ./config/start.sh /start.sh
ADD ./config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD ./config/wrapdocker /usr/local/bin/wrapdocker
ADD ./config/htcondor-wrapper /usr/local/bin/htcondor-wrapper
RUN chmod +x /usr/local/bin/wrapdocker /usr/local/bin/htcondor-wrapper
RUN usermod -aG docker submithost

# Python packages
# argon2-cffi-bindings which jupyter requires has a requirements for setuptools_scm>=6.2
RUN python3 -m pip install 'setuptools_scm>=6'
RUN python3 -m pip install cartopy
RUN python3 -m pip install elevation
# Determine version of GDAL to install with gdalinfo --version
RUN python3 -m pip install GDAL==3.0.4
RUN python3 -m pip install geopandas
RUN python3 -m pip install hublib
RUN python3 -m pip install jupyter
RUN python3 -m pip install kaleido
RUN python3 -m pip install plotly
RUN python3 -m pip install rasterio

# Appmode - Jupyter extension that turns notebooks into web applications
RUN python3 -m pip install appmode
RUN jupyter nbextension enable --py --sys-prefix appmode
RUN jupyter serverextension enable --py --sys-prefix appmode

# Locale and timezone
ENV LANG en_US.UTF-8
RUN cp /usr/share/zoneinfo/America/New_York /etc/localtime

# ====================================================================
# HTCondor installation
# ====================================================================

RUN dnf -y config-manager --add-repo=https://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel8.repo && \
    rpm --import https://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor && \
    dnf -y install condor minicondor && \
    sed -i 's/condor@/submithost@/g' /etc/condor/config.d/00-minicondor

RUN usermod -a -G condor submithost
RUN chmod -R g+w /var/{lib,log,lock,run}/condor
ADD ./config/10-dynamic-slots /etc/condor/config.d/10-dynamic-slots

# ====================================================================
# Pegasus installation
# ====================================================================

# Pegasus -- rebuild everything below here
#            http://dev.im-bot.com/docker-select-caching/
ARG CACHEBUST=1
ARG PEGASUS_VERSION=5.0.5
RUN dnf -y install https://download.pegasus.isi.edu/pegasus/$PEGASUS_VERSION/pegasus-$PEGASUS_VERSION-1.el8.x86_64.rpm

# ====================================================================
# Octave installation
# ====================================================================

# Installs Octave 5.2.0.
# For Octave 5.2.0 qt not available as a graphics toolkit,
# available_graphics_toolkits() only displays gnuplot
# https://trac.macports.org/ticket/58275

RUN dnf -y install --allowerasing --nobest \
     octave \
     octave-devel

# For the Docker build, cd ~ > /root
ADD ./.aws /root/.aws
ADD ./.pegasus /root/.pegasus

ADD ./emulator /home/submithost/emulator
RUN chown -R submithost:submithost-group /home/submithost/emulator
RUN chmod 555 /home/submithost/emulator/remotebin/titanLaunch.sh
RUN chmod 555 /home/submithost/emulator/remotebin/octaveLaunch.sh

#RUN echo -e "condor_master > /dev/null 2>&1" >> /home/submithost/.bashrc

# User setup
RUN echo -e "submithost ALL=(ALL)       NOPASSWD:ALL\n" >> /etc/sudoers
USER submithost

WORKDIR /home/submithost

# Set up config for ensemble manager and service
RUN mkdir /home/submithost/.pegasus \
    && echo -e "#!/usr/bin/env python3\nUSERNAME='submithost'\nPASSWORD='submithost123'\nAUTHENTICATION='NoAuthentication'\nSERVER_HOST='0.0.0.0'\n" >> /home/submithost/.pegasus/service.py \
    && chmod u+x /home/submithost/.pegasus/service.py

USER root
ADD ./.aws /home/submithost/.aws
RUN chown -R submithost:submithost-group /home/submithost/.aws
ADD ./.pegasus/credentials.conf /home/submithost/.pegasus/credentials.conf
RUN chown -R submithost:submithost-group /home/submithost/.pegasus/credentials.conf

USER submithost

# Set up pegasus database
RUN pegasus-db-admin create

# Set Kernel for Jupyter (exposes PATH and PYTHONPATH for use when terminal from jupyter is used)
ADD ./config/kernel.json /usr/local/share/jupyter/kernels/python3/kernel.json
RUN echo -e "export PATH=/home/submithost/.pyenv/bin:\$PATH:/usr/lib64/mpich/bin" >> /home/submithost/.bashrcƒ

# Set notebook password to 'emulator'. This pw will be used instead of token authentication
RUN mkdir /home/submithost/.jupyter \
    && echo "{ \"NotebookApp\": { \"password\": \"sha1:30a323540baa:6eec8eaf3b4e0f44f2f2aa7b504f80d5bf0ad745\" } }" >> /home/submithost/.jupyter/jupyter_notebook_config.json

USER root
CMD ["/start.sh"]


