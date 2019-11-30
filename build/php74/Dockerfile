ARG centos=7
ARG image=php-igbinary-7.4

FROM aursu/peclbuild:${centos}-${image}

RUN yum -y --enablerepo=custom --enablerepo=bintray-php74custom install \
        php-pecl-msgpack-devel \
    && yum clean all && rm -rf /var/cache/yum /var/cache/dnf
