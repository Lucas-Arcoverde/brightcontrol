# nix-shell -> ambiente para rodar direto: python brightcontrol.py
{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  nativeBuildInputs = [ pkgs.wrapGAppsHook4 pkgs.gobject-introspection ];
  buildInputs = [
    pkgs.gtk4
    pkgs.brightnessctl
    (pkgs.python3.withPackages (ps: [ ps.pygobject3 ]))
  ];
}
