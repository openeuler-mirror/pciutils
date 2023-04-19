Name:           pciutils
Version:        3.9.0
Release:        2
Summary:        PCI bus related utilities
License:        GPLv2+
URL:            http://atrey.karlin.mff.cuni.cz/~mj/pciutils.shtml
Source0:        https://mirrors.edge.kernel.org/pub/software/utils/pciutils/%{name}-%{version}.tar.gz

# patch0 is from fedora, change pci.ids directory from /usr/share to /usr/share/hwdata
Patch0:         0000-pciutils-2.2.1-idpath.patch
# patch1 is from fedora, rhbz#195327
Patch1:         0001-pciutils-dir-d.patch
Patch2:         0002-Support-specify-CC.patch

ExclusiveOS:    Linux
BuildRequires:  gcc sed kmod-devel pkgconfig zlib-devel
Requires:       hwdata
Provides:       %{name}-libs
Obsoletes:      %{name}-libs
Provides:       %{name}-libs-debuginfo
Obsoletes:      %{name}-libs-debuginfo

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
%autosetup -n %{name}-%{version} -p1

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
/usr/bin/lspci
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
* Wed Apr 19 2023 jammyjellyfish <jammyjellyfish255@outlook.com> - 3.9.0-2
- Support specify CC

* Thu Feb 09 2023 suweifeng <suweifeng1@huawei.com> 3.9.0-1
- upgrade to 3.9.0

* Fri Oct 28 2022 liusirui <liusirui@huawei.com> - 3.8.0-1
- update to v3.8.0

* Tue Sep 6 2022 Wangming Shao <shaowangming@h-partners.com> - 3.7.0-3
- DESC:add support lspci querying 10-bit tag information

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 3.7.0-2
- DESC: delete -Sgit from %autosetup, and delete BuildRequires git

* Thu Jul 16 2020 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 3.7.0-1
- update to v3.7.0 version

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

