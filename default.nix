{ lib, stdenv, darwin, callPackage, python3Packages, nodejs-10_x }:

let
  nodeEnv = callPackage <nixpkgs/pkgs/development/node-packages/node-env.nix> {
    nodejs = nodejs-10_x;
    libtool = if stdenv.isDarwin then darwin.cctools else null;
  };

  solver = callPackage ./solver/node-packages.nix {
    inherit nodeEnv;
  };

in
with python3Packages;

buildPythonPackage rec {
  pname = "cloudpiercer";
  version = "0.1.0";
  src = lib.cleanSource ./.;
  propagatedBuildInputs = [
    aiohttp
  ];
  passthru = {
    solver = solver.package;
  };
}
