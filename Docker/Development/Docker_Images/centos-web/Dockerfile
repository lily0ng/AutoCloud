# CentOS Web Server
FROM centos:7

# Install EPEL repository
RUN yum -y install epel-release

# Install web server packages
RUN yum -y update && yum -y install \
    httpd \
    php \
    php-mysql \
    mariadb \
    && yum clean all

# Configure Apache
RUN sed -i 's/Listen 80/Listen 8080/' /etc/httpd/conf/httpd.conf

# Expose port 8080
EXPOSE 8080

# Start Apache
CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]
