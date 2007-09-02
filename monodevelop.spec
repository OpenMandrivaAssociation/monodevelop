%define name monodevelop
%define version 0.15
%define svn 1949
%define release %mkrel 2
%define gtksharp 1.9.5
%define gtksourceview 0.10
%define gecko 0.10
%define monodoc 1.0
%if %mdkversion >= 200600
%define pkgconfigdir %_datadir/pkgconfig
%else
%define pkgconfigdir %_libdir/pkgconfig
%endif
%define mozver %(rpm -q --queryformat %%{VERSION} mozilla-firefox)

Summary: Full-featured IDE for mono and Gtk#
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://go-mono.com/sources/monodevelop/%{name}-%{version}.tar.bz2
Patch: monodevelop-0.9-xvt.patch
Patch1: monodevelop-0.12-firefox.patch
#gw #30828: use libapr1 by default
Patch2: monodevelop-0.14-noapr0.patch
#gw from svn: fix build with new boo
Patch3: monodevelop-85179-new-boo.patch
Patch4: monodevelop-desktop-entry.patch
URL: http://www.monodevelop.com/
License: GPL
Group: Development/Other
Requires: gecko-sharp2 >= %gecko
Requires: gtksourceview-sharp >= %gtksourceview
Requires: gnome-sharp2 >= %gtksharp
Requires: glade-sharp2 >= %gtksharp
Requires: monodoc >= %monodoc
Requires: shared-mime-info
Requires: libmozilla-firefox = %mozver
Requires: ikvm
BuildRequires: boo >= 0.7.6
BuildRequires: ikvm
# gw our nemerle is too old
#BuildRequires: nemerle
BuildRequires: mono-devel
BuildRequires: gecko-sharp2 >= %gecko
BuildRequires: gtksourceview-sharp >= %gtksourceview
BuildRequires: gnome-sharp2 >= %gtksharp
BuildRequires: glade-sharp2 >= %gtksharp
BuildRequires: jscall-sharp zip
BuildRequires: monodoc >= %monodoc
BuildRequires: mono-data-sqlite
#BuildRequires: libmono-debugger-devel >= 0.12
BuildRequires: apache-mod_mono
BuildRequires: mozilla-firefox-devel
BuildRequires: perl-XML-Parser
BuildRequires: ImageMagick
#BuildRequires: desktop-file-utils
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Requires(post): desktop-file-utils shared-mime-info
Requires(postun): desktop-file-utils shared-mime-info

%description 
This is MonoDevelop which is intended to be a full-featured
integrated development environment (IDE) for mono and Gtk#.
It was originally a port of SharpDevelop 0.98.

%prep
%setup -q
%patch -p1 -b .xvt
%patch1 -p1 -b .firefox
%patch2 -p1 -b .noapr0
%patch3 -p2
%patch4 -p1
cp %_prefix/lib/jscall-sharp/* Extras/AspNetEdit/libs/

%build
./configure --prefix=%_prefix --libdir=%_libdir --enable-java --enable-versioncontrol --enable-boo --enable-aspnet --enable-subversion --enable-aspnetedit
#--enable-nemerle 
#--enable-debugger
make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
mkdir -p %{buildroot}/`monodoc --get-sourcesdir` %buildroot%_libdir/firefox-%mozver/chrome
%makeinstall_std UPDATE_MIME_DB="#" pkgconfigdir=%pkgconfigdir packagedir=%buildroot%_prefix/lib/monodevelop/AddIns/AspNetEdit MOZILLA_HOME=%buildroot%_libdir/firefox-%mozver/
#gw fix mozilla-firefox directory
perl -pi -e "s^xMOZVERx^%mozver^g" %buildroot%_bindir/monodevelop

# menu
mkdir -p %{buildroot}/%{_menudir}
cat > %{buildroot}/%{_menudir}/%{name} <<EOF
?package(%{name}): \
command="%{_bindir}/monodevelop" \
title="MonoDevelop" \
longtitle="Full-featured IDE for mono and Gtk#" \
%if %mdkversion <= 1000
section="More applications/Development/Development environments" \
%else
section="More Applications/Development/Development Environments" \
%endif
needs="x11" \
icon="monodevelop.png" \
startup_notify="yes" xdg="true"
EOF

#icons
mkdir -p %buildroot{%_liconsdir,%_iconsdir,%_miconsdir}
ln -s %_datadir/pixmaps/%name.png %buildroot%_liconsdir/
convert -scale 32x32 %name.png %buildroot%_iconsdir/%name.png
convert -scale 16x16 %name.png %buildroot%_miconsdir/%name.png

%find_lang %name

ln -sf %_prefix/lib/jscall-sharp/jscall.dll  %buildroot%{_prefix}/lib/monodevelop/AddIns/AspNetEdit

%post
%update_mime_database
%update_desktop_database
%update_menus

%postun
%clean_mime_database
%clean_desktop_database
%clean_menus

%files -f %name.lang
%defattr(-,root,root) 
%doc AUTHORS ChangeLog README 
%{_bindir}/mdtool
%{_bindir}/monodevelop
%{_menudir}/%{name}
%{_prefix}/lib/monodevelop/
%_libdir/firefox-%mozver/chrome/aspdesigner.manifest
%{_datadir}/applications/monodevelop.desktop
%{_datadir}/mime/packages/monodevelop.xml
%{_datadir}/pixmaps/monodevelop.png
%pkgconfigdir/monodevelop.pc
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png

%clean
rm -rf $RPM_BUILD_ROOT
