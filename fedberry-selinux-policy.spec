%global selinux_pol targeted
%global modulenames accounts_daemon alsactl systemd_devlog systemd_pstore systemd_syslogd systemd_rfkill systemd_modules

Name:           fedberry-selinux-policy
Version:        24
Release:        1%{?dist}
Summary:        Custom SELinux policy module(s) for FedBerry
Group:          Development/Tools
License:        GPLv3+
URL:            https://github.com/fedberry/fedberry-selinux-policy
Source0:        systemd_pstore.te
Source1:        systemd_devlog.te
Source2:        systemd_syslogd.te
Source3:        systemd_rfkill.te
Source4:        accounts_daemon.te
Source5:        alsactl.te
Source6:        systemd_modules.te

BuildArch:      noarch
BuildRequires:  checkpolicy
BuildRequires:  selinux-policy
BuildRequires:  selinux-policy-devel
Requires:       selinux-policy-targeted


%description
%{summary}.


%prep
mkdir %{name}
for module in %{modulenames}; do
    cp -p %{_sourcedir}/$module.te %{name}
done


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
  /usr/sbin/semodule -r %{modulenames} &> /dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_datadir}/selinux/%{selinux_pol}/*.pp


%changelog
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
