ARG centos=7
ARG image=php-7.1

FROM aursu/pearbuild:${centos}-${image}

COPY SOURCES ${BUILD_TOPDIR}/SOURCES
COPY SPECS ${BUILD_TOPDIR}/SPECS

RUN chown -R $BUILD_USER ${BUILD_TOPDIR}/{SOURCES,SPECS}

USER $BUILD_USER

ENTRYPOINT ["/usr/bin/rpmbuild", "php7-pecl-msgpack.spec"]
CMD ["-ba"]
