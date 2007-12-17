%define name imgSeek
%define version 0.8.4
%define release %mkrel 2

Summary: Photo collection manager and viewer with content-based query
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	%{name}-%{version}.tar.bz2
Patch0:     imgSeek-0.8.4-sizetype.patch 
License: 	GPL
Group:		Graphics
Requires: 	PyQt >= 3.4
Requires: 	python-imaging
Requires: 	libjpeg-progs
BuildRequires:	PyQt
BuildRequires:	python-devel
BuildRequires:	ImageMagick
BuildRequires:	qt3-devel
Url: 		http://imgseek.sourceforge.net/

%description
imgSeek is a photo collection manager and viewer with content-based search 
and many other features. The query is expressed either as a rough sketch 
painted by the user or as another image you supply (or an image in your 
collection).

%prep
%setup -q
%patch -p0
%build

env CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

#icons
install -d -m755 %{buildroot}/{%{_miconsdir},%{_liconsdir}}
install -m644 %{name}.png %{buildroot}/%{_iconsdir}/
install -m644 %{name}.png %{buildroot}/%{_liconsdir}/
convert -resize 16x16 %{name}.png %{buildroot}/%{_miconsdir}/%{name}.png

#menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat <<EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): \
needs="x11" \
section="Multimedia/Graphics" \
title="ImgSeek" \
longtitle="ImgSeek Photo Manager" \
command="%{_bindir}/%{name}" needs="X11" \
icon="%{name}.png"
EOF

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%doc ChangeLog README THANKS AUTHORS

