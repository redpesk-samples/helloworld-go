# helloworld-go

A golang version of helloworld example, implemented in a redpesk context

## Pre-requisites

To follow this tutorial without inconvenience, you have to use a redpesk factory WebUI or redpesk command line: `rp-cli`.

First you must register on a redpesk factory, for example you can use the community edition available at :

  [https://community-app.redpesk.bzh](https://community-app.redpesk.bzh/signup)

You can either use a GitHub or a GitLab account.

If you also want to use the command line, you must install and configuration `rp-cli` using instructions documented in [Command line interface (rp-cli) / Installation](https://docs.redpesk.bzh/docs/en/master/getting_started/rp_cli_quickstart/quickstart/quick-installation.html) chapter.

### Specfile

In order to build an RPM package in the redpesk context, your application should contain a specfile.
The reference specfile for helloworld-go sample can be found into the sources at the following path:
[conf.d/packaging/helloworld-go.spec](conf.d/packaging/helloworld-go.spec).

This specfile will be used to describe how to build your helloworld application. The resulting build produces an helloworld-go binary that is embedded in a RPM.

## Create ur project

Please read the [documentation](https://docs.redpesk.bzh/docs/en/master/getting_started/ci-build/docs/ci-build.html) to correctly create and setup your redpesk project and application for this example.

Create a project (choose any name) and then add an application by making the following choices or selecting the following fields :
- Select `Custom App` / `Create a New Application`
- `Name` : what ever you want but usually like the package name, eg. `Helloworld Go`
- `Package Name` : MUST be equal to Name field of specfile, here `helloworld-go`
- `Distribution` : select at least one, eg. `redpesk-lts-batz 2.1-update`
- `Source settings` : `https://github.com/redpesk-samples/helloworld-go`
- `Source revision` : let empty or set `master`
- `Spec file` : select `Relative Path` and set to `./conf.d/packaging/helloworld-go.spec`
- `Application services` : add `Fetch go dependencies` service and let `Archive` field to empty and select `bztar` Compression


Or you can create it using command line tool named `rp-cli` :

```bash
rpcli projects add --name golang-sample --optional-arch aarch64 --optional-arch x86_64 --optional-distro redpesk-lts-batz-2.1-update

rpcli applications add --name helloworld-go --pkg-name helloworld-go --project golang-sample  --source-url https://github.com/redpesk-samples/helloworld-go --source-rev master --specfile-type relative_path --specfile-location ./conf.d/packaging/helloworld-go.spec --service "go_dependency={'archive':'', 'compression':'bztar'}" --package-active-branch main
```

## Build

The aim of this part is to create a package which contained the helloworld-go application.

Either use redpesk factory WebUI and browse to `Dashboard / Projects / My projects / golang-sample / Applications / helloworld-go / Builds` view.

Or use following `rp-cli` command line:

```bash
rpcli applications build helloworld-go --project golang-sample
```

## Deploy on a board

Now that an helloworld-go package have been build thanks to redpesk, let's see how to install it on a board.
Since redpesk support cross-compilation, we can use either a x86_64 or aarch64 board to get your package installed in.
During this part, one case will be studied:

- Emulated x86_64 board: **qemu-x86_64**

If you want to use the helloworld-go in an embedded aarch64 context, but do not have a real board, an other tutorial is present at the following [path](https://docs.redpesk.bzh/docs/en/master/redpesk-os/boards/docs/boards/qemu.html#launch-a-aarch64-image).

### Booting a redpesk image with Qemu

Download and launch a x86\_64 image using instructions documented at :

https://docs.redpesk.bzh/docs/en/master/redpesk-os/boards/docs/boards/qemu.html

### Connect to the qemu over SSH

You can access your emulated board with the following command:

    ssh -p $PORT_SSH root@localhost


> _NOTE: Default root password is: `root`._

### Installing your package

Once you get in your redpesk image, you can proceed to the package download and installation.

The conventional way is to declare the new RPM repository associated to your project (in that example repo project is named `golang-sample_0a99d181` ).\
To do so, you just have execute a script named `install_repo.sh` that will declare the new repository. This script can be retrieved in top right corner of project overview in redpesk factory WebUI or using this command line:

```bash
rpcli projects get golang-sample --repository

...

Add repository on target:
-------------------------

redpesk-lts-batz-2.1-update
  curl -fsSL 'https://community-app.redpesk.bzh/kbuild/repos/golang-sample_0a99d181--redpesk-lts-batz-2.1-update-build/latest/install_repo.sh?token=21f7f0fc-4adb-44b7-a508-116b34f74fb0_491c62a8-3f1e-4012-a7e4-ee667c20d630' | bash
```

Copy the `curl -fsSL ...` command into your board/qemu console or ssh session.

And then you can install your helloworld-go application using :

```bash
dnf install -y helloworld-go
```

> NOTE: you can also directly install your RPM without declaring the repository using the command line below\
>   but note that it will not ease package updates if you plan to rebuild and update it several times.
>
```bash
dnf install -y https://community-app.redpesk.bzh/kbuild/work/tasks/8291/8291/helloworld-go-1.0.0-1.golang.sample_0a99d181.rpbatz_1.x86_64.rpm

```

### Run the sample

```bash
[root@localhost ~] /usr/bin/helloworld_go
Hello World !
```
