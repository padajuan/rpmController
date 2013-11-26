Summary: One RPM Controller to rule them all
Name: rpmcontroller
Version: %{_gs_version}
Release: %{_gs_revision}
License: MIT
BuildRoot: %{_topdir}/BUILD/%{name}
BuildArch: noarch
Provides:  rpmcontroller
Group: Application/M2M Global Services
Distribution: Global Services
Vendor: Telefónica I+D


%description
This utility take control about the RPMs installed in X nodes and centralize the information in a MongoDB node.

%define _controller_dir /opt/rpmcontroller

# Do not check unpackaged files
%undefine __check_files


# -------------------------------------------------------------------------------------------- #
# prep section:
# -------------------------------------------------------------------------------------------- #
# remove previous build files
%prep
rm -Rf $RPM_BUILD_ROOT/*

# clean up development-only files
find %{_gitdir} -depth -name .git -exec rm -rf {} \;
if [ $? -ne 0 ]
then
  echo "Error cleaning GIT stuff.";
fi

%build
# -------------------------------------------------------------------------------------------- #
# install section:
# -------------------------------------------------------------------------------------------- #
%install
# copy gs-api project from the SVN repo
[ -d $RPM_BUILD_ROOT%{_controller_dir} ] || mkdir -p $RPM_BUILD_ROOT%{_controller_dir}
cp -rp %{_gitdir}/* $RPM_BUILD_ROOT%{_controller_dir}

# -------------------------------------------------------------------------------------------- #
# post-install section:
# -------------------------------------------------------------------------------------------- #
%post
## Install all requirements.txt
pip-python install -r %{_controller_dir}/requirements.txt
if [ $? -ne 0 ]
then
  echo "Error installing PiP dependencies.";
fi

[ -h /usr/bin/rpmcontroller ] || ln -s %{_controller_dir}/bin/rpmcontroller /usr/bin


# -------------------------------------------------------------------------------------------- #
# pre-uninstall section:
# -------------------------------------------------------------------------------------------- #
%preun


# -------------------------------------------------------------------------------------------- #
# post-uninstall section:
# -------------------------------------------------------------------------------------------- #
%postun
unlink /usr/bin/rpmcontroller
exit 0
	
		
%clean
rm -rf $RPM_BUILD_ROOT/*

%files
%{_controller_dir}/*
# Specify config file
%config %{_controller_dir}/conf/rpmController.ini




