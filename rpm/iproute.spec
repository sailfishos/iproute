Summary: Advanced IP routing and network device configuration tools
Name: iproute
Version: 5.15.0
Release: 1
Source0: %{name}-%{version}.tar.xz
URL:     https://github.com/sailfishos/iproute
License: GPLv2+
BuildRequires: flex psutils db4-devel bison

%description
The iproute package contains networking utilities (ip and rtmon, for
example) which are designed to use the advanced networking
capabilities of the Linux 2.4.x and 2.6.x kernel.

%package doc
Summary: IP and tc documentation with examples

%description doc
The iproute documentation contains man pages, howtos and examples of settings.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%configure
%make_build

%install
export SBINDIR='%{_sbindir}'
export LIBDIR='%{_libdir}'
%make_install


%files
%defattr(-,root,root,-)
%license COPYING
%dir %{_sysconfdir}/iproute2
%attr(644,root,root) %config %{_sysconfdir}/iproute2/*
%{_sbindir}/*
%dir %{_libdir}/tc/
%{_libdir}/tc/*
%exclude %{_datadir}/bash-completion/completions/*
%exclude %{_includedir}/iproute2/bpf_elf.h

%files doc
%defattr(-,root,root,-)
%doc %{_mandir}/man3/*
%doc %{_mandir}/man7/*
%doc %{_mandir}/man8/*
