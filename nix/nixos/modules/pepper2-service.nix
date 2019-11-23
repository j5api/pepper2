# This files defines a "services.pepper2" module in NixOS that runs pepperd.

{ config, pkgs, lib, ... }:

with lib;
let
  cfg = config.services.pepper2;
  pepper2 = pkgs.pepper2;

in {
  options.services.pepper2 = {
    enable = mkEnableOption "pepper2 daemon";
  };

  config = mkIf cfg.enable {
    environment.systemPackages = [ pepper2 ];
    systemd.services.pepper2 = {
      description = "pepper2 daemon";
      wantedBy = [ "multi-user.target" ];
      script = "${pepper2}/bin/pepperd --verbose";
    };
    services.dbus.packages = [ pepper2 ];
  };
}
