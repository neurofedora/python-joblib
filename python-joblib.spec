%global upname joblib
%global upversion 0.8.0a2
%global with_python3 1

Name: python-%{upname}
Version: 0.8.0
Release: 0.2.a2%{?dist}
Summary: Lightweight pipelining: using Python functions as pipeline jobs
License: BSD

Group: Development/Libraries
URL: http://pythonhosted.org/joblib
Source0: https://pypi.python.org/packages/source/j/joblib/joblib-%{upversion}.tar.gz
BuildArch: noarch
BuildRequires: python2-devel python-nose python-sphinx
# Required by doctests
BuildRequires: numpy 
BuildRequires: python-setuptools
Requires: numpy

%description
Joblib is a set of tools to provide lightweight pipelining in Python. 
In particular, joblib offers:
 * transparent disk-caching of the output values and lazy
   re-evaluation (memoize pattern)
 * easy simple parallel computing
 * logging and tracing of the execution

%if 0%{?with_python3}
%package -n python3-joblib
Summary: Lightweight pipelining: using Python functions as pipeline jobs
BuildRequires: python3-devel python3-nose
# Required by doctests
BuildRequires: python3-numpy 
BuildRequires: python3-setuptools
Requires: python3-numpy

%description -n python3-joblib
Joblib is a set of tools to provide lightweight pipelining in Python. 
In particular, joblib offers:
 * transparent disk-caching of the output values and lazy
   re-evaluation (memoize pattern)
 * easy simple parallel computing
 * logging and tracing of the execution
%endif # with_python3

%prep
%setup -n %{upname}-%{upversion} -q
rm -rf %{upname}.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build
%{__python} setup.py build
%{__python} setup.py build_sphinx
rm -f build/sphinx/html/.buildinfo

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
# The doc system not compatible with python3
popd
%endif # with_python3

%check
nosetests
%if 0%{?with_python3}
pushd %{py3dir}
nosetests-%{python3_version}
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root  %{buildroot}
popd
%endif # with_python3

%{__python} setup.py install --skip-build --root  %{buildroot}
 
%files
%doc build/sphinx/html
%{python_sitelib}/%{upname}
%{python_sitelib}/%{upname}-%{upversion}-py2.7.egg-info

%if 0%{?with_python3}
%files -n python3-%{upname}
%doc build/sphinx/html
%{python3_sitelib}/%{upname}
%{python3_sitelib}/%{upname}-%{upversion}-py%{python3_version}.egg-info
%endif # with_python3


%changelog
* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.0-0.2.a2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Jan 09 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.0-0.1.a2
- New upstream prerelease (0.8.0a2)

* Sun Aug 25 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.7.1-2
- Removing upstream egg
- Adding BR python(3)-setuptools

* Sat Aug 24 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.7.1-1
- New upstream version (0.7.1)

* Thu Jul 4 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.7.0d-1
- Adding index.rst before importing

