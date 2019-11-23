# This file defines the source of truth for nixpkgs. Normally one would
# just import <nixpkgs>, but unfortunately poetry is broken on the latest nixpkgs
# release (19.09), so we explicitly fetch nixpkgs master instead.

rec {
  src = fetchTarball https://nixos.org/channels/nixpkgs-unstable/nixexprs.tar.xz;
  nixpkgs = import src;
  nixos = import (src + "/nixos");
}
