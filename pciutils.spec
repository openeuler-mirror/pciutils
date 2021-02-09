Name:           pciutils
Version:        3.6.4
Release:        4
Summary:        PCI bus related utilities
License:        GPLv2+
URL:            http://atrey.karlin.mff.cuni.cz/~mj/pciutils.shtml
Source0:        https://mirrors.edge.kernel.org/pub/software/utils/pciutils/%{name}-%{version}.tar.gz


ExclusiveOS:    Linux
BuildRequires:  gcc git sed kmod-devel pkgconfig zlib-devel

%ifarch i686
BuildRequires:	which kmod-libs
%endif

Requires:       hwdata
Provides:       %{name}-libs
Obsoletes:      %{name}-libs
Provides:       %{name}-libs-debuginfo
Obsoletes:      %{name}-libs-debuginfo

#change pci.ids directory to hwdata, fedora/rhel specific
Patch6000:      6000-pciutils-2.2.1-idpath.patch

#add support for directory with another pci.ids, rejected by upstream, rhbz#195327
Patch6001:      6001-pciutils-dir-d.patch

%description
The PCI Utilities are a collection of programs for inspecting and manipulating configuration
of PCI devices, all based on a common portable library libpci which offers access to the PCI
configuration space on a variety of operating systems.

The utilities include:
lspci
    displays detailed information about all PCI buses and devices in the system
setpci
    allows reading from and writing to PCI device configuration registers. For example, you
    can adjust the latency timers with it.

%package devel
Summary:   Library and Include Files of the PCI utilities
Requires:  zlib-devel pkgconfig %{name} = %{version}-%{release}
Provides:  %{name}-devel-static
Obsoletes: %{name}-devel-static

%description devel
This package contains the files that are necessary for software
development using the PCI utilities.

%package help
Summary: Including man files for pciutils
Requires: man

%description    help
This contains man files for the using of pciutils.

%prep
%autosetup -Sgit -n %{name}-%{version}

%build
make SHARED="no" ZLIB="no" LIBKMOD=yes STRIP="" OPT="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS" PREFIX="/usr" %{?_smp_mflags}
mv lib/libpci.a lib/libpci.a.tobak

make clean

make SHARED="yes" ZLIB="no" LIBKMOD=yes STRIP="" OPT="$RPM_OPT_FLAGS"  PREFIX="/usr" LIBDIR="/%{_lib}"  %{?_smp_mflags}
sed -i "s|^libdir=.*$|libdir=/%{_lib}|" lib/libpci.pc

%install
make install PREFIX=$RPM_BUILD_ROOT/usr SBINDIR=$RPM_BUILD_ROOT/sbin \
             ROOT=$RPM_BUILD_ROOT/ MANDIR=$RPM_BUILD_ROOT/%{_mandir} STRIP="" \
             SHARED="yes" LIBDIR=$RPM_BUILD_ROOT/%{_lib}

install -d $RPM_BUILD_ROOT/{%{_libdir}/pkgconfig,%{_includedir}/pci}
mv lib/libpci.a.tobak lib/libpci.a
install -p -m 644 lib/libpci.a $RPM_BUILD_ROOT%{_libdir}
cp -p lib/{pci,header,config,types}.h $RPM_BUILD_ROOT%{_includedir}/pci
install -p lib/config.h $RPM_BUILD_ROOT%{_includedir}/pci/config.%{_lib}.h
/sbin/ldconfig -N $RPM_BUILD_ROOT%{_libdir}
install -p lib/libpci.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig
install -D -m 0644 lib/libpci.pc %{buildroot}%{_libdir}/pkgconfig/libpci.pc
install -p lib/libpci.so.* $RPM_BUILD_ROOT/%{_lib}/
ln -s ../../%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/*.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libpci.so
rm -rf $RPM_BUILD_ROOT/usr/share/hwdata/pci.ids*

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README ChangeLog pciutils.lsm COPYING
/sbin/lspci
/sbin/setpci
/sbin/update-pciids
/%{_lib}/libpci.so.*

%files devel
%defattr(0644, root, root, 0755)
%{_libdir}/pkgconfig/libpci.pc
%{_libdir}/libpci.so
%{_includedir}/pci
%{_libdir}/libpci.a

%files help
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Feb 9 2021 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 3.6.4-4
- solve i686 dependency problem and set release num to 4 for CI

* Tue Apr 14 2020 linfeilong<linfeilong@huawei.com> - 3.6.4-1
- Type:enhancemnet
- ID:NA
- SUG:NA
- DESC:update to 3.6.4

* Tue Mar 17 2020 hy-euler <eulerstoragemt@huawei.com> - 3.6.2-5
- Type:enhancemnet
- ID:NA
- SUG:NA
- DESC:add fedora patches for displaying more information while running lspci

* Tue Jan 7 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.6.2-4
- Type:enhancemnet
- ID:NA
- SUG:NA
- DESC:update package

* Thu Aug 29 2019 zoujing <zoujing13@huawei.com> - 3.6.2-3
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESC:openEuler Debranding

* Mon Apr 15 2019 Buildteam <buildteam@openeuler.org> - 3.6.2-2
- Package Initialization

