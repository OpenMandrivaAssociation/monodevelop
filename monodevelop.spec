%define name monodevelop
%define version 0.18.1
%define svn 1949
%define release %mkrel 1
%define gtksharp 1.9.5
%define gtksourceview 0.10
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
Patch1: monodevelop-0.16-firefox.patch
Patch4: monodevelop-desktop-entry.patch
URL: http://www.monodevelop.com/
License: GPL
Group: Development/Other
Requires: gtksourceview-sharp >= %gtksourceview
Requires: gnome-sharp2 >= %gtksharp
Requires: glade-sharp2 >= %gtksharp
Requires: monodoc >= %monodoc
Requires: shared-mime-info
Requires: libmozilla-firefox = %mozver
Requires: xterm
#gw this is dllimported http://qa.mandriva.com/show_bug.cgi?id=34514
Requires: %mklibname svn 0
BuildRequires:	mono-addins
BuildRequires: mono-devel
BuildRequires: gtksourceview-sharp >= %gtksourceview
BuildRequires: gnome-sharp2 >= %gtksharp
BuildRequires: glade-sharp2 >= %gtksharp
BuildRequires: monodoc >= %monodoc
BuildRequires: xsp
BuildRequires: mozilla-firefox-devel
BuildRequires: perl-XML-Parser
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Requires(post): desktop-file-utils shared-mime-info
Requires(postun): desktop-file-utils shared-mime-info

%description 
This is MonoDevelop which is intended to be a full-featured
integrated development environment (IDE) for mono and Gtk#.
It was originally a port of SharpDevelop 0.98.

%prep
%setup -q
%patch1 -p1 -b .firefox
%patch4 -p1

%build
./configure --prefix=%_prefix --libdir=%_libdir --enable-versioncontrol --enable-aspnet --enable-subversion --enable-aspnetedit
make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
mkdir -p %{buildroot}/`monodoc --get-sourcesdir`
%makeinstall_std UPDATE_MIME_DB="#" pkgconfigdir=%pkgconfigdir packagedir=%buildroot%_prefix/lib/monodevelop/AddIns/AspNetEdit MOZILLA_HOME=%buildroot%_libdir/firefox-%mozver/
#gw fix mozilla-firefox directory
perl -pi -e "s^xMOZVERx^%mozver^g" %buildroot%_bindir/monodevelop

# menu

#icons
mkdir -p %buildroot{%_liconsdir,%_iconsdir,%_miconsdir}
ln -s %_datadir/pixmaps/%name.png %buildroot%_liconsdir/
convert -scale 32x32 %name.png %buildroot%_iconsdir/%name.png
convert -scale 16x16 %name.png %buildroot%_miconsdir/%name.png

%find_lang %name

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
%{_prefix}/lib/monodevelop/
%_mandir/man1/mdtool.1*
%{_datadir}/applications/monodevelop.desktop
%{_datadir}/mime/packages/monodevelop.xml
%{_datadir}/pixmaps/monodevelop.png
%pkgconfigdir/monodevelop.pc
%pkgconfigdir/monodevelop-core-addins.pc
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png

%clean
rm -rf $RPM_BUILD_ROOT
