ARG os=8.8.20230518
ARG image=php-igbinary-8.1

FROM aursu/peclbuild:${os}-${image}

RUN dnf -y --repo=bintray-phpcustom install \
        php-pecl-msgpack-devel \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
