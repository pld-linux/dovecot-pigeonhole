
%define	dovecot_series		2.0
%define	pigeonhole_version	0.2.1


Summary:	Sieve plugin for dovecot
Summary(pl.UTF-8):	Wtyczka Sieve i Managesieve dla dovecota
Name:		dovecot-pigeonhole
Version:	%{dovecot_series}_%{pigeonhole_version}
Release:	1
License:	LGPL
Group:		Daemons
Source0:	http://www.rename-it.nl/dovecot/%{dovecot_series}/dovecot-%{dovecot_series}-pigeonhole-%{pigeonhole_version}.tar.gz
# Source0-md5:	7baf6ebac21bdb865cb733d8e96ee81b
Patch0:		%{name}-config.patch
URL:		http://www.dovecot.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	dovecot-devel >= 1:2.0
BuildRequires:	flex
BuildRequires:	libtool
%requires_eq_to	dovecot dovecot-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define skip_post_check_so	libdovecot-sieve.so.0.0.0

%description
Dovecot Pigeonhole is implementation of Sieve and Managesieve for
Dovecot v2.

%description -l pl.UTF-8
Dovecot Pigeonhole jest implementacją Sieve i Managesieve dla Dovecot
v2.

%package devel
Summary:	Libraries and headers for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
This package contains development files for linking against %{name}.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki rozwoju łączenia %{name}.

%package -n dovecot-managesieve
Summary:	Manage Sieve daemon for dovecot
Group:		Daemons

%description -n dovecot-managesieve
This package provides the Manage Sieve daemon for dovecot.


%prep
%setup -q -n dovecot-%{dovecot_series}-pigeonhole-%{pigeonhole_version}
%patch0 -p1

%build

%configure \
		--with-dovecot=%{_libdir} \
		--with-managesieve=yes \
		--enable-header-install=yes \
		--prefix=%{_libdir}/dovecot

%{__make}

%install

rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

#remove the libtool archives
find $RPM_BUILD_ROOT%{_libdir}/dovecot/ -name '*.la' | xargs rm -f
find $RPM_BUILD_ROOT%{_libdir}/dovecot/ -name '*.a' | xargs rm -f


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(644,root,root,755)

%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sieve-test
%attr(755,root,root) %{_bindir}/sievec
%attr(755,root,root) %{_bindir}/sieve-dump
%{_libdir}/dovecot/plugins/lib90_sieve_plugin.so
%attr(755,root,root) %{_libdir}/dovecot/libdovecot-sieve.so*

%{_mandir}/man1/sieve-test.1*
%{_mandir}/man1/sievec.1*
%{_mandir}/man1/sieved.1*
%{_mandir}/man1/sieve-dump.1*
%{_mandir}/man7/pigeonhole.7*
%{_docdir}/dovecot/example-config/conf.d/90-sieve.conf
%{_docdir}/dovecot/sieve

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/dovecot/sieve
%{_includedir}/dovecot/sieve/*.h

%files -n dovecot-managesieve
%defattr(644,root,root,755)
%dir %{_libdir}/dovecot/plugins/settings/
%{_libdir}/dovecot/plugins/settings/libmanagesieve_login_settings.so
%{_libdir}/dovecot/plugins/settings/libmanagesieve_settings.so
%{_libexecdir}/dovecot/managesieve
%{_libexecdir}/dovecot/managesieve-login
%{_docdir}/dovecot/example-config/conf.d/20-managesieve.conf
