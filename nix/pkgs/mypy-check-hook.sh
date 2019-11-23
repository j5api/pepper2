# Setup hook for mypy
echo "Sourcing mypy-check-hook.sh"

declare -ar mypyPaths

function mypyCheckPhase() {
  echo "Executing mypyCheckPhase"
  runHook preMypyCheck

  mypyPathsStr="${mypyPaths[@]}"
  if [ -z "$mypyPathsStr" ]; then
    mypyPathsStr="."
  fi
  @mypy@/bin/mypy $mypyPathsStr

  runHook postMypyCheck
  echo "Finished executing mypyCheckPhase"
}

if [ -z "$dontUseMypyCheck" ] && [ -z "$installCheckPhase" ]; then
  echo "Using mypyCheckPhase"
  preDistPhases+=" mypyCheckPhase"
fi
