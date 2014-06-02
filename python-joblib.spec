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

Name:		python-%{upname}
Version:	0.8.0
Release:	1%{?dist}
Summary:	Lightweight pipelining: using Python functions as pipeline jobs

License:	BSD
URL:		http://pythonhosted.org/%{upname}
Source0:	https://github.com/%{upname}/%{upname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	numpy
BuildRequires:	python-nose
BuildRequires:	python2-devel

# Required by doctests
BuildRequires:	python-setuptools
BuildRequires:	python-sphinx

Requires:	numpy

%description
%{common_description}


%if 0%{?with_python3}
%package -n python3-joblib
Summary:	Lightweight pipelining: using Python functions as pipeline jobs

BuildRequires:	python3-devel
BuildRequires:	python3-nose
BuildRequires:	python3-numpy

# Required by doctests
BuildRequires:	python3-setuptools
BuildRequires:	python3-sphinx

Requires:	python3-numpy

%description -n python3-joblib
%{common_description}
%endif # 0%{?with_python3}


%prep
%setup -qn %{upname}-%{version}
rm -rf %{upname}.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
for _file in `find %{py3dir} -type f -name '*.py'`
do
  sed -e '1s|^#!.*python|#!%{__python3}|' < ${_file} > ${_file}.new &&	\
  touch -r ${_file} ${_file}.new &&					\
  mv -f ${_file}.new ${_file}
done

# Fix failing testsuite, executable files are skipped
chmod +x %{py3dir}/doc/sphinxext/autosummary_generate.py
%endif # 0%{?with_python3}

for _file in `find . -type f -name '*.py'`
do
  sed -e '1s|^#!.*python|#!%{__python2}|' < ${_file} > ${_file}.new &&	\
  touch -r ${_file} ${_file}.new &&					\
  mv -f ${_file}.new ${_file}
done


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
%{__python2} setup.py install --skip-build --root  %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root  %{buildroot}
popd
%endif # 0%{?with_python3}


%check
nosetests-%{python2_version} -v

%if 0%{?with_python3}
pushd %{py3dir}
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
