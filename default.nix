{ stdenv, lib, wrapGAppsHook4, gobject-introspection, gtk4, python3, brightnessctl }:

stdenv.mkDerivation {
  pname = "brightcontrol";
  version = "0.1.0";
  src = ./.;

  nativeBuildInputs = [ wrapGAppsHook4 gobject-introspection ];
  buildInputs = [ gtk4 (python3.withPackages (ps: [ ps.pygobject3 ])) ];

  dontBuild = true;
  installPhase = ''
    install -Dm755 brightcontrol.py $out/bin/brightcontrol
  '';

  preFixup = ''
    gappsWrapperArgs+=(--prefix PATH : ${lib.makeBinPath [ brightnessctl ]})
  '';
}
