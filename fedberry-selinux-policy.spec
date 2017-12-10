%global selinux_pol targeted

Name:           fedberry-selinux-policy
Version:        27
Release:        2%{?dist}
Summary:        Custom SELinux policy module(s) for FedBerry
Group:          Development/Tools
License:        GPLv3+
URL:            https://github.com/fedberry/fedberry-selinux-policy
Source0:        systemd_pstore.te
Source1:        systemd_syslogd.te
Source2:        sssd_passwd.te
Source3:        systemd-modules_unix_dgram_socket.te
Source4:        systemd_rfkill.te
Source5:        plymouthd_fb.te
Source6:        systemd_tmpfile.te

BuildArch:      noarch
BuildRequires:  checkpolicy
BuildRequires:  selinux-policy
BuildRequires:  selinux-policy-devel
Requires:       selinux-policy-targeted >= 3.13.1-225.10.fc25

%define policy_mods	%(echo %{sources} |sed -e 's|/builddir/build/SOURCES/||g' -e 's|\\.te||g')


%description
%{summary}.


%prep
mkdir %{name}
cp -a %{sources} %{name}


%build
cd %{name}
make -f /usr/share/selinux/devel/Makefile


%install
install -d %{buildroot}%{_datadir}/selinux/%{selinux_pol}
install -p -m 644 %{name}/*.pp %{buildroot}%{_datadir}/selinux/%{selinux_pol}/


%post
/usr/sbin/semodule -i %{_datadir}/selinux/%{selinux_pol}/*.pp &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /usr/sbin/semodule -r %{policy_mods} &> /dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_datadir}/selinux/%{selinux_pol}/*.pp


%changelog
* Sun Dec 10 2017 Vaughan Agrez <devel at agrez.net> 27-2
- Add systemd_tmpfile policy module

* Thu Nov 30 2017 Vaughan Agrez <devel at agrez.net> 27-1
- Bump version for Fedberry 27
- Add plymouthd frambuffer policy module

* Tue Aug 08 2017 Vaughan Agrez <devel at agrez.net> 26-1
- Bump version for Fedberry 26
- Drop systemd-modules_devtmpfs policy module
- Add sssd_passwd policy module

* Sat May 13 2017 Vaughan Agrez <devel at agrez.net> 25-4
- Add systemd_rfkill policy module

* Thu Mar 02 2017 Vaughan Agrez <devel at agrez.net> 25-3
- Drop policy modules: systemd-modules_modules_load, modprobe_module_load,
  systemd_module_load (Fixed in selinux-policy-targeted-3.13.1-225.11.fc25)

* Sun Feb 26 2017 Vaughan Agrez <devel at agrez.net> 25-2
- Add policy modules: systemd-modules_modules_load, modprobe_module_load,
  systemd_module_load
  (Fixes breakage from selinux-policy-targeted-3.13.1-225.10.fc25)

* Thu Feb 09 2017 Vaughan Agrez <devel at agrez.net> 25-1
- Update / add policy modules for f25 release images
- Improve %%prep & %%postun

* Thu Sep 22 2016 Vaughan Agrez <devel at agrez.net> 24-1
- Add policy module for systemd_modules
- Clean up spec
- Bump version to match FedBerry release

* Sun Aug 28 2016 Vaughan Agrez <devel at agrez.net> 0.1-3
- Add policy module for accounts_daemon & alsactl

* Sun Aug 21 2016 Vaughan Agrez <devel at agrez.net> 0.1-2
- Add policy module for systemd_rfkill

* Wed Aug 17 2016 Vaughan Agrez <devel at agrez.net> 0.1-1
- Initial package
