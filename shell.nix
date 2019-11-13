{
  pkgsSrc ? <nixpkgs>,
  pkgs ? import pkgsSrc {},
}:

with pkgs;

stdenv.mkDerivation {
  name = "pepper2-dev-env";
  buildInputs = [
    gnumake
    python3
    python3Packages.poetry
  ];
}