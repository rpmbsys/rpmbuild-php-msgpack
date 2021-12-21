ARG centos=7.9.2009
ARG image=php-igbinary-7.4

FROM aursu/peclbuild:${centos}-${image}

RUN yum -y --enablerepo=bintray-phpcustom install \
        php-pecl-msgpack-devel \
    && yum clean all && rm -rf /var/cache/yum /var/cache/dnf
