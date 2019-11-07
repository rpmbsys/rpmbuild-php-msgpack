ARG centos=7
ARG image=php-igbinary-7.1

FROM aursu/peclbuild:${centos}-${image}

RUN yum -y --enablerepo=custom --enablerepo=bintray-php71custom install \
        php-pecl-msgpack-devel \
    && yum clean all && rm -rf /var/cache/yum
