# Fedora spec file for php-pecl-msgpack
#
# Copyright (c) 2012-2020 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

# we don't want -z defs linker flag
%undefine _strict_symbol_defs_build

%global upstream_version 2.1.2
%global pecl_name   msgpack
%global ini_name  40-%{pecl_name}.ini
# system library is outdated, and bundled library includes not yet released changes
# BTW, only pack_template.h and unpack_template.h headers are used
%global        with_msgpack 0

Summary:       API for communicating with MessagePack serialization
Name:          php7-pecl-msgpack
Version:       %{upstream_version}%{?upstream_lower:~%{upstream_lower}}
Release:       1%{?dist}
Source:        https://pecl.php.net/get/%{pecl_name}-%{upstream_version}%{?upstream_prever}.tgz
License:       BSD
Group:         Development/Languages
URL:           https://pecl.php.net/package/msgpack

BuildRequires: php7-devel
BuildRequires: php7-pear
%if %{with_msgpack}
BuildRequires: msgpack-devel
%else
Provides:      bundled(msgpack) = 3.2.0
%endif
# https://github.com/msgpack/msgpack-php/issues/25
ExcludeArch: ppc64

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

Provides:      php-%{pecl_name} = %{version}
Provides:      php7-%{pecl_name} = %{version}
Provides:      php-%{pecl_name}%{?_isa} = %{version}
Provides:      php7-%{pecl_name}%{?_isa} = %{version}
Provides:      php-pecl(%{pecl_name}) = %{version}
Provides:      php-pecl(%{pecl_name})%{?_isa} = %{version}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif

%description
This extension provide API for communicating with MessagePack serialization.

MessagePack is an efficient binary serialization format. It lets you exchange
data among multiple languages like JSON but it's faster and smaller.
For example, small integers (like flags or error code) are encoded into a
single byte, and typical short strings only require an extra byte in addition
to the strings themselves.

If you ever wished to use JSON for convenience (storing an image with metadata)
but could not for technical reasons (encoding, size, speed...), MessagePack is
a perfect replacement.

This extension is still EXPERIMENTAL.


%package devel
Summary:       MessagePack developer files (header)
Group:         Development/Libraries
Requires:      php7-pecl-%{pecl_name}%{?_isa} = %{version}-%{release}
Requires:      php7-devel%{?_isa}

%description devel
These are the files needed to compile programs using MessagePack serializer.


%prep
%setup -qc

mv %{pecl_name}-%{upstream_version}%{?upstream_prever} NTS
sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml

cd NTS

%if %{with_msgpack}
# use system library
rm -rf msgpack
%endif

# When this file will be removed, clean the description.
[ -f EXPERIMENTAL ] || exit 1

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_MSGPACK_VERSION/{s/.* "//;s/".*$//;p}' php_msgpack.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}%{?gh_date:-dev}"; then
   : Error: Upstream extension version is ${extver}, expecting %{upstream_version}%{?upstream_prever}%{?gh_date:-dev}.
   exit 1
fi
cd ..

# Drop in the bit of configuration
cat > %{ini_name} << 'EOF'
; Enable MessagePack extension module
extension = %{pecl_name}.so

; Configuration options

;msgpack.error_display = On
;msgpack.illegal_key_insert = Off
;msgpack.php_only = On
EOF


%build
cd NTS
%{_bindir}/phpize7
%configure --with-php-config=%{_bindir}/php7-config
make %{?_smp_mflags}



%install
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Test & Documentation
cd NTS
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do [ -f tests/$i ] && install -Dpm 644 tests/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/tests/$i
   [ -f $i ]       && install -Dpm 644 $i       %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
# Erratic results
rm */tests/034.phpt
# Known by upstream as failed test (travis result)

cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/php7 \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=0 \
%{_bindir}/php7 -n run-tests.php --show-diff


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi

%files
%license NTS/LICENSE
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so


%files devel
%doc %{pecl_testdir}/%{pecl_name}
%{php_incldir}/ext/%{pecl_name}


%changelog
* Mon Nov 30 2020 Remi Collet <remi@remirepo.net> - 2.1.2-1
- update to 2.1.2

* Mon Mar  2 2020 Remi Collet <remi@remirepo.net> - 2.1.0-1
- update to 2.1.0

* Fri May  3 2019 Alexander Ursu <alexander.ursu@gmail.com> - 2.0.3-2
- Corrected dependencies for devel package

* Thu Dec 20 2018 Remi Collet <remi@remirepo.net> - 2.0.3-1
- update to 2.0.3

* Fri Jul 20 2018 Alexander Ursu <alexander.ursu@gmail.com> - 2.0.2-7
- Build for CentOS

* Mon Jan 29 2018 Remi Collet <remi@remirepo.net> - 2.0.2-6
- undefine _strict_symbol_defs_build

* Tue Oct 03 2017 Remi Collet <remi@fedoraproject.org> - 2.0.2-5
- rebuild for https://fedoraproject.org/wiki/Changes/php72

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec  7 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to 2.0.2

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- rebuild for https://fedoraproject.org/wiki/Changes/php71
- add patch for PHP 7.1

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1 (php 7, beta)
- add patch for PHP 7.1
  open https://github.com/msgpack/msgpack-php/pull/87

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 0.5.7-3
- drop scriptlets (replaced by file triggers in php-pear)
- cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Aug 30 2015 Remi Collet <remi@fedoraproject.org> - 0.5.7-1
- Update to 0.5.7 (beta)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 0.5.5-8
- rebuild for https://fedoraproject.org/wiki/Changes/Php56

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Remi Collet <rcollet@redhat.com> - 0.5.5-6
- add numerical prefix to extension configuration file

* Tue Mar 11 2014 Remi Collet <remi@fedoraproject.org> - 0.5.5-5
- cleanups
- move doc in pecl_docdir
- move tests in pecl_testdir (devel)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr  2 2013 Remi Collet <remi@fedoraproject.org> - 0.5.5-3
- use system msgpack library headers

* Tue Mar 26 2013 Remi Collet <remi@fedoraproject.org> - 0.5.5-2
- cleanups

* Wed Feb 20 2013 Remi Collet <remi@fedoraproject.org> - 0.5.5-1
- Update to 0.5.5

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 0.5.3-1.1
- also provides php-msgpack

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> - 0.5.3-1
- update to 0.5.3 (beta)

* Sat Sep 15 2012 Remi Collet <remi@fedoraproject.org> - 0.5.2-1
- initial package, version 0.5.2 (beta)
