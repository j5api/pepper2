# This file defines a nixpkgs overlay that includes pepper2 and related packages.

self: super: {
  python3Packages = super.python3Packages // {
    pygobject3 = super.python3Packages.pygobject3.overridePythonAttrs rec {
      version = "3.34.0";
      src = self.python3Packages.fetchPypi {
        pname = "PyGObject";
        inherit version;
        sha256 = "0hy5w15718xsz1sl4zsz5zp9ycsk20yw4v06a87sj8rs5fphvjra";
      };
    };
    pydbus = super.python3Packages.pydbus.override { inherit (self.python3Packages) pygobject3; };
  };
  pepper2 = self.callPackage ./pepper2.nix {
    inherit (self.python3Packages) buildPythonApplication click pydbus pygobject3 python systemd;
  };
}
