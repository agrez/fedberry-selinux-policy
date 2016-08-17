%global selinux_pol targeted
%global modulenames systemd_devlog systemd_pstore systemd_syslogd

Name:           fedberry-selinux-policy
Version:        0.1
Release:        1%{?dist}
License:        GPLv3+
Source0:        systemd_pstore.te
Source1:        systemd_devlog.te
Source2:        systemd_syslogd.te
Group:          Development/Tools
Summary:        Custom SELinux policy module(s) for FedBerry
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
BuildRequires:  checkpolicy, selinux-policy, selinux-policy-devel
Requires:       selinux-policy-targeted

%description
Custom SELinux policy module(s) for FedBerry.

%prep
if [ ! -d %{name} ]; then
  mkdir %{name}
fi
cp -p %{SOURCE0} %{SOURCE1} %{SOURCE2} %{name}

%build
cd %{name}
make -f /usr/share/selinux/devel/Makefile

%install
install -d %{buildroot}%{_datadir}/selinux/%{selinux_pol}
install -p -m 644 %{name}/*.pp %{buildroot}%{_datadir}/selinux/%{selinux_pol}/

%post
/usr/sbin/semodule -i %{_datadir}/selinux/%{selinux_pol}/systemd_*.pp &> /dev/null || :

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
* Wed Aug 17 2016 Vaughan Agrez <devel at agrez.net> 0.1-1
- Initial package
