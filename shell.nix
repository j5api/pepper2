{
  pkgsSrc ? (fetchTarball https://nixos.org/channels/nixos-19.03/nixexprs.tar.xz),
  pkgs ? import pkgsSrc {},
}:

with pkgs;

stdenv.mkDerivation {
  name = "pepper2-dev-env";
  buildInputs = [
    gnumake
    python3
    python3Packages.poetry
    pkgconfig  # dependency of pygobject/pycairo
    cairo.dev  # dependency of pygobject/pycairo
    gobject-introspection.dev  # dependency of pygobject
    systemd.dev  # dependency of python-systemd
  ];

  # Without this, pygobject fails to build a wheel.
  # https://nixos.org/nixpkgs/manual/#python-setup.py-bdist_wheel-cannot-create-.whl
  shellHook = ''
    unset SOURCE_DATE_EPOCH
  '';
}
