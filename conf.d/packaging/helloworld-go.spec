%global debug_package %{nil}

Name:           helloworld-go
Version:        1.0.0
Release:        0%{?dist}
Summary:        Simple hello world program in golang
License:        Apache-2.0
URL:            https://github.com/redpesk-samples/helloworld-go
Source:         %{name}-%{version}.tar.gz
Source1:        vendor.tar.bz2

BuildRequires:  go-rpm-macros
BuildRequires:  go >= 1.21

%ifarch aarch64
    %define go_arch arm64
%elifarch x86_64
    %define go_arch amd64
%endif

%description
The simple helloworld program written in go !

%prep
%autosetup -D -a 1

%build
%ifnarch aarch64 x86_64
    echo "Unsupported architecture %{_arch}"
    exit 1
%endif
GOOS=linux GOARCH=%{go_arch} go build -buildmode=pie -ldflags="-linkmode=external" -o helloworld-go .

# this check is not yet working
#%%check
#make test

%install
install -Dm 755 helloworld-go %{buildroot}/%{_bindir}/helloworld-go

%files
%license LICENSE
%doc README.md
%{_bindir}/helloworld-go

%changelog
