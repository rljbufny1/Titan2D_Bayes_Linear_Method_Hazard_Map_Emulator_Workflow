#------------------------------------------------------------------------------------------------------------------------------
# Dockerfile to install the remote host Docker image for Pegasus WMS pegasus-aws-batch.
#
# Component of: Titan2D Hazard Map Emulator Workflow
# Purpose: Run a Pegasus WMS workflow on Amazon AWS
# Author: Renette Jones-Ivey
# Date: Sept 2024
#
# Important: need to source ../pegasus-wms-configuration-scripts/configure.sh before building the remotehostimage Docker image.
# See ../pegasus-wms-configuration-scripts/configure.sh for more information.
#
# When the remotehostimage Docker image is created or updated,
# need to upload the image to the Amazon Elastic Container Registry (ECR) repository.
# See ./push-remotehostimage-to-ECR.sh for more information.

#-------------------------------------------------------------------------------------------------------------------------------

# References:
#
# https://pegasus.isi.edu/documentation/user-guide/deployment-scenarios.html#
# https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job
# https://github.com/jsperhac/titan2d-docker

# https://docs.docker.com/engine/reference/commandline/build/
# --tag,-t Name
# build:
#   # docker builder prune to remove cache first
#   docker image build -t remotehostimage . 2>&1 | tee build.log

# ====================================================================
# System installations
# ====================================================================

# Rocky Linux is an open-source enterprise operating system compatible with Red Hat Enterprise Linux.
FROM rockylinux:8
LABEL desc="remotehost Docker image for Pegasus WMS pegasus-aws-batch."

# Create directories for the build
ENV TITAN_WSP=/opt/titan_wsp

# Core count for compilation
ENV NUM_PROCESSES=4

RUN dnf -y update && \
    dnf -y install 'dnf-command(config-manager)' && \
    dnf -y config-manager --set-enabled powertools && \
    dnf -y config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo && \
    dnf -y install epel-release

# Note: perl findutils, aws cli, unzip and futures required for pegasus-aws-batch

RUN dnf -y install --allowerasing --nobest \
    autoconf \
    automake \
    gcc-c++ \
    git \
    make \
    perl findutils \
    python2-devel \
    python2-pip \
    python3-devel \
    python3-pip \
    sudo \
    swig \
    wget \
    which \
    unzip \
    zlib*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN sudo ./aws/install

# Python packages
RUN python2 -m pip install --upgrade pip
RUN python2 -m pip install futures

# ====================================================================
# hdf5 installation
#   hierarchical data format (HDF)
# ====================================================================
# serial version of hdf5 with C++ support

ENV HDF5_VERSION=1.8.18
ENV TITAN_HDF5=${TITAN_WSP}/hdf5-${HDF5_VERSION}
WORKDIR $TITAN_WSP/bld

RUN wget -q https://support.hdfgroup.org/ftp/HDF5/prev-releases/hdf5-1.8/hdf5-${HDF5_VERSION}/src/hdf5-${HDF5_VERSION}.tar && \
    tar xvf hdf5-${HDF5_VERSION}.tar && \
    cd hdf5-${HDF5_VERSION} && \
    ./configure --prefix=$TITAN_HDF5 --enable-cxx && \
    make -j $NUM_PROCESSES && \
    make install

# ====================================================================
# GDAL installation
#   translator library for raster and vector geospatial data
# ====================================================================

ENV GDAL_VERSION=2.1.0
ENV TITAN_GDAL=${TITAN_WSP}/gdal-${GDAL_VERSION}
WORKDIR $TITAN_WSP/bld

RUN wget -q http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz && \
    tar xvzf gdal-${GDAL_VERSION}.tar.gz && \
    cd gdal-${GDAL_VERSION} && \
    ./configure --prefix=$TITAN_GDAL \
        --with-png=internal \
        --with-jpeg=internal \
        --without-curl \
        --without-pg \
        --without-mysql \
        --without-sqlite3 \
        --without-pcre \
        --without-xml2 && \
    make -j $NUM_PROCESSES && \
    make install

# ==========================================================================
# titan2d configure, compile, and install
# including:
#   generate all autotools scripts (i.e. configure script and others).
#
# Created the TITAN2D Titan2D_Hazard_Map_Emulator_Workflow_Remotehost branch
# on Sept 18, 2024, master - 28ce6f4 506 commits
# ==========================================================================

ENV TITAN_SWIG=/usr/bin
WORKDIR $TITAN_WSP/titan2d_bld/iccoptompmpi
WORKDIR $TITAN_WSP

RUN git clone --single-branch --branch Titan2D_Hazard_Map_Emulator_Workflow_Remotehost https://github.com/TITAN2D/titan2d.git && \
    cd titan2d && \
    aclocal && autoheader && autoconf && automake --add-missing --copy && \
    cd $TITAN_WSP/titan2d_bld/iccoptompmpi && \
    ../../titan2d/configure --prefix=`pwd` \
        CXX=g++ \
        CXXFLAGS=-O3 \
        --enable-openmp \
        --with-gdal=$TITAN_GDAL \
        --with-hdf5=$TITAN_HDF5 \
        --with-swig=$TITAN_SWIG \
        --disable-java-gui && \
    make -j $NUM_PROCESSES && \
    make install

# ====================================================================
# Octave installation
# ====================================================================

# Reverified on Sept 12, 2024, the default version of Octave installed is version 5.2.0.
RUN dnf -y install --allowerasing --nobest \
     octave \
     octave-devel

ADD fetch_and_run.sh /usr/local/bin/fetch_and_run.sh

USER root
RUN ln -s /usr/bin/python2.7 /usr/bin/python

WORKDIR /tmp
USER nobody
ENTRYPOINT ["/usr/local/bin/fetch_and_run.sh"]
