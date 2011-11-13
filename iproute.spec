##%define date_version 070710
%define cbq_version v0.7.3

Summary: Advanced IP routing and network device configuration tools
Name: iproute
Version: 2.6.38
Release: 4
Group: Applications/System
Source: http://developer.osdl.org/dev/iproute2/download/iproute2-%{version}.tar.bz2
#Source1: iproute-doc-2.6.22.tar.gz
URL:	http://linux-net.osdl.org/index.php/Iproute2
Patch4: iproute2-2.6.25-segfault.patch
Patch5: iproute2-sharepath.patch
Patch6: iproute2-2.6.38-noarpd.patch
License: GPLv2+
BuildRequires: flex  psutils db4-devel bison
# introduction new iptables (xtables) which broke ipt
Conflicts:      iptables < 1.4.1

%description
The iproute package contains networking utilities (ip and rtmon, for
example) which are designed to use the advanced networking
capabilities of the Linux 2.4.x and 2.6.x kernel.

%package doc
Summary: IP and tc documentation with examples
Group:  Applications/System
License: GPLv2+

%description doc
The iproute documentation contains howtos and examples of settings.

%prep
%setup -q -n iproute2-%{version}
%patch4 -p1 -b .seg
%patch5 -p1 -b .share
%patch6 -p1 -b .noarpd

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
%doc %{_mandir}/man8/*
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*
%{_sbindir}/*
%dir %{_datadir}/tc
%{_datadir}/tc/*

%files doc
%defattr(-,root,root,-)
%doc README README.decnet README.iproute2+tc README.distribution README.lnstat
%doc examples
%doc RELNOTES
%dir %{_sysconfdir}/sysconfig/cbq
%config(noreplace) %{_sysconfdir}/sysconfig/cbq/*

