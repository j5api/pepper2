# This file exports nixpkgs with the overlay defined in ./overlay.nix enabled,
# so that you can simply do "nix-build -A pepper2" to build pepper2.

(import ../nixpkgs.nix).nixpkgs { overlays = [ (import ./overlay.nix) ]; }
