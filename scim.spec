%define nam             scim
%define ver             1.4.9
%define rel             1
%define build_config_socket	1
%define build_config_simple	1
%define build_frontend_x11	1
%define build_frontend_socket	1
%define build_imengine_rawcode	1
%define build_imengine_socket	1
%define build_gtk2_immodule	1
%define build_scim_setup        1
%define build_panel_gtk         1
%define build_gtk_utils         1
%define build_x11_utils         1
%define build_filter_sctc       1

# Something's not quite right with libtool....
%define __libtoolize    echo

Summary:        Smart Chinese/Common Input Method platform
Name:           %{nam}
Version:        %{ver}
Release:        %{rel}
License:        LGPL
Group:          System Environment/Libraries
URL:            http://scim.freedesktop.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

Source0:        %{name}-%{version}.tar.gz
#NoSource: 0

PreReq:         /sbin/ldconfig, /bin/sh

%if %{build_gtk_utils}
Requires:       glib2 >= 2.0.0
BuildRequires:  glib2-devel >= 2.0.0
Requires:       gtk2 >= 2.3.5
BuildRequires:  gtk2-devel >= 2.3.5
Requires:       pango >= 1.0.0
BuildRequires:  pango-devel >= 1.0.0
%endif

%if %{build_x11_utils}
Requires:       XFree86-libs >= 4.1.0
BuildRequires:  XFree86-devel >= 4.1.0
%endif

BuildRequires:  pkgconfig >= 0.12

%description
SCIM is a developing platform to significant reduce the difficulty of 
input method development. 

%package devel
Summary:        Smart Chinese/Common Input Method platform
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       pkgconfig >= 0.12

%description devel
The scim-devel package includes the static libraries and header files
for the scim package.

Install scim-devel if you want to develop programs which will use
scim.

#--------------------------------------------------

%prep

%setup -n %{name}-%{version}

%build
CFLAGS="-O3" CXXFLAGS="-O3" \
%configure \
%if ! %{build_config_socket}
  --disable-config-socket \
%endif
%if ! %{build_config_simple}
  --disable-config-simple \
%endif
%if ! %{build_frontend_x11}
  --disable-frontend-x11 \
%endif
%if ! %{build_frontend_socket}
  --disable-frontend-socket \
%endif
%if ! %{build_imengine_rawcode}
  --disable-im-rawcode \
%endif
%if ! %{build_imengine_socket}
  --disable-im-socket \
%endif
%if ! %{build_filter_sctc}
  --disable-filter-sctc \
%endif
%if ! %{build_gtk2_immodule}
  --disable-gtk2-immodule \
%endif
%if ! %{build_scim_setup}
  -disable-setup-ui \
%endif


make 

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

make DESTDIR=${RPM_BUILD_ROOT} install

mkdir -p ${RPM_BUILD_ROOT}/%{_libdir}/scim-1.0/{Config,FrontEnd,IMEngine,SetupUI,Helper,Filter}

rm -f ${RPM_BUILD_ROOT}/%{_libdir}/scim-1.0/*/*/*.{a,la}
rm -f ${RPM_BUILD_ROOT}//usr/lib/gtk-2.0/immodules/im-scim.{a,la}

# install user manual
mkdir -p docs/dist/manual/zh_CN/figures/

cp -a docs/manual/zh_CN/user-manual.{html,xml} docs/dist/manual/zh_CN/
cp -a docs/manual/zh_CN/figures/*.png docs/dist/manual/zh_CN/figures/

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%if %{build_gtk2_immodule}
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules
%endif

%postun
/sbin/ldconfig

%if %{build_gtk2_immodule}
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules
%endif


%files
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS README ChangeLog TODO
%doc docs/dist/manual/zh_CN
%dir %{_sysconfdir}/scim
%dir %{_libdir}/scim-1.0/*/FrontEnd
%dir %{_libdir}/scim-1.0/*/IMEngine
%dir %{_libdir}/scim-1.0/*/Config
%dir %{_libdir}/scim-1.0/*/SetupUI
%dir %{_libdir}/scim-1.0/*/Helper
%dir %{_libdir}/scim-1.0/*/Filter
%dir %{_libdir}/scim-1.0/Config
%dir %{_libdir}/scim-1.0/FrontEnd
%dir %{_libdir}/scim-1.0/IMEngine
%dir %{_libdir}/scim-1.0/SetupUI
%dir %{_libdir}/scim-1.0/Helper
%dir %{_libdir}/scim-1.0/Filter
%dir %{_datadir}/scim
%dir %{_datadir}/scim/icons
%config %{_sysconfdir}/scim/global
%{_bindir}/scim
%{_bindir}/scim-config-agent
%{_libdir}/libscim*.so.*
%{_libdir}/scim-1.0/scim-launcher
%{_libdir}/scim-1.0/scim-helper-launcher
%{_libdir}/scim-1.0/scim-helper-manager
%{_datadir}/locale/*/LC_MESSAGES/scim.mo
%{_datadir}/scim/icons/keyboard.png
%{_datadir}/scim/icons/up.png
%{_datadir}/scim/icons/down.png
%{_datadir}/scim/icons/left.png
%{_datadir}/scim/icons/right.png
%{_datadir}/scim/icons/full-letter.png
%{_datadir}/scim/icons/half-letter.png
%{_datadir}/scim/icons/full-punct.png
%{_datadir}/scim/icons/half-punct.png
%{_datadir}/scim/icons/help.png
%{_datadir}/scim/icons/pin-up.png
%{_datadir}/scim/icons/pin-down.png
%{_datadir}/scim/icons/setup.png
%{_datadir}/scim/icons/trademark.png
%{_datadir}/scim/icons/menu.png
%if %{build_scim_setup}
%{_bindir}/scim-setup
%{_datadir}/applications/scim-setup.desktop
%{_datadir}/control-center-2.0/capplets/scim-setup.desktop
%{_datadir}/pixmaps/scim-setup.png
%{_libdir}/scim-1.0/*/Helper/setup.so
%{_libdir}/scim-1.0/*/SetupUI/aaa-frontend-setup.so
%{_libdir}/scim-1.0/*/SetupUI/aaa-imengine-setup.so
%endif
%if %{build_panel_gtk}
%{_libdir}/scim-1.0/scim-panel-gtk
%if %{build_scim_setup}
%{_libdir}/scim-1.0/*/SetupUI/panel-gtk-setup.so
%endif
%endif
%if %{build_frontend_x11}
%{_libdir}/scim-1.0/*/FrontEnd/x11.so
%endif
%if %{build_imengine_rawcode}
%{_libdir}/scim-1.0/*/IMEngine/rawcode.so
%{_datadir}/scim/icons/rawcode.png
%endif
%if %{build_filter_sctc}
%{_libdir}/scim-1.0/*/Filter/sctc.so
%{_datadir}/scim/icons/sctc.png
%{_datadir}/scim/icons/sctc-sc-to-tc.png
%{_datadir}/scim/icons/sctc-tc-to-sc.png
%endif
%if %{build_config_simple}
%config %{_sysconfdir}/scim/config
%{_libdir}/scim-1.0/*/Config/simple.so
%endif
%if %{build_imengine_socket}
%{_libdir}/scim-1.0/*/IMEngine/socket.so
%endif
%if %{build_frontend_socket}
%{_libdir}/scim-1.0/*/FrontEnd/socket.so
%endif
%if %{build_config_socket}
%{_libdir}/scim-1.0/*/Config/socket.so
%endif
%if %{build_gtk2_immodule}
/usr/lib/gtk-2.0/immodules/im-scim.so
%endif

%files devel
%defattr(-, root, root)
%doc docs/html
%doc docs/developers
%{_libdir}/libscim*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/scim-1.0

#--------------------------------------------------

%changelog
* Sun Jan 9 2005 James Su <suzhe@tsinghua.org.cn>
- Remove GConf Config module.

* Wed Jan 5 2005 James Su <suzhe@tsinghua.org.cn>
- Remove table IMEngine.

* Fri Aug 6 2004 James Su <suzhe@tsinghua.org.cn>
- Move scim-launcher and scim-panel-gtk to /usr/lib/scim-1.0.

* Sun Jun 20 2004  James Su <suzhe@tsinghua.org.cn>
- Merge all things into one package.

* Sat Jun 19 2004  James Su <suzhe@tsinghua.org.cn>
- Added /usr/libexec/scim-launcher.
- Remove setup module for SocketFrontEnd and SocketIMEngine.

* Mon Mar 8 2004  James Su <suzhe@turbolinux.com.cn>
- Added scim-config-agent.

* Thu Oct 30 2003 James Su <suzhe@turbolinux.com.cn>
- Added Simplified Chinese User Manual.

* Wed Sep 03 2003 James Su <suzhe@turbolinux.com.cn>
- cleanup spec.

* Tue Sep 02 2003 James Su <suzhe@turbolinux.com.cn>
- upto 0.8.0

* Tue Jul 29 2003 James Su <suzhe@turbolinux.com.cn>
- updated to include scim-panel-gtk.

* Thu Jun 19 2003 James Su <suzhe@turbolinux.com.cn>
- updated to include scim-setup and its modules.

* Thu Apr 3 2003 James Su <suzhe@turbolinux.com.cn>
- added suite package, which includes all necessary components of SCIM.

* Tue Mar 25 2003 James Su <suzhe@turbolinux.com.cn>
- updated to v0.4.0

* Wed Feb 26 2003 James Su <suzhe@turbolinux.com.cn>
- implemented dynamic adjust feature for generic table module.
- fixed key handling bug in generic table module.

* Mon Feb 10 2003 James Su <suzhe@turbolinux.com.cn>
- Replaced highlight_start and highlight_end in scim_server
  and scim_frontend with AttributeList (scim_attributes.h)
- Moved icons/* to data/icons and gtkstringview.* to
  utils/

* Thu Jan 2 2003 James Su <suzhe@turbolinux.com.cn>
- updated configure.ac and Makefile.am
- ready to release 0.3.0

* Tue Nov 12 2002 James Su <suzhe@turbolinux.com.cn>
- merged signal system from libinti.
- implemented namespace scim.
- implemented referenced object.
- version 0.3.0

* Tue Nov 05 2002 James Su <suzhe@turbolinux.com.cn>
- minor fixes for table IM module.

* Mon Nov 04 2002 James Su <suzhe@turbolinux.com.cn>
- More IMdkit memory leak fixes.
- Table input method bugfixes.
- version 0.2.2

* Fri Nov 01 2002 James Su <suzhe@turbolinux.com.cn>
- improved table input method.
- actually fixed the memleaks within IMdkit.
- pumped the version to 0.2.1

* Thu Oct 31 2002 James Su <suzhe@turbolinux.com.cn>
- fixed some memory leaks in IMdkit
- reduced memory usage.
- upgraded to libtool-1.4.3

* Tue Oct 29 2002 James Su <suzhe@turbolinux.com.cn>
- finished Generic Table input server module.
- fixed several bugs in scim-lib.

* Thu Oct 10 2002 James Su <suzhe@turbolinux.com.cn>
- used gettext to support i18n message.
- added release info to lib name.

* Mon Sep 30 2002 James Su <suzhe@turbolinux.com.cn>
- version 0.1.4
- added Embedded Lookup Table style into X11 FrontEnd.
- use wchar_t instead of unsigned long if __STDC_ISO_10646__ defined.

* Sun Sep 22 2002 James Su <suzhe@turbolinux.com.cn>
- version 0.1.3
- config button of X11 FrontEnd was disabled.

* Fri Sep 6 2002 James Su <suzhe@turbolinux.com.cn>
- simplified the utilities and lookup table interface.

* Wed Aug 21 2002 James Su <suzhe@turbolinux.com.cn>
- version 0.1.2
- added configuration options to disable modules.
- enhanced X11 FrontEnd.

* Sun Aug 11 2002 James Su <suzhe@turbolinux.com.cn>
- version 0.1.1
- X11 FrontEnd was enhanced.

* Sat Aug 10 2002 James Su <suzhe@turbolinux.com.cn>
- version 0.1.0
- many bugfixes.
- Help window of X11 FrontEnd was implemented.
- scim can exit cleanly.

* Fri Aug 2 2002 James Su <suzhe@turbolinux.com.cn>
- SCIM 0.0.13.
- Minor bugfixes.

* Mon Jul 29 2002 James Su <suzhe@turbolinux.com.cn>
- SCIM 0.0.12.
- Minor bugfixes.

* Sun Jul 28 2002 James Su <suzhe@turbolinux.com.cn>
- SCIM 0.0.11.
- Minor bugfixes.

* Sun Jul 21 2002 James Su <suzhe@turbolinux.com.cn>
- SCIM 0.0.10.
- Added Simple Config module.

* Sat Jun 22 2002 James Su <suzhe@turbolinux.com.cn>
- first public release of SCIM.

