# Is Python3 available?
%if 0%{?fedora} >= 13 || 0%{?rhel} >= 8
%global with_python3 1
%endif # 0%{?fedora} >= 13 || 0%{?rhel} >= 8

%global upname joblib

%global common_description						\
Joblib is a set of tools to provide lightweight pipelining in Python.	\
In particular, joblib offers:						\
 * transparent disk-caching of the output values and lazy		\
   re-evaluation (memorize pattern)					\
 * easy simple parallel computing					\
 * logging and tracing of the execution

Name:           python-%{upname}
Version:        0.9.3
Release:        1%{?dist}
Summary:        Lightweight pipelining: using Python functions as pipeline jobs
License:        BSD

URL:            http://pythonhosted.org/joblib
Source0:        https://github.com/joblib/joblib/archive/%{version}/%{upname}-%{version}.tar.gz
BuildArch:      noarch

%description
%{common_description}

%package -n python2-%{upname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{upname}}
%if 0%{?fedora} > 23
BuildRequires:  python2-numpy
%else
BuildRequires:  numpy
%endif
BuildRequires:  python2-nose python2-devel
# Required by doctests
BuildRequires:  python2-setuptools python-sphinx
%if 0%{?fedora} > 23
Requires:       python2-numpy
%else
Requires:       numpy
%endif

%description -n python2-%{upname}
%{common_description}

Python 2 version.

%if 0%{?with_python3}
%package -n python3-joblib
Summary:        Lightweight pipelining: using Python functions as pipeline jobs
%{?python_provide:%python_provide python2-%{upname}}
BuildRequires:  python3-numpy python3-nose python3-devel
# Required by doctests
BuildRequires:  python3-setuptools python3-sphinx
Requires:       python3-numpy

%description -n python3-joblib
%{common_description}

Python 3 version.
%endif # 0%{?with_python3}

%prep
%setup -qc
mv %{upname}-%{version} python2

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # 0%{?with_python3}

find python2 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%build
pushd python2
  %py2_build
  %{__python2} setup.py build_sphinx
  rm -f build/sphinx/html/.buildinfo
popd

%if 0%{?with_python3}
pushd python3
  %py3_build
  # The doc system is not compatible with python3
popd
%endif # 0%{?with_python3}

%install
pushd python2
  %py2_install
popd

%if 0%{?with_python3}
pushd python3
  %py3_install
popd
%endif # 0%{?with_python3}

%check
pushd %{buildroot}/%{python2_sitelib}
  nosetests-%{python2_version} -v
popd

%if 0%{?with_python3}
pushd %{buildroot}/%{python3_sitelib}
  nosetests-%{python3_version} -v
popd
%endif # 0%{?with_python3}

%files -n python2-%{upname}
%doc python2/build/sphinx/html python2/README.rst
%doc python2/examples
%{python2_sitelib}/%{upname}*

%if 0%{?with_python3}
%files -n python3-%{upname}
%doc python2/build/sphinx/html python3/README.rst
%doc python3/examples
%{python3_sitelib}/%{upname}*
%endif # 0%{?with_python3}

%changelog
* Mon Nov 23 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.9.3-1
- Update to 0.9.3 (RHBZ #1236575)
- Modernize spec

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.4-1
- New upstream release (0.8.4)

* Wed Sep 03 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.3-1
- New upstream release (0.8.3)

* Wed Jul 02 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.2-1
- New upstream release (0.8.2)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.0-2
- Reverted stylistic changes
- Run checks on installed files
- Use tarball from PyPI

* Mon Jun 02 2014 Björn Esser <bjoern.esser@gmail.com> - 0.8.0-1
- new stable upstream
- restructured spec-file
- include README from src-tarball in %%doc
- updated python2-macros
- make testsuite a bit more verbose
- preserve timestamps of modified files
- use tarball from github-tags

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
