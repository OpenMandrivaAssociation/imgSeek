%define name imgSeek
%define version 0.8.6
%define release %mkrel 6

Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Summary: Photo collection manager and viewer with content-based query
License: 	GPL
Group:		Graphics
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url: 		http://imgseek.sourceforge.net/
Source0: 	http://downloads.sourceforge.net/imgseek/%{name}-%{version}.tar.bz2
Patch1:     imgseek-0.8.6-ImageDB-name-change.patch
Patch2:     imgseek-0.8.6-lib64.patch
Patch3:     imgSeek-0.8.6-fix-missing-header.patch
Requires: 	python-qt >= 3.4
Requires: 	python-imaging
Requires: 	libjpeg-progs
BuildRequires:	python-qt
BuildRequires:	python-devel
BuildRequires:	qt3-devel

%description
imgSeek is a photo collection manager and viewer with content-based search 
and many other features. The query is expressed either as a rough sketch 
painted by the user or as another image you supply (or an image in your 
collection).

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
rm -rf distutils

%build
export QTDIR=%qt3dir
env CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --root=%{buildroot}

cd imgSeekLib/
g++ -DNDEBUG -fPIC -I%qt3dir/include -I%{_includedir}/python%{pyver}/ -c imgdb.cpp -o imgdb.o
g++ -DNDEBUG -fPIC -I%qt3dir/include -I%{_includedir}/python%{pyver}/ -c haar.cpp -o haar.o
g++ -shared imgdb.o haar.o -L%qt3dir/%_lib -lqt-mt -o imgdb.so 

%__cp imgdb.so %buildroot%{py_platsitedir}
cd -

#menu
mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Categories=Graphics;Viewer;
Name=ImgSeek
Comment=ImgSeek Photo Manager
Exec=%{_bindir}/%{name}
Icon=%{name}
EOF

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/applications/mandriva-%{name}.desktop
%doc ChangeLog README THANKS AUTHORS
%{_bindir}/*
%{_datadir}/%{name}
%{py_platsitedir}/imgSeekLib
%{py_platsitedir}/imgSeek-*.egg-info
%{py_platsitedir}/imgdb.so
