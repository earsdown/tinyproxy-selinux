# vim: sw=4:ts=4:et


%define relabel_files() \
restorecon -R /usr/sbin/tinyproxy; \
restorecon -R /etc/rc\.d/init\.d/tinyproxy; \
restorecon -R /var/log/tinyproxy; \
restorecon -R /var/run/tinyproxy; \
restorecon -R /etc/tinyproxy;

%define selinux_policyver 3.13.1-23

Name:   tinyproxy_selinux
Version:	1.0
Release:	1%{?dist}
Summary:	SELinux policy module for tinyproxy

Group:	System Environment/Base		
License:	GPLv2+	
# This is an example. You will need to change it.
URL:		https://github.com/earsdown/tinyproxy-selinux
Source0:	tinyproxy.pp
Source1:	tinyproxy.if
Source2:	tinyproxy_selinux.8


Requires: policycoreutils, libselinux-utils, policycoreutils-python
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils, policycoreutils-python
Requires(preun): policycoreutils-python
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the SELinux policy security module for tinyproxy.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/tinyproxy_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/


%post
semodule -n -i %{_datadir}/selinux/packages/tinyproxy.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files
    /sbin/semanage port -a -t tinyproxy_port_t -p tcp 8888
fi;
exit 0

%preun
/sbin/semanage port --list -C | grep tinyproxy_port_t | sed -e 's/tinyproxy_port_t/-p/g' | while read line; do
  /sbin/semanage port -d $line
done

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r tinyproxy
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files
    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/tinyproxy.pp
%{_datadir}/selinux/devel/include/contrib/tinyproxy.if
%{_mandir}/man8/tinyproxy_selinux.8.*


%changelog
* Fri Aug 14 2015 YOUR NAME <YOUR@EMAILADDRESS> 1.0-1
- Initial version
