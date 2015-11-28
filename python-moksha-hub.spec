#
# Conditional build:
%bcond_with	tests	# do not perform "make test"

%define	module moksha.hub
Summary:	Hub components for Moksha
Name:		python-moksha-hub
Version:	1.4.4
Release:	1
License:	Apache v2.0
Group:		Development/Libraries
Source0:	http://pypi.python.org/packages/source/m/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	97ec72d1fb223de0d883715185b63e06
URL:		http://pypi.python.org/pypi/moksha.hub
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
%if %{with tests}
BuildRequires:	python-TwistedCore
BuildRequires:	python-daemon
BuildRequires:	python-devel
BuildRequires:	python-mock
BuildRequires:	python-moksha-common >= 1.0.6
BuildRequires:	python-nose
BuildRequires:	python-six
BuildRequires:	python-stomper
BuildRequires:	python-txws
BuildRequires:	python-txzmq
BuildRequires:	python-websocket-client
%endif
Requires:	python-TwistedCore
Requires:	python-daemon
Requires:	python-moksha-common >= 1.0.6
Requires:	python-six
Requires:	python-stomper
Requires:	python-txws
Requires:	python-txzmq
# When installed, these enable new plugins for the moksha.hub
#BuildRequires:  python-qpid
#Requires:       python-qpid
# Its a whole different package now.
Conflicts:	moksha < 1.0.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hub components for Moksha.

%prep
%setup -q -n %{module}-%{version}

# Removed twisted from the list of deps in setup.py.
%{__sed} -i 's/"Twisted",//' setup.py

# *Experimental* support for python-zmq-13.0.0 in rawhide.
%{__sed} -i 's/pyzmq<=2.2.0.1/pyzmq/' setup.py

%build
%py_build

%if %{with tests}
%{__python} setup.py test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/moksha/hub/tests

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README COPYING AUTHORS
%attr(755,root,root) %{_bindir}/moksha-hub
%{py_sitescriptdir}/moksha/hub
%{py_sitescriptdir}/moksha.hub-%{version}-py*-nspkg.pth
%{py_sitescriptdir}/moksha.hub-%{version}-py*.egg-info
