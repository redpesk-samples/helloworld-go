# helloworld-go

A "helloworld"-type project to teach how a Go program is built in the redpesk factory

See the C equivalent here: <https://github.com/redpesk-samples/simple-helloworld>

## Pre-requisites

To follow this tutorial, you have to use a redpesk factory WebUI or the redpesk command line `rp-cli`.

First you must register on a redpesk factory, for example you can use the community edition available at [https://community-app.redpesk.bzh](https://community-app.redpesk.bzh/signup).

You can use either a GitHub or a GitLab account.

To setup the application and run the build, you can choose to use the same WebUI where you signed up, or a command line interface to the factory. If you prefer the CLI, you must install and configure `rp-cli` using the instructions of the [Command line interface (rp-cli) / Installation](https://docs.redpesk.bzh/docs/en/master/getting_started/rp_cli_quickstart/quickstart/quick-installation.html) chapter.

### Specfile

In order to build an RPM package in the redpesk context, your application should contain a specfile. The reference specfile for helloworld-go sample can be found into the sources at [conf.d/packaging/helloworld-go.spec](conf.d/packaging/helloworld-go.spec).

This specfile will be used to describe how to build your helloworld application. The resulting build produces an helloworld-go binary embedded in an RPM package.

## Create your project

Please read the [documentation](https://docs.redpesk.bzh/docs/en/master/getting_started/ci-build/docs/ci-build.html) to correctly create and setup your redpesk project and application for this example.

The application should have the following parameters to be able to build the helloworld-go sample:

- Select `Custom App` / `Create a New Application`
- `Name`: whatever you want but usually like the package name, eg. `Helloworld Go`
- `Package Name`: MUST be equal to Name field of specfile, here `helloworld-go`
- `Distribution`: select at least one, eg. `redpesk-lts-batz 2.1-update`
- `Source settings`: `https://github.com/redpesk-samples/helloworld-go`
- `Source revision`: leave empty or set `master`
- `Spec file`: select `Relative Path` and set to `./conf.d/packaging/helloworld-go.spec`
- `Application services`: add `Fetch go dependencies` service, leave the `Archive` field empty and select `bztar` compression

Or you can create the project and app using our command line tool named `rp-cli`:

```bash
rpcli projects add --name golang-sample --optional-arch aarch64 --optional-arch x86_64 --optional-distro redpesk-lts-batz-2.1-update

rpcli applications add --name helloworld-go --pkg-name helloworld-go --project golang-sample  --source-url https://github.com/redpesk-samples/helloworld-go --source-rev master --specfile-type relative_path --specfile-location ./conf.d/packaging/helloworld-go.spec --service "go_dependency={'archive':'', 'compression':'bztar'}" --package-active-branch main
```

## Build

Now that a project is created and an application configured to match the helloworld-go sample, you can launch the actual build. this will create an RPM package containing the application, and ready to be installed in redpesk OS.

If you use redpesk factory's WebUI, browse to `Dashboard / Projects / My projects / golang-sample / Applications / helloworld-go / Builds` view and click the green "play" button to run the build.

If you use `rp-cli`, run the following command (adapt the application name `helloworld-go` and the project name `golang-sample` according to your inputs in the previous step):

```bash
rpcli applications build helloworld-go --project golang-sample
```

## Deploy on a board

Now that an helloworld-go package has been built thanks to redpesk, let's see how to install it on a board.

Since redpesk support cross-compilation, we can use either a x86_64 or aarch64 board to get your package installed in; you just have to select the correct architecture when creating the project and building the application.

For this tutorial, we will use an emulated QEMU x86_64 board.

If you want to use helloworld-go in an embedded aarch64 context but do not have a real board, we have [another tutorial](https://docs.redpesk.bzh/docs/en/master/redpesk-os/boards/docs/boards/qemu.html#launch-a-aarch64-image) to use QEMU to run aarch64 images.

### Booting a redpesk image with Qemu

Download and launch an x86\_64 image using the instructions at <https://docs.redpesk.bzh/docs/en/master/redpesk-os/boards/docs/boards/qemu.html>.

### Connect to the QEMU machine over SSH

You can access your emulated board with the following command:

```bash
ssh -p $PORT_SSH root@localhost
```

> NOTE: the default root password is `root`.

### Installing your package

Once you get in your redpesk image, you can proceed to download and install the package.

The conventional way is to declare the new RPM repository associated to your project (in that example project, the repo is named `golang-sample_0a99d181`).

To do so, you just have execute a script named `install_repo.sh` that will declare the new repository. This script can be retrieved in top right corner of project overview in redpesk factory WebUI (see the box-looking button in the distributions and architectures table) or using this command line:

```bash
rpcli projects get golang-sample --repository
```

Which will produce the following output:

```txt
Add repository on target:
-------------------------

redpesk-lts-batz-2.1-update
  -> curl -fsSL 'https://community-app.redpesk.bzh/kbuild/repos/golang-sample_0a99d181--redpesk-lts-batz-2.1-update-build/latest/install_repo.sh?token=21f7f0fc-4adb-44b7-a508-116b34f74fb0_491c62a8-3f1e-4012-a7e4-ee667c20d630' | bash
```

Copy the `curl -fsSL ...` command into your board/QEMU console or SSH session.

Then you can install your helloworld-go application using the package manager:

```bash
dnf install -y helloworld-go
```

> NOTE: you can also directly install your RPM without declaring the repository using the command line below but note that it will make package updates harder if you plan to rebuild and update it several times. The URL is found in the details of the application build.

  ```bash
  dnf install -y https://community-app.redpesk.bzh/kbuild/work/tasks/8291/8291/helloworld-go-1.0.0-1.golang.sample_0a99d181.rpbatz_1.x86_64.rpm
  ```

### Run the sample

The executable is installed in `/usr/bin/helloworld-go`, and can be run as such in redpesk OS:

```bash
[root@localhost ~]# helloworld_go
Hello World !
```
