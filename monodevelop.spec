%define	name monodevelop
%define	version  3.0.3.5
%define release  2
%define	gtksharp 1.9.5
%define	monodoc  1.0
%define	pkgconfigdir %_datadir/pkgconfig

Summary:	Full-featured IDE for mono and Gtk#
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://download.mono-project.com/sources/monodevelop/%{name}-%{version}.tar.bz2
Patch0:		link_system_nunit.patch
Patch1:		%{name}-3.0.3.2-md-gettext.patch
URL:		http://www.monodevelop.com/
License:	LGPLv2
Group:		Development/Other
#Requires: gtksourceview-sharp >= % gtksourceview
Requires:	gnome-sharp2 >= %gtksharp
Requires:	glade-sharp2 >= %gtksharp
Requires:	monodoc >= %monodoc
Requires:	mono-tools
Requires:	mono-basic
Requires:	libmono-devel
Requires:	shared-mime-info
Requires:	xterm
Requires:	subversion
Requires:	git
Requires:	xsp
BuildRequires:	pkgconfig(gconf-sharp-2.0) >= 2.12.8
BuildRequires:	pkgconfig(glade-sharp-2.0) >= 2.12.8
BuildRequires:	pkgconfig(glib-sharp-2.0) >= 2.12.8
BuildRequires:	pkgconfig(gnome-sharp-2.0) >= 2.12.8
BuildRequires:	pkgconfig(gnome-vfs-sharp-2.0) >= 2.12.8
BuildRequires:	pkgconfig(gtk-sharp-2.0) >= 2.12.8
BuildRequires:	pkgconfig(wcf)
BuildRequires:	pkgconfig(mono-addins) >= 0.6
BuildRequires:	pkgconfig(mono-addins-gui) >= 0.6
BuildRequires:	pkgconfig(mono-addins-setup) >= 0.6
BuildRequires:	pkgconfig(mono-nunit)
BuildRequires:	pkgconfig(monodoc) >= 1.0
BuildRequires:	pkgconfig(mono) >= 2.8
BuildRequires:	intltool
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
# Obsolete deprecated plugins which are not compatible with MD 2.6
Obsoletes:	monodevelop-boo
Obsoletes:	monodevelop-debugger-mdb

Conflicts:	%{name} <= 3.0.3.2-2
Obsoletes:	%{name} <= 3.0.3.2-2

BuildArch:     noarch
%define _requires_exceptions ^libg.*\\|lib64g.*\\|libp.*\\|lib64p.*\\|liba.*\\|lib64a.*

%description 
This is MonoDevelop which is intended to be a full-featured
integrated development environment (IDE) for mono and Gtk#.
It was originally a port of SharpDevelop 0.98.

%prep
%setup -q
%patch0 -p1 -b .nunit
%patch1 -p1 -b .mdgettext

%build
./configure --prefix=%_prefix --libdir=%_prefix/lib --enable-versioncontrol --enable-aspnet --enable-subversion --enable-git --enable-aspnetedit --enable-monoextensions --disable-update-mimedb --disable-update-desktopdb 
#--enable-gtksourceview2
make

%install
rm -rf %{buildroot} %name.lang
mkdir -p %{buildroot}/`monodoc --get-sourcesdir`
%makeinstall_std pkgconfigdir=%pkgconfigdir packagedir=%buildroot%_prefix/lib/monodevelop/AddIns/AspNetEdit MOZILLA_HOME=%buildroot%_prefix/lib/firefox-%mozver/

desktop-file-install --dir %buildroot%_datadir/applications \
  %buildroot%_datadir/applications/*.desktop

%find_lang %name

%files -f %name.lang
%doc AUTHORS ChangeLog README 
%{_bindir}/mdtool
%{_bindir}/monodevelop
%{_prefix}/lib/monodevelop
%_mandir/man1/mdtool.1*
%_mandir/man1/monodevelop.1*
%{_datadir}/applications/monodevelop.desktop
%{_datadir}/mime/packages/monodevelop.xml
%_datadir/icons/hicolor/*/apps/monodevelop.*
%pkgconfigdir/monodevelop.pc
%pkgconfigdir/monodevelop-core-addins.pc
