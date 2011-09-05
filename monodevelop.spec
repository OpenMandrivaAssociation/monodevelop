#define name monodevelop
%define version 2.4.2
%define release %mkrel 1
%define gtksharp 1.9.5
%define monodoc 1.0
%define pkgconfigdir %_datadir/pkgconfig
%if %mdvver < 201000
%define xulrunner_version 1.9
%endif

Summary:	Full-featured IDE for mono and Gtk#
Name:		monodevelop
Version:	%{version}
Release:	%{release}
Source:		http://go-mono.com/sources/monodevelop/%{name}-%{version}.tar.bz2
Patch:		monodevelop-1.9.2-libxul.patch
Patch1:		%{name}.desktop.patch
URL:		http://www.monodevelop.com/
License:	LGPLv2
Group:		Development/Other
#Requires:	gtksourceview-sharp >= %gtksourceview
Requires:	gnome-sharp2 >= %gtksharp
Requires:	glade-sharp2 >= %gtksharp
Requires:	monodoc >= %monodoc
Requires:	shared-mime-info
Requires:	libxulrunner >= %xulrunner_version
Requires:	xterm
Requires:	subversion
BuildRequires:	mono-addins-devel
BuildRequires:	gnome-desktop-sharp-devel
BuildRequires:	gnome-sharp2-devel >= %gtksharp
BuildRequires:	glade-sharp2 >= %gtksharp
BuildRequires:	monodoc >= %monodoc
%if %mdvver >= 201100
BuildRequires:	xsp-devel
%else
BuildRequires:	xsp
%endif
%if %mdvver >= 201000
BuildRequires:	xulrunner-devel
%else
BuildRequires:	xulrunner-devel-unstable >= %xulrunner_version
%endif
BuildRequires:	intltool
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Requires(post):		desktop-file-utils shared-mime-info
Requires(postun):	desktop-file-utils shared-mime-info
%define _requires_exceptions ^libg.*\\|lib64g.*\\|libp.*\\|lib64p.*\\|liba.*\\|lib64a.*

%description 
This is MonoDevelop which is intended to be a full-featured
integrated development environment (IDE) for mono and Gtk#.
It was originally a port of SharpDevelop 0.98.

%prep
%setup -q
%patch -p1 -b .libxul
%patch1 -p0
autoconf

%build
./configure --prefix=%_prefix --libdir=%_prefix/lib --enable-versioncontrol --enable-aspnet --enable-subversion --enable-aspnetedit --enable-monoextensions --disable-update-mimedb --disable-update-desktopdb 
#--enable-gtksourceview2
make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
mkdir -p %{buildroot}/`monodoc --get-sourcesdir`
%makeinstall_std pkgconfigdir=%pkgconfigdir packagedir=%buildroot%_prefix/lib/monodevelop/AddIns/AspNetEdit MOZILLA_HOME=%buildroot%_prefix/lib/firefox-%mozver/

%find_lang %name

#gw replace bundled nunit by symlinks:
cd %buildroot%_prefix/lib/monodevelop/AddIns/NUnit
for x in nunit.*.dll; do
    ln -sf %_prefix/lib/mono/2.0/$x .
done

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
