ARG os=8.7.20221112
ARG image=php-igbinary-7.4

FROM aursu/peclbuild:${os}-${image}

RUN dnf -y --repo=bintray-phpcustom install \
        php-pecl-msgpack-devel \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
