{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.numpy
    python312Packages.pip
    python312Packages.pandas
    python312Packages.pytest
  ];

}
