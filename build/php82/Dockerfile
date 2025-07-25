ARG os=10.0.20250606
ARG image=php-igbinary-8.2

FROM aursu/peclbuild:${os}-${image}

RUN dnf -y --repo=bintray-phpcustom install \
        php-pecl-msgpack-devel \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
