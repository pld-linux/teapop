#
# Conditional build:
# _with_mysql		enable mySQL support
# _without_pgsql	disable PostreSQL support
#
Summary:	Teapop is a POP3-server with flexible virtual domain support
Summary(pl):	Serwer POP3 ze wsparciem dla wirtualnych domen
Name:		teapop
Version:	0.3.7
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.toontown.org/pub/teapop/%{name}-%{version}.tar.gz
# Source0-md5:	0e67030968e48e4307df854d433cc6f4
Source1:	%{name}.inetd
%{?_with_mysql:BuildRequires:	mysql-devel}
%{!?_without_pgsql:BuildRequires:	postgresql-devel}
URL:		http://www.toontown.org/teapop/
Prereq:		rc-inetd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Teapop is yet another RFC1939 compliant POP3-server. The flexible
virtual domain support is what distinguish Teapop from all other
POP3-servers.

%description -l pl
Teapop to jeszcze jeden serwer POP3 zgodny z RFC 1939. Elastyczna
obs³uga wirtualnych domen jest tym, co ró¿ni Teapop od innych serwerów
POP3.

%prep
%setup -q

%build
cd config
rm -f configure
%{__autoconf}
%configure \
	--enable-flock \
	--enable-extra-dividers=:%! \
	%{?_with_mysql:--with-mysql=/usr} \
	%{!?_without_pgsql:--with-pgsql=/usr}
cd ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc/sysconfig/rc-inetd,%{_sbindir},%{_mandir}/man8}

install teapop/teapop		$RPM_BUILD_ROOT%{_sbindir}
install man/teapop.8		$RPM_BUILD_ROOT%{_mandir}/man8
install etc/teapop.passwd	$RPM_BUILD_ROOT%{_sysconfdir}/teapop.passwd

install %{SOURCE1}		$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/teapop

tar czf contrib.tar.gz contrib/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi

%files
%defattr(644,root,root,755)
%doc doc/{TODO,ChangeLog} contrib.tar.gz
%attr(755,root,root) %{_sbindir}/teapop
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/teapop
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/teapop.passwd
%{_mandir}/man8/*
