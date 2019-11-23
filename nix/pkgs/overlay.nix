# This file defines a nixpkgs overlay that includes pepper2 and related packages.

self: super: {
  pepper2 = self.callPackage ./pepper2.nix {
    inherit (self.python3Packages) buildPythonApplication click pydbus pygobject3 pytestCheckHook python systemd;
  };
}
