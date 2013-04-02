#
# Conditional build:
%bcond_without	tests		# build without tests

%include	/usr/lib/rpm/macros.java
Summary:	SIGAR - System Information Gatherer And Reporter
Summary(pl.UTF-8):	SIGAR - narzędzie do zbierania i raportowania informacji systemowych
Name:		sigar
Version:	1.6.5
Release:	2
License:	Apache v2.0
Group:		Libraries
Source0:	%{name}-%{version}-58097d9.tbz2
# Source0-md5:	a8dfe38ed914a364943f746489b79539
URL:		http://sigar.hyperic.com/
BuildRequires:	ant >= 1.6.5
BuildRequires:	cmake
BuildRequires:	jdk >= 1.3
BuildRequires:	perl-base >= 5.6.1
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Sigar API provides a portable interface for gathering system
information such as:
- System memory, swap, CPU, load average, uptime, logins
- Per-process memory, CPU, credential info, state, arguments,
  environment, open files
- File system detection and metrics
- Network interface detection, configuration info and metrics
- Network route and connection tables

This information is available in most operating systems, but each OS
has their own way(s) providing it. SIGAR provides developers with one
API to access this information regardless of the underlying platform.
The core API is implemented in pure C with bindings currently
implemented for Java, Perl and C#.

%description -l pl.UTF-8
Sigar API udostępnia przenośny interfejs do zbierania informacji
systemowych, takich jak:
- systemowa pamięć, swap, procesor, obciążenie, czas pracy, logowania
- informacje dla procesów: pamięć, wykorzystanie procesora,
  uprawnienia, stan, argumenty, środowisko, otwarte pliki
- wykrywanie i pomiary systemów plików
- wykrywanie informacji sieciowych, informacje o konfiguracji i
  pomiary
- tablice tras i połączeń sieciowych

Informacje te są dostępne w większości systemów operacyjnych, ale
każdy system ma własny sposób udostępniania ich. SIGAR udostępnia
programistom jedno API pozwalające na dostęp dotych informacji
niezależnie od platformy. Podstawowe API jest zaimplementowane w
czystym C, z wiązaniami dla Javy, Perla i C#.

%package devel
Summary:	SIGAR Development package - System Information Gatherer And Reporter
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for developing against the Sigar API

%package -n java-%{name}
Summary:	Java bindings to sigar library
Group:		Libraries/Java
# does not use base library

%description -n java-%{name}
Java bindings to Sigar library.

%prep
%setup -q

%{__sed} -i -e 's,DESTINATION lib$,DESTINATION %{_lib},' src/CMakeLists.txt

%build
install -d build
cd build
%cmake ..
%{__make}

cd ../bindings/java
%ant
chmod a+rx sigar-bin/lib/lib*.so

%if %{with tests}
%java -jar sigar-bin/lib/sigar.jar test
%endif
cd ../..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_javadir}
install -p bindings/java/sigar-bin/lib/libsigar-*-*.so $RPM_BUILD_ROOT%{_libdir}
cp -p bindings/java/sigar-bin/lib/sigar.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

%clean
rm -rf $RPM_BUILD_ROOT

# no SONAME, but run ldconfig to update ld.so.cache
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n java-%{name} -p /sbin/ldconfig
%postun	-n java-%{name} -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NOTICE README
%attr(755,root,root) %{_libdir}/libsigar.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/sigar*.h

%files -n java-%{name}
%defattr(644,root,root,755)
%{_javadir}/sigar-%{version}.jar
%{_javadir}/sigar.jar
%attr(755,root,root) %{_libdir}/libsigar-*-*.so
