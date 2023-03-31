FROM python:3.9
LABEL maintainer="Valentin Sasyan <valentin.sasyan@ign.fr>"

ARG tag

# set noninteractive installation
ENV DEBIAN_FRONTEND="noninteractive"
ENV PATH="/var/www/.local/bin:$PATH"

# Proxy for apt
RUN \
    echo 'Acquire::http::Proxy "http://proxy.ign.fr:3128";' >> /etc/apt/apt.conf.d/proxy & \
    echo 'Acquire::https::Proxy "http://proxy.ign.fr:3128";' >> /etc/apt/apt.conf.d/proxy

# Proxy env var
ENV http_proxy=http://proxy.ign.fr:3128
ENV https_proxy=http://proxy.ign.fr:3128
ENV HTTP_PROXY=http://proxy.ign.fr:3128
ENV HTTPS_PROXY=http://proxy.ign.fr:3128

# Install needed programs
RUN apt-get update
RUN apt-get install -y tzdata apache2

# Configure tzdata
RUN ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

# Apache config
RUN mkdir -p /etc/ssl/apache2/
ADD ./config/apache/website.conf /etc/apache2/sites-available/
RUN a2ensite website
RUN a2dissite 000-default.conf
RUN a2enmod rewrite

# Apache files and users
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
RUN mkdir -p $APACHE_RUN_DIR $APACHE_LOCK_DIR $APACHE_LOG_DIR

# Gestion des droits du dossier
RUN chown www-data:www-data -R /var/www

# Changement d'utilisateur
USER www-data

# Git config
RUN git config --global user.email "docker-container@ign.fr"
RUN git config --global user.name "Docker Container"

# Récupération du dépôt git
RUN mkdir -p /var/www
RUN git clone --depth 1 -b $tag https://github.com/ignf-sidc/ignf-gpf-api.git /var/www/ignf-gpf-api
WORKDIR "/var/www/ignf-gpf-api"

# Installation des dépendances
RUN python3 -m pip install --user --upgrade pip setuptools flit
RUN python3 -m flit install --extras all
RUN mkdocs build

# Point d'entrée
USER root
#ENTRYPOINT ["/bin/bash"]
CMD ["apache2ctl", "-D", "FOREGROUND"]
