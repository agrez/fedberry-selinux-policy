%global selinux_pol targeted
%global modulenames accounts_daemon alsactl systemd_devlog systemd_pstore systemd_syslogd systemd_rfkill

Name:           fedberry-selinux-policy
Version:        0.1
Release:        3%{?dist}
License:        GPLv3+
Source0:        systemd_pstore.te
Source1:        systemd_devlog.te
Source2:        systemd_syslogd.te
Source3:        systemd_rfkill.te
Source4:        accounts_daemon.te
Source5:        alsactl.te
Group:          Development/Tools
Summary:        Custom SELinux policy module(s) for FedBerry
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
BuildRequires:  checkpolicy, selinux-policy, selinux-policy-devel
Requires:       selinux-policy-targeted

%description
Custom SELinux policy module(s) for FedBerry.

%prep
mkdir %{name}
cp -p %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{name}

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
* Sun Aug 28 2016 Vaughan Agrez <devel at agrez.net> 0.1-3
- Add policy module for accounts_daemon & alsactl

* Sun Aug 21 2016 Vaughan Agrez <devel at agrez.net> 0.1-2
- Add policy module for systemd_rfkill

* Wed Aug 17 2016 Vaughan Agrez <devel at agrez.net> 0.1-1
- Initial package
