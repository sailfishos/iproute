##%define date_version 070710
%define cbq_version v0.7.3

Summary: Advanced IP routing and network device configuration tools
Name: iproute
Version: 3.7.0
Release: 1
Group: Applications/System
Source0: %{name}-%{version}.tar.xz
URL:     http://kernel.org/pub/linux/utils/net/%{name}2/
Patch1:  iproute2-3.4.0-kernel.patch
Patch2:  iproute2-3.5.0-optflags.patch
Patch3:  iproute2-3.4.0-sharepath.patch
Patch4:  iproute2-2.6.31-tc_modules.patch
Patch5:  iproute2-2.6.29-IPPROTO_IP_for_SA.patch
Patch6:  iproute2-example-cbq-service.patch
Patch7:  iproute2-2.6.35-print-route.patch
Patch8:  iproute2-2.6.39-create-peer-veth-without-a-name.patch
Patch9:  iproute2-2.6.39-lnstat-dump-to-stdout.patch
Patch10: iproute2-2.6.38-noarpd.patch
Patch11: iproute2-use-busybox-compatible-arguments-for-find.patch
Patch12: include-stdint-explicitly.patch
License: GPLv2+
BuildRequires: flex psutils db4-devel bison
# introduction new iptables (xtables) which broke ipt
Conflicts:     iptables < 1.4.1

%description
The iproute package contains networking utilities (ip and rtmon, for
example) which are designed to use the advanced networking
capabilities of the Linux 2.4.x and 2.6.x kernel.

%package doc
Summary: IP and tc documentation with examples
Group:  Applications/System
License: GPLv2+

%description doc
The iproute documentation contains man pages, howtos and examples of settings.

%prep
%setup -q -n %{name}-%{version}/upstream
%patch1 -p1 -b .kernel
%patch2 -p1 -b .opt_flags
%patch3 -p1 -b .share
%patch4 -p1 -b .ipt
%patch5 -p1 -b .ipproto
%patch6 -p1 -b .fix_cbq
%patch7 -p1 -b .print-route
%patch8 -p1 -b .peer-veth-without-name
%patch9 -p1 -b .lnstat-dump-to-stdout
%patch10 -p1 -b .noarpd
%patch11 -p1 -b .posix-find
%patch12 -p1

%build
export LIBDIR=/%{_libdir}
export IPT_LIB_DIR=/%{_lib}/xtables
%ifnarch %arm
make %{?jobs:-j%jobs}
%else
make
%endif

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/sbin \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_mandir}/man8 \
	$RPM_BUILD_ROOT/%{_sysconfdir}/iproute2 \
	$RPM_BUILD_ROOT%{_datadir}/tc \
	$RPM_BUILD_ROOT%{_libdir}/tc

install -m 755 ip/ip ip/ifcfg ip/rtmon tc/tc $RPM_BUILD_ROOT/sbin
install -m 755 misc/ss misc/nstat misc/rtacct misc/lnstat $RPM_BUILD_ROOT%{_sbindir}
#netem is static
install -m 644 netem/normal.dist netem/pareto.dist netem/paretonormal.dist $RPM_BUILD_ROOT%{_datadir}/tc
install -m 644 man/man8/*.8 $RPM_BUILD_ROOT/%{_mandir}/man8
rm -r $RPM_BUILD_ROOT/%{_mandir}/man8/ss.8
iconv -f latin1 -t utf8 < man/man8/ss.8 > $RPM_BUILD_ROOT/%{_mandir}/man8/ss.8
install -m 755 examples/cbq.init-%{cbq_version} $RPM_BUILD_ROOT/sbin/cbq
install -d -m 755 $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/cbq

cp -f etc/iproute2/* $RPM_BUILD_ROOT/%{_sysconfdir}/iproute2
rm -rf $RPM_BUILD_ROOT/%{_libdir}/debug/*

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}
install -m 644 -t $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version} \
	README README.decnet README.iproute2+tc README.distribution \
        README.lnstat
cp -r examples $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}/

#create example avpkt file
cat <<EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/cbq/cbq-0000.example
DEVICE=eth0,10Mbit,1Mbit
RATE=128Kbit
WEIGHT=10Kbit
PRIO=5
RULE=192.168.1.0/24
EOF

cat <<EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/cbq/avpkt
AVPKT=3000
EOF

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/iproute2
/sbin/*
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*
%{_sbindir}/*
%dir %{_datadir}/tc
%{_datadir}/tc/*

%files doc
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}
%doc %{_mandir}/man8/*
%dir %{_sysconfdir}/sysconfig/cbq
%config(noreplace) %{_sysconfdir}/sysconfig/cbq/*
