#
# Conditional build:
%bcond_without mysql	# disable mySQL support
%bcond_without pgsql	# disable PostreSQL support
%bcond_without ldap	# disable OpenLDAP support
%bcond_without whoson	# disable whoson support
#
Summary:	Teapop is a POP3-server with flexible virtual domain support
Summary(pl):	Serwer POP3 ze wsparciem dla wirtualnych domen
Name:		teapop
Version:	0.3.8
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.toontown.org/pub/teapop/%{name}-%{version}.tar.gz
# Source0-md5:	c322c20018663a1a9b7860966cbd4ed2
Source1:	%{name}.inetd
URL:		http://www.toontown.org/teapop/
BuildRequires:	autoconf
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{?with_ldap:BuildRequires:	openldap-devel}
%{?with_whoson:BuildRequires:	whoson-devel}
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
sed -i -e 's#\.a#\.so#g' configure.in
rm -f configure
%{__autoconf}
%configure \
	%{?with_mysql:--with-mysql=/usr} \
	%{?with_pgsql:--with-pgsql=/usr} \
	%{?with_ldap:--with-ldap=openldap} \
	%{?with_whoson:--with-whoson=/usr} \
	--enable-flock \
	--enable-ipv6 \
	--enable-extra-dividers=":%!"
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
