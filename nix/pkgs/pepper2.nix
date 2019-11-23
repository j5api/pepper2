# This file defines a derivation for the pepper2 python package.

{ buildPythonApplication, click, poetry, pydbus, pygobject3, python, systemd }:

buildPythonApplication {
  pname = "pepper2";
  version = "0.1.0";
  src = ../..;
  format = "pyproject";
  nativeBuildInputs = [ poetry ];
  propagatedBuildInputs = [ click pydbus pygobject3 systemd ];
  postInstall = ''
    install -D -m 0644 uk.org.j5.pepper2.conf -t $out/etc/dbus-1/system.d
  '';
}
