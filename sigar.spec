#
# Conditional build:
%bcond_without	tests		# build without tests
#
# TODO
# - clarify license -- COPYING in sources is gplv2 but on homepage link is to gplv3
Summary:	SIGAR - System Information Gatherer And Reporter
Name:		sigar
Version:	1.4.0.0
Release:	0.1
License:	GPL v3
Group:		Libraries
Source0:	http://dl.sourceforge.net/sigar/hyperic-%{name}-%{version}-src.tar.gz
# Source0-md5:	0e3718c99c183f194578ba39cf207a65
Source1:	http://jan.kneschke.de/assets/2007/2/16/hyperic-%{name}-1.3.0.0-src-cmake.tar.gz
URL:		http://sigar.hyperic.com/
BuildRequires:	ant >= 1.6.5
BuildRequires:	cmake
BuildRequires:	jdk >= 1.3
BuildRequires:	perl-base >= 5.6.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Sigar API provides a portable interface for gathering system
information such as:
- System memory, swap, cpu, load average, uptime, logins
- Per-process memory, cpu, credential info, state, arguments,
  environment, open files
- File system detection and metrics
- Network interface detection, configuration info and metrics
- Network route and connection tables

This information is available in most operating systems, but each OS
has their own way(s) providing it. SIGAR provides developers with one
API to access this information regardless of the underlying platform.
The core API is implemented in pure C with bindings currently
implemented for Java, Perl and C#.


%prep
%setup -q -n hyperic-%{name}-%{version}-src -a1

%build
%cmake .
%{__make}

cd bindings/java
%ant
chmod a+rx sigar-bin/lib/lib*.so

%if %{with tests}
%java -jar sigar-bin/lib/sigar.jar test
%endif
cd ../..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSES README
