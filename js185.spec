# NOTE: JavaScript version is 1.8.5, implementation version is 1.0.0; what should be package version?
# Some paths (library name, .pc file) seem intentionally not conflict with js < 1.8,
# but some still do (includes path, js-config, js shell).
# It's somehow messy, so let's put this version in separate js185 package for now,
# until upstream decides which way to go in the future.
Summary:	SpiderMonkey JavaScript 1.8.5 implementation
Summary(pl.UTF-8):	Implementacja SpiderMonkey języka JavaScript 1.8.5
Name:		js185
Version:	1.0.0
Release:	2
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/%{name}-%{version}.tar.gz
# Source0-md5:	a4574365938222adca0a6bd33329cb32
Patch0:		%{name}-install.patch
URL:		http://www.mozilla.org/js/
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 4.7.0
BuildRequires:	perl-base >= 1:5.6
BuildRequires:	python >= 1:2.5
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.294
BuildRequires:	sed >= 4.0
Requires:	nspr >= 4.7.0
%ifarch %{x8664} ia64 ppc64 s390x sparc64
Provides:	libjs.so.1()(64bit)
%else
Provides:	libjs.so.1
%endif
Provides:	js = 2:1.8.5
Obsoletes:	js < 2:1.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JavaScript Reference Implementation (codename SpiderMonkey). The
package contains JavaScript runtime (compiler, interpreter,
decompiler, garbage collector, atom manager, standard classes) and
small "shell" program that can be used interactively and with .js
files to run scripts.

%description -l pl.UTF-8
Wzorcowa implementacja JavaScriptu (o nazwie kodowej SpiderMonkey).
Pakiet zawiera środowisko uruchomieniowe (kompilator, interpreter,
dekompilator, odśmiecacz, standardowe klasy) i niewielką powłokę,
która może być używana interaktywnie lub z plikami .js do uruchamiania
skryptów.

%package devel
Summary:	Header files for JavaScript reference library
Summary(pl.UTF-8):	Pliki nagłówkowe do biblioteki JavaScript
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	nspr-devel >= 4.7.0
Provides:	js-devel = 2:1.8.5
Obsoletes:	js-devel < 2:1.8

%description devel
Header files for JavaScript reference library.

%description devel -l pl.UTF-8
Pliki nagłówkowe do biblioteki JavaScript.

%package static
Summary:	Static JavaScript reference library
Summary(pl.UTF-8):	Statyczna biblioteka JavaScript
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	js-static = 2:1.8.5
Obsoletes:	js-static < 2:1.8

%description static
Static version of JavaScript reference library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki JavaScript.

%prep
%setup -q -n js-1.8.5
%patch0 -p1

sed -i -e 's/-O3//' js/src/Makefile.in js/src/config/Makefile.in

%build
cd js/src
%configure2_13 \
	--enable-readline \
	--enable-threadsafe \
	--with-system-nspr

%{__make} \
	HOST_OPTIMIZE_FLAGS= \
	MOZILLA_VERSION=%{version}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C js/src install \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZILLA_VERSION=%{version}

# not installed by make install in new buildsystem
install js/src/shell/js js/src/jscpucfg $RPM_BUILD_ROOT%{_bindir}

# provide libjs.so for backward compability
ln -sf libmozjs185.so $RPM_BUILD_ROOT%{_libdir}/libjs.so
ln -sf libmozjs185.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}/libjs.so.1.0.0
ln -sf libmozjs185.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}/libjs.so.1
ln -sf libmozjs185-1.0.a $RPM_BUILD_ROOT%{_libdir}/libjs.a

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc js/src/README.html
%attr(755,root,root) %{_bindir}/js
%attr(755,root,root) %{_libdir}/libjs.so.*.*.*
# NOTE: it's alternative symlink, created in PLD, so must be packaged
%attr(755,root,root) %{_libdir}/libjs.so.1
%attr(755,root,root) %{_libdir}/libmozjs185.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmozjs185.so.1.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/js-config
%attr(755,root,root) %{_bindir}/jscpucfg
%attr(755,root,root) %{_libdir}/libjs.so
%attr(755,root,root) %{_libdir}/libmozjs185.so
%{_includedir}/js
%{_pkgconfigdir}/mozjs185.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libjs.a
%{_libdir}/libmozjs185-1.0.a
