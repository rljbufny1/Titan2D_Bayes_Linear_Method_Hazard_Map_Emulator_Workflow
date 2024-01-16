# Install remotehost docker image for Pegasus WMS pegasus-aws-batch.

# References:
# https://pegasus.isi.edu/documentation/user-guide/execution-environments.html
# https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job
# https://github.com/jsperhac/titan2d-docker
# https://wiki.octave.org/Octave_for_GNU/Linux

# When the image is created or updated,
# need to create or update the Amazon Elastic Container Registry repository remotehost docker image,
# this requires that the ~/.aws/credential aws access key is activated via the Amazon AWS console.
# See ./build-and-push-docker-image-to-ECR.sh for more information.

# https://docs.docker.com/engine/reference/commandline/build/
# --tag,-t Name
# build:
#   docker image build -t remotehostimage .

# https://docs.docker.com/engine/reference/commandline/run/
# --interactive,-i Keep STDIN open even if not attached
# --tty,-t Allocate a pseudo-TTY
# run:
#   For initial testing:
#   docker run -it remotehostimage /bin/sh

# System packages

# See CCR vortex /etc/os-release: CentOS Linux version 7
FROM centos:7
LABEL desc="remotehost docker image for Pegasus WMS pegasus-aws-batch."

# Create directories for the build
ENV TITAN_WSP=/opt/titan_wsp

# Core count for compilation
ENV NUM_PROCESSES=4

RUN yum -y update && \
    yum -y install \
        epel-release
        
# Note: perl findutils, aws cli, unzip and futures required for pegasus-aws-batch

RUN yum -y update && \
    yum -y install \
        autoconf \
        automake \
        gcc-c++ \
        git \
        make \
        netcdf-4.3.3.1 \
	    perl findutils \
        python-devel \
        python-pip \
        sudo \
        swig3 \
        wget \
        which \
        unzip \
        zlib*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN sudo ./aws/install

RUN python -m pip install futures

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

# ====================================================================
# titan2d configure, compile, and install
# including:
#   generate all autotools scripts (i.e. configure script and others).
# ====================================================================
#ENV TITAN_SWIG=`rpm -ql swig3 | grep bin | grep "/swig3"$ | awk -F 'swig3' '{print $1}'`

ENV TITAN_SWIG=/usr/bin
WORKDIR $TITAN_WSP/titan2d_bld/iccoptompmpi
WORKDIR $TITAN_WSP

RUN git clone https://github.com/TITAN2D/titan2d.git && \
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
# octave-4.0.0 installation
# ====================================================================

ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk

# Octave dependencies

RUN yum-builddep -y octave

# Fix A BLAS library was detected but found incompatible with your Fortran 77 compiler settings error configuring Octave-4.0.0
RUN yum -y update && \
    yum -y install \
    blas-devel \
    lapack-devel
    
# Octave-4.0.0
RUN wget ftp://ftp.gnu.org/gnu/octave/octave-4.0.0.tar.gz && \
    tar zxvf octave-4.0.0.tar.gz && \
    cd octave-4.0.0 && \
    ./configure --prefix=/usr/local/OCTAVE/4.0.0 && \
    make -j $NUM_PROCESSES && \
    make install

# (For initial testing do not set ENTRYPOINT.)
ADD fetch_and_run.sh /usr/local/bin/fetch_and_run.sh
WORKDIR /tmp
USER nobody
ENTRYPOINT ["/usr/local/bin/fetch_and_run.sh"]


