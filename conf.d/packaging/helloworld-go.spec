# disable debuginfo package generation
%global debug_package %{nil}

# set Go cross-compilation environment variable
%ifarch aarch64
    %define go_arch arm64
%elifarch x86_64
    %define go_arch amd64
%endif

Name:           helloworld-go
Version:        1.0.0
Release:        0%{?dist}
Summary:        Simple hello world program in golang
License:        Apache-2.0
URL:            https://github.com/redpesk-samples/helloworld-go
Source:         %{name}-%{version}.tar.gz
Source1:        vendor.tar.bz2

BuildRequires:  go-rpm-macros
BuildRequires:  go >= 1.19

%description
The simple helloworld program written in Go!

### redtest package definition
%package redtest
Summary:        Redtest subpackage of helloworld-go package
Requires:       %{name} = %{version}

%description redtest
The tests for the simplest hello program of the world!

### Prepare build environment stage
%prep
# unpack archive source 1, IOW unpack go dependencies into vendor directory
%autosetup -D -a 1

### Build stage
%build
%ifnarch aarch64 x86_64
    echo "Unsupported architecture %{_arch}"
    exit 1
%endif
GOOS=linux GOARCH=%{go_arch} go build -buildmode=pie -ldflags="-linkmode=external" -o helloworld-go .
GOOS=linux GOARCH=%{go_arch} go test -buildmode=pie -ldflags="-linkmode=external" -o helloworld-go.test ./cmd/...

### Check stage
%check
%ifarch x86_64
make test
%endif

# Install stage
%install
install -Dm 755 helloworld-go %{buildroot}/%{_bindir}/helloworld-go
install -Dm 755 redtest/run-redtest %{buildroot}/%{_libexecdir}/redtest/%{name}/run-redtest
install -Dm 755 helloworld-go.test %{buildroot}/%{_libexecdir}/redtest/%{name}/helloworld-go.test

### Files list for "main" / helloworld-go package
%files
%license LICENSE
%doc README.md
%{_bindir}/helloworld-go

### Files list for redtest package
%files redtest
%{_libexecdir}/redtest/%{name}/*

### Changelog
%changelog

* Wed Feb 05 2025 IoT.bzh <sebastien@iot.bzh> 1.0.0
- Initial creation
