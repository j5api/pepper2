# This file defines a nixpkgs overlay that includes pepper2 and related packages.

self: super: {
  python3Packages = super.python3Packages // {
    mypyCheckHook = self.callPackage ./mypy-check-hook.nix {
      inherit (self.python3Packages) mypy;
    };
  };
  pepper2 = self.callPackage ./pepper2.nix {
    inherit (self.python3Packages) buildPythonApplication click mypyCheckHook pydbus pygobject3 pytestCheckHook python systemd;
  };
}
