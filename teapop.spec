Summary:	Teapop is a RFC1939 compliant POP3-server, with flexible virtual domain support 
Name:		teapop
Version:	0.28
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://www.toontown.org/pub/teapop/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Patch0:		%{name}-configure.patch
%{?_with_mysql:BuildRequires: mysql-devel}
%{!?_without_pgsql:BuildRequires: postgresql-devel}
URL:		http://www.toontown.org/teapop/
Prereq:		rc-inetd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Teapop is yet another RFC1939 compliant POP3-server. The flexible
virtual domain support is what distinguish Teapop from all other
POP3-servers.


%prep
%setup -q
%patch0 -p1
%build
(cd config; autoconf)
%configure  \
	--enable-flock \
	--enable-extra-dividers=:%! \
        %{?_with_mysql:--with-mysql=/usr} \
        %{!?_without_pgsql:--with-pgsql=/usr}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/sysconfig/rc-inetd,%{_sbindir},%{_mandir}/man8}

install teapop/teapop		$RPM_BUILD_ROOT%{_sbindir}
install man/teapop.8		$RPM_BUILD_ROOT%{_mandir}/man8
install etc/teapop.passwd	$RPM_BUILD_ROOT%{_sysconfdir}/teapop.passwd

install %{SOURCE1}		$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/teapop

gzip -9nf doc/{TODO,ChangeLog}

%post
%rc_inetd_post

%postun
%rc_inetd_postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{TODO,ChangeLog}.gz
%attr(755,root,root) %{_sbindir}/teapop
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/rc-inetd/teapop
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/teapop.passwd
%{_mandir}/man8/*
