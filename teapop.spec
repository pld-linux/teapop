#
# Conditional build:
%bcond_without	mysql	# disable mySQL support
%bcond_without	pgsql	# disable PostreSQL support
%bcond_without	ldap	# disable OpenLDAP support
%bcond_without	whoson	# disable whoson support
%bcond_without	ipv6	# disable IPv6 support
#
Summary:	Teapop is a POP3-server with flexible virtual domain support
Summary(pl.UTF-8):	Serwer POP3 ze wsparciem dla wirtualnych domen
Name:		teapop
Version:	0.3.8
Release:	12
License:	GPL
Group:		Networking/Daemons/POP3
Source0:	http://www.toontown.org/pub/teapop/%{name}-%{version}.tar.gz
# Source0-md5:	c322c20018663a1a9b7860966cbd4ed2
Source1:	%{name}.inetd
Patch0:		%{name}-x86_64.patch
Patch1:		%{name}-openldap-2.3.patch
URL:		http://www.toontown.org/teapop/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
%{?with_whoson:BuildRequires:	whoson-devel}
Requires:	rc-inetd
Provides:	pop3daemon
Obsoletes:	pop3daemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Teapop is yet another RFC1939 compliant POP3-server. The flexible
virtual domain support is what distinguish Teapop from all other
POP3-servers.

%description -l pl.UTF-8
Teapop to jeszcze jeden serwer POP3 zgodny z RFC 1939. Elastyczna
obsługa wirtualnych domen jest tym, co odróżnia Teapop od innych
serwerów POP3.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub config
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
	%{?with_ipv6:--enable-ipv6} \
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
%service -q rc-inetd reload

%postun
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc doc/{TODO,ChangeLog} contrib.tar.gz
%attr(755,root,root) %{_sbindir}/teapop
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/teapop
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/teapop.passwd
%{_mandir}/man8/*
