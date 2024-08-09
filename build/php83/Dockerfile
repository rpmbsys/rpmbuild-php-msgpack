ARG os=9.4.20240523
ARG image=php-igbinary-8.3

FROM aursu/peclbuild:${os}-${image}

RUN dnf -y --repo=bintray-phpcustom install \
        php-pecl-msgpack-devel \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
