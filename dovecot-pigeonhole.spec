#
%bcond_without	tests
#
%define	dovecot_series		2.3
%define	pigeonhole_version	0.5.17
Summary:	Sieve plugin for dovecot
Summary(pl.UTF-8):	Wtyczka Sieve i Managesieve dla dovecota
Name:		dovecot-pigeonhole
Version:	%{dovecot_series}_%{pigeonhole_version}
Release:	1
License:	LGPL
Group:		Daemons
Source0:	https://pigeonhole.dovecot.org/releases/%{dovecot_series}/dovecot-%{dovecot_series}-pigeonhole-%{pigeonhole_version}.tar.gz
# Source0-md5:	b694322af9d54ca8cfaf857bb8d69b12
URL:		http://pigeonhole.dovecot.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
#BuildRequires:	dovecot-devel >= 1:%{dovecot_series}
BuildRequires:	dovecot-devel >= 1:2.3.13
BuildRequires:	flex
BuildRequires:	libtool
%requires_eq_to	dovecot dovecot-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define skip_post_check_so	libdovecot-sieve.so.0.0.0

%description
Dovecot Pigeonhole is implementation of Sieve for Dovecot v2.x

%description -l pl.UTF-8
Dovecot Pigeonhole jest implementacją Sieve dla Dovecot v2.x

%package devel
Summary:	Libraries and headers for %{name}
Summary(pl.UTF-8):	Pliki nagłówkowe dla %{name}
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
This package contains development files for linking against %{name}.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki rozwoju łączenia %{name}.

%package -n dovecot-managesieve
Summary:	Manage Sieve daemon for dovecot
Summary(pl.UTF-8):	Manage Sieve demon dla dovecot
Group:		Daemons

%description -n dovecot-managesieve
Manage Sieve daemon for dovecot.

%description -n dovecot-managesieve -l pl.UTF-8
Ten pakiet zawiera demona Manage Sieve dla dovecot.

%prep
%setup -q -n dovecot-%{dovecot_series}-pigeonhole-%{pigeonhole_version}

%build
%configure \
	ac_cv_path_VALGRIND=reject \
	--with-dovecot=%{_libdir}/dovecot \
	--with-managesieve=yes \
	--prefix=%{_libdir}/dovecot

%{__make}

%{?with_tests:%{__make} -j1 check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir}/dovecot/ -name '*.la' | xargs rm -f
find $RPM_BUILD_ROOT%{_libdir}/dovecot/ -name '*.a' | xargs rm -f

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/example-config/conf.d/90-sieve.conf
%doc doc/extensions
%attr(755,root,root) %{_bindir}/sieve-test
%attr(755,root,root) %{_bindir}/sieve-filter
%attr(755,root,root) %{_bindir}/sievec
%attr(755,root,root) %{_bindir}/sieve-dump
%attr(755,root,root) %{_libdir}/dovecot/plugins/lib90_sieve_plugin.so
%attr(755,root,root) %{_libdir}/dovecot/libdovecot-sieve.so*
%attr(755,root,root) %{_libdir}/dovecot/plugins/lib95_imap_filter_sieve_plugin.so
%attr(755,root,root) %{_libdir}/dovecot/plugins/lib95_imap_sieve_plugin.so
%attr(755,root,root) %{_libdir}/dovecot/plugins/doveadm/lib10_doveadm_sieve_plugin.so
%dir %{_libdir}/dovecot/plugins/settings
%attr(755,root,root) %{_libdir}/dovecot/plugins/settings/libpigeonhole_settings.so
%dir  %{_libdir}/dovecot/plugins/sieve
%attr(755,root,root) %{_libdir}/dovecot/plugins/sieve/lib90_sieve_extprograms_plugin.so
%attr(755,root,root) %{_libdir}/dovecot/plugins/sieve/lib90_sieve_imapsieve_plugin.so

%{_mandir}/man1/doveadm-sieve.1*
%{_mandir}/man1/sieve-test.1*
%{_mandir}/man1/sieve-filter.1*
%{_mandir}/man1/sievec.1*
%{_mandir}/man1/sieved.1*
%{_mandir}/man1/sieve-dump.1*
%{_mandir}/man7/pigeonhole.7*

%files devel
%defattr(644,root,root,755)
%{_aclocaldir}/dovecot-pigeonhole.m4
%dir %{_includedir}/dovecot/sieve
%{_includedir}/dovecot/sieve/*.h

%files -n dovecot-managesieve
%defattr(644,root,root,755)
%doc doc/example-config/conf.d/20-managesieve.conf
%attr(755,root,root) %{_libexecdir}/dovecot/managesieve
%attr(755,root,root) %{_libexecdir}/dovecot/managesieve-login
%{_libdir}/dovecot/plugins/settings/libmanagesieve_login_settings.so
%{_libdir}/dovecot/plugins/settings/libmanagesieve_settings.so
