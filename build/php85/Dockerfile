ARG os=10.1.20251126
ARG image=php-igbinary-8.5

FROM aursu/peclbuild:${os}-${image}

RUN dnf -y --repo=bintray-phpcustom install \
        php-pecl-msgpack-devel \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
