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

Name: python-%{upname}
Version: 0.8.4
Release: 2%{?dist}
Summary: Lightweight pipelining: using Python functions as pipeline jobs
License: BSD

URL: http://pythonhosted.org/joblib
Source0: https://pypi.python.org/packages/source/j/joblib/joblib-%{version}.tar.gz
BuildArch: noarch
BuildRequires: numpy python-nose python2-devel
# Required by doctests
BuildRequires: python-setuptools python-sphinx
Requires: numpy

%description
%{common_description}

%if 0%{?with_python3}
%package -n python3-joblib
Summary: Lightweight pipelining: using Python functions as pipeline jobs

BuildRequires: python3-numpy python3-nose python3-devel
# Required by doctests
BuildRequires: python3-setuptools python3-sphinx
Requires: python3-numpy

%description -n python3-joblib
%{common_description}
%endif # 0%{?with_python3}

%prep
%setup -qn %{upname}-%{version}
rm -rf %{upname}.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

# Fix failing testsuite, executable files are skipped
chmod +x %{py3dir}/doc/sphinxext/autosummary_generate.py
%endif # 0%{?with_python3}

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build
%{__python2} setup.py build
%{__python2} setup.py build_sphinx
rm -f build/sphinx/html/.buildinfo

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
# The doc system is not compatible with python3
popd
%endif # 0%{?with_python3}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
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

%files
%doc build/sphinx/html README*
%{python2_sitelib}/%{upname}
%{python2_sitelib}/%{upname}-%{version}-py%{python2_version}.egg-info

%if 0%{?with_python3}
%files -n python3-%{upname}
%doc build/sphinx/html README*
%{python3_sitelib}/%{upname}
%{python3_sitelib}/%{upname}-%{version}-py%{python3_version}.egg-info
%endif # 0%{?with_python3}


%changelog
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
