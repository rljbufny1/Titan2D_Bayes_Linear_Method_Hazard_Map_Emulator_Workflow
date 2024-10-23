#------------------------------------------------------------------------------------------------------------------------------
# Dockerfile to install the submithostimage Docker image for Pegasus WMS pegasus-aws-batch.
#
# Component of: Titan2D Hazard Map Emulator Workflow
# Purpose: Run a Pegasus WMS workflow on Amazon AWS
# Author: Renette Jones-Ivey
# Date: Sept 2024
#
# Important: need to source ../pegasus-wms-configuration-scripts/configure.sh before building the submithostimage Docker image.
# See ../pegasus-wms-configuration-scripts/configure.sh for more information.
#------------------------------------------------------------------------------------------------------------------------------

# Dockerfile based on https://github.com/pegasus-isi/pegasus/tree/master/tutorial/docker/Dockerfile - Pegasus WMS version 5.0.5

# References:
# https://pegasus.isi.edu/documentation/user-guide/tutorial.html
# https://pegasus.isi.edu/documentation/user-guide/deployment-scenarios.html#
# https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job

# https://docs.docker.com/engine/reference/commandline/build/
# --tag,-t Name
# build:
#   # docker builder prune to remove cache first
#   docker image build -t submithostimage . 2>&1 | tee dockerbuild.log

# https://docs.docker.com/engine/reference/commandline/run/
# --interactive,-i: Keep STDIN open
# --publish,-p: Publish a container's (ports) to the host
# --rm: Remove container when it exits
# --tty,-t: Allocate a pseudo-TTY
# --volume,-v: Bind mount a volume
#
# run:
#   docker run --privileged --rm -v $PWD/emulator/LOCAL/shared-storage:/home/submithost/emulator/LOCAL/shared-storage -p 9999:8888 submithostimage

#   When the Sending DC_SET_READY message appears,
#   open a web browser and enter the url submithost:9999, enter the password emulator and open emulator.ipynb
#
#   For testing:
#   docker run -it submithostimage /bin/sh
#
#   This form maintains previous information:
#   docker run --privileged --rm --name submithostimage-container -p 9999:8888 submithostimage

# On Mac, Docker containers and images are stored in a single file, large file named Docker.raw.
# See:
# ~/Library/Containers/Docker/Data/vms/0/data/Docker.raw
# On Linux,  Docker containers and images are usually stored in the /var/lib/docker directory.

# ====================================================================
# System installations
# ====================================================================

# Rocky Linux is an open-source enterprise operating system compatible with Red Hat Enterprise Linux.
FROM rockylinux:8
LABEL desc="submithost docker image for Pegasus WMS pegasus-aws-batch."

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
     sudo \
     supervisor \
     tar \
     vim \
     wget

# Python packages
RUN python3 -m pip install --upgrade pip
# argon2-cffi-bindings which jupyter requires has a requirements for setuptools_scm>=6.2
RUN python3 -m pip install 'setuptools_scm>=6'
# Verified on Oct 21, 2024, the default version of boto3 installed is version 7.8.4.
RUN python3 -m pip install boto3
RUN python3 -m pip install cartopy
RUN python3 -m pip install cryptography
RUN python3 -m pip install colorcet
RUN python3 -m pip install datashader
RUN python3 -m pip install elevation
# Determined version of GDAL to install with gdalinfo --version
RUN python3 -m pip install GDAL==3.0.4
RUN python3 -m pip install geopandas
RUN python3 -m pip install hublib
# Verified on Sept 12, 2024, the default version of ipywidgets installed is version 7.8.4.
# With this version, the Output widget is not working.
RUN python3 -m pip install ipywidgets==7.0.0
RUN python3 -m pip install jupyter
RUN python3 -m pip install kaleido
RUN python3 -m pip install matplotlib
RUN python3 -m pip install numpy
RUN python3 -m pip install pandas
RUN python3 -m pip install pillow
RUN python3 -m pip install plotly
RUN python3 -m pip install pyproj
RUN python3 -m pip install PyYAML
RUN python3 -m pip install rasterio
RUN python3 -m pip install scipy
RUN python3 -m pip install shapely
RUN python3 -m pip install xarray-spatial

RUN jupyter nbextension enable --py --sys-prefix widgetsnbextension

# Appmode - Jupyter extension that turns notebooks into web applications
RUN python3 -m pip install appmode
RUN jupyter nbextension enable --py --sys-prefix appmode
RUN jupyter serverextension enable --py --sys-prefix appmode

ADD ./pegasus-wms-setup-files/config/start.sh /start.sh
ADD ./pegasus-wms-setup-files/config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD ./pegasus-wms-setup-files/config/wrapdocker /usr/local/bin/wrapdocker
ADD ./pegasus-wms-setup-files/config/htcondor-wrapper /usr/local/bin/htcondor-wrapper
RUN chmod +x /usr/local/bin/wrapdocker /usr/local/bin/htcondor-wrapper
RUN usermod -aG docker submithost

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
ADD ./pegasus-wms-setup-files/config/10-dynamic-slots /etc/condor/config.d/10-dynamic-slots

# ====================================================================
# Pegasus installation
# ====================================================================

# Pegasus -- rebuild everything below here
#            http://dev.im-bot.com/docker-select-caching/
ARG CACHEBUST=1
ARG PEGASUS_VERSION=5.0.9dev
RUN dnf -y install https://download.pegasus.isi.edu/pegasus/$PEGASUS_VERSION/pegasus-$PEGASUS_VERSION-1.el8.x86_64.rpm
# -f, --full, returns internal build metrics including the version. UTC time stamp, in ISO 8601 format, is appended to the version.
RUN pegasus-version -f

# ====================================================================
# Octave installation
# ====================================================================

# Reverified on Sept 12, 2024, the default version of Octave installed is version 5.2.0.
# For Octave 5.2.0, qt not available as a graphics toolkit,
# available_graphics_toolkits() only displays gnuplot.
# Also see: https://trac.macports.org/ticket/58275.
# Created ./emulator/bin/view_phm.py based on ./emulator/bin/view_phm.m which depends on qt.

RUN dnf -y install --allowerasing --nobest \
     octave \
     octave-devel


# For the Docker build, cd ~ > /root
# ./aws/config users' account ID is not needed.
# ./aws/config should not have any region specified.
ADD ./amazon-aws-credentials/.aws/credentials /root/.aws/credentials
ADD ./amazon-aws-credentials/.pegasus /root/.pegasus

ADD ./emulator /home/submithost/emulator
RUN chown -R submithost:submithost-group /home/submithost/emulator
RUN chmod 555 /home/submithost/emulator/remotebin/titanLaunch.sh
RUN chmod 555 /home/submithost/emulator/remotebin/octaveLaunch.sh

ADD ./emulator/pegasusrc /home/submithost/emulator/pegasusrc
# Create pegasusrc_template from the pegasusrc configured with ./pegasus-wms-configure.sh,
# pegasusrc is updated with a new prefix for each workflow run.
ADD ./emulator/pegasusrc /home/submithost/emulator/pegasusrc_template

ADD ./pegasus-wms-scripts /home/submithost/emulator/pegasus-wms-scripts

#RUN echo -e "condor_master > /dev/null 2>&1" >> /home/submithost/.bashrc

# User setup
RUN echo -e "submithost ALL=(ALL)       NOPASSWD:ALL\n" >> /etc/sudoers
USER submithost

RUN mkdir /home/submithost/emulator/conf
ADD ./pegasus-wms-configuration-files/compute-env.json /home/submithost/emulator/conf/compute-env.json
# Add compute_env_json_template,
# compute-env.json can be updated with user selected parameters for each workflow run.
ADD ./pegasus-wms-configuration-files/compute_env_json_template /home/submithost/emulator/conf/compute_env_json_template
ADD ./pegasus-wms-configuration-files/job-definition.json /home/submithost/emulator/conf/job-definition.json
# Create job_definition_json_template from the job-definition.json configured with ./pegasus-wms-configure.sh,
# job-definition.json can be updated with a user selected parameter for each workflow run.
ADD ./pegasus-wms-configuration-files/job-definition.json /home/submithost/emulator/conf/job_definition_json_template
ADD ./pegasus-wms-configuration-files/job-queue.json /home/submithost/emulator/conf/job-queue.json
ADD ./pegasus-wms-configuration-files/sites.xml /home/submithost/emulator/conf/sites.xml

WORKDIR /home/submithost

# Set up config for ensemble manager and service
RUN mkdir /home/submithost/.pegasus \
    && echo -e "#!/usr/bin/env python3\nUSERNAME='submithost'\nPASSWORD='submithost123'\nAUTHENTICATION='NoAuthentication'\nSERVER_HOST='0.0.0.0'\n" >> /home/submithost/.pegasus/service.py \
    && chmod u+x /home/submithost/.pegasus/service.py

USER root

# Required for boto3
ADD ./amazon-aws-credentials/.aws /home/submithost/.aws
RUN chown -R submithost:submithost-group /home/submithost/.aws
ADD ./amazon-aws-credentials/.pegasus/credentials.conf /home/submithost/.pegasus/credentials.conf
RUN chown -R submithost:submithost-group /home/submithost/.pegasus/credentials.conf
RUN chmod 600 /home/submithost/.pegasus/credentials.conf

USER submithost

# Set up pegasus database
RUN pegasus-db-admin create

# Set Kernel for Jupyter (exposes PATH and PYTHONPATH for use when terminal from jupyter is used)
ADD ./pegasus-wms-setup-files/config/kernel.json /usr/local/share/jupyter/kernels/python3/kernel.json
RUN echo -e "export PATH=/home/submithost/.pyenv/bin:\$PATH:/usr/lib64/mpich/bin" >> /home/submithost/.bashrcƒ

# Set notebook password to 'emulator'. This pw will be used instead of token authentication
RUN mkdir /home/submithost/.jupyter \
    && echo "{ \"NotebookApp\": { \"password\": \"sha1:30a323540baa:6eec8eaf3b4e0f44f2f2aa7b504f80d5bf0ad745\" } }" >> /home/submithost/.jupyter/jupyter_notebook_config.json

USER root
CMD ["/start.sh"]


