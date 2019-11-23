# This file defines a derivation for a QEMU VM image that contains
# a running instance of pepperd.

let
  topModule = { config, pkgs, lib, ... }: {
    imports = [
      ./modules/pepper2-service.nix
    ];
    nixpkgs.overlays = [ (import ../pkgs/overlay.nix) ];
    users = {
      mutableUsers = false;
      users = {
        root = { password = "root"; };
      };
    };
    services.pepper2 = {
      enable = true;
    };
  };
  nixos = (import ../nixpkgs.nix).nixos {
    configuration = topModule;
    system = "x86_64-linux";
  };
in nixos.vm
