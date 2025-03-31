{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.numpy
    python312Packages.pip
    python312Packages.pandas
    python312Packages.pytest
    stdenv.cc.cc.lib  # This provides libstdc++
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
  '';
}
