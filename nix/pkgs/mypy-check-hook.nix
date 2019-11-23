{ makeSetupHook, mypy }:
makeSetupHook {
  name = "mypy-check-hook";
  deps = [ mypy ];
  substitutions = {
    inherit mypy;
  };
} ./mypy-check-hook.sh
