%define name monodevelop
%define version 1.9
%define svn 1949
%define release %mkrel 1
%define gtksharp 1.9.5
%define gtksourceview 0.10
%define monodoc 1.0
%define pkgconfigdir %_datadir/pkgconfig
%if %mdvver < 200900
%define mozver %(rpm -q --queryformat %%{VERSION} mozilla-firefox)
%endif
%define xulrunner 1.9

Summary: Full-featured IDE for mono and Gtk#
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://go-mono.com/sources/monodevelop/%{name}-%{version}.tar.bz2
Patch: monodevelop-1.0-libxul.patch
Patch1: monodevelop-0.16-firefox.patch
Patch2: monodevelop-1.9-headbuild.patch
URL: http://www.monodevelop.com/
License: GPLv3+
Group: Development/Other
#Requires: gtksourceview-sharp >= %gtksourceview
Requires: gnome-sharp2 >= %gtksharp
Requires: glade-sharp2 >= %gtksharp
Requires: monodoc >= %monodoc
Requires: shared-mime-info
%if %mdvver < 200900
Requires: libmozilla-firefox = %mozver
%else
Requires: %mklibname xulrunner %xulrunner
%endif
Requires: xterm
#gw this is dllimported http://qa.mandriva.com/show_bug.cgi?id=34514
Requires: %mklibname svn 0
BuildRequires:	mono-addins
BuildRequires: mono-devel
#BuildRequires: gtksourceview-sharp >= %gtksourceview
BuildRequires: gnome-desktop-sharp-devel
BuildRequires: gnome-sharp2-devel >= %gtksharp
BuildRequires: glade-sharp2 >= %gtksharp
BuildRequires: monodoc >= %monodoc
BuildRequires: xsp
%if %mdvver < 200900
BuildRequires: mozilla-firefox-devel
%else
BuildRequires: xulrunner-devel-unstable >= %xulrunner
%endif
BuildRequires: intltool
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
%if %mdvver < 200900
%patch1 -p1 -b .firefox
%else
%patch -p1 -b .libxul
%endif
%patch2 -p1

%build
./configure --prefix=%_prefix --libdir=%_libdir --enable-versioncontrol --enable-aspnet --enable-subversion --enable-aspnetedit --enable-monoextensions --disable-update-mimedb --disable-update-desktopdb --enable-gtksourceview2
make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
mkdir -p %{buildroot}/`monodoc --get-sourcesdir`
%makeinstall_std pkgconfigdir=%pkgconfigdir packagedir=%buildroot%_prefix/lib/monodevelop/AddIns/AspNetEdit MOZILLA_HOME=%buildroot%_libdir/firefox-%mozver/
#gw fix mozilla-firefox directory
perl -pi -e "s^xMOZVERx^%mozver^g" %buildroot%_bindir/monodevelop

%find_lang %name

%if %mdkversion < 200900
%post
%update_mime_database
%update_desktop_database
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_mime_database
%clean_desktop_database
%clean_menus
%clean_icon_cache hicolor
%endif

%files -f %name.lang
%defattr(-,root,root) 
%doc AUTHORS ChangeLog README 
%{_bindir}/mdtool
%{_bindir}/monodevelop
%{_prefix}/lib/monodevelop/
%_mandir/man1/mdtool.1*
%_mandir/man1/monodevelop.1*
%{_datadir}/applications/monodevelop.desktop
%{_datadir}/mime/packages/monodevelop.xml
%_datadir/icons/hicolor/*/apps/monodevelop.*
%pkgconfigdir/monodevelop.pc
%pkgconfigdir/monodevelop-core-addins.pc

%clean
rm -rf $RPM_BUILD_ROOT
