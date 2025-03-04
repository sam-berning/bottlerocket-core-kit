Name: %{_cross_os}kmod
Version: 33
Release: 1%{?dist}
Summary: Tools for kernel module loading and unloading
License: GPL-2.0-or-later AND LGPL-2.1-or-later
URL: http://git.kernel.org/?p=utils/kernel/kmod/kmod.git;a=summary
Source0: https://www.kernel.org/pub/linux/utils/kernel/kmod/kmod-%{version}.tar.xz
Source1: https://www.kernel.org/pub/linux/utils/kernel/kmod/kmod-%{version}.tar.sign
Source2: gpgkey-EAB33C9690013C733916AC839BA2A5A630CBEA53.asc
BuildRequires: %{_cross_os}glibc-devel
BuildRequires: %{_cross_os}libz-devel
BuildRequires: %{_cross_os}libzstd-devel
Requires: %{_cross_os}libz
Requires: %{_cross_os}libzstd

%description
%{summary}.

%package devel
Summary: Files for development using the tools for kernel module loading and unloading
Requires: %{name}

%description devel
%{summary}.

%prep
%{gpgverify} --data=<(xzcat %{S:0}) --signature=%{S:1} --keyring=%{S:2}
%autosetup -n kmod-%{version} -p1
cp COPYING COPYING.LGPL
cp tools/COPYING COPYING.GPL

%build

%define _configure ../configure

mkdir static-build
pushd static-build
%cross_configure \
  --with-noarch-pkgconfigdir=%{_cross_pkgconfigdir} \
  --with-zlib \
  --with-zstd \
  --without-openssl \
  --disable-manpages

%make_build LDFLAGS="-all-static"

popd

mkdir dynamic-build
pushd dynamic-build

%cross_configure \
  --with-noarch-pkgconfigdir=%{_cross_pkgconfigdir} \
  --with-zlib \
  --with-zstd \
  --without-openssl \
  --disable-manpages

%make_build

popd

%install
pushd dynamic-build
%make_install
popd

pushd static-build
install -p tools/kmod %{buildroot}%{_cross_bindir}

install -d %{buildroot}%{_cross_sbindir}
ln -s ../bin/kmod %{buildroot}%{_cross_sbindir}/modprobe
popd

%files
%license COPYING.LGPL COPYING.GPL
%{_cross_attribution_file}
%{_cross_bindir}/kmod
%{_cross_bindir}/depmod
%{_cross_bindir}/insmod
%{_cross_bindir}/lsmod
%{_cross_bindir}/modinfo
%{_cross_bindir}/modprobe
%{_cross_bindir}/rmmod
%{_cross_sbindir}/modprobe
%{_cross_libdir}/*.so.*
%exclude %{_cross_datadir}/bash-completion

%files devel
%{_cross_libdir}/*.so
%{_cross_includedir}/*.h
%{_cross_pkgconfigdir}/*.pc
%changelog
