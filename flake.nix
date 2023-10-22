{
  description = "My website build environment";
  #nixConfig.bash-prompt = ''\n\[\033[1;32m\][\[\e]0;\]my-website\[: \w\a\]\u@\h:\w]\$\[\033[0m\]'';
nixConfig.bash-propmt-prefix = "website";
  inputs = { nixpkgs.url = "nixpkgs/nixos-unstable"; };

  outputs = { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux.pkgs;
      fooScript = pkgs.writeScriptBin "foo.sh" ''
        #!/bin/sh
        echo $FOO

      '';
pyopencv4 = pkgs.python311Packages.opencv4.override {
        enableGtk2 = true;
        gtk2 = pkgs.gtk2;
        #enableFfmpeg = true; #here is how to add ffmpeg and other compilation flags
        #ffmpeg_3 = pkgs.ffmpeg;
        };

    in {
      devShells.x86_64-linux.default = pkgs.mkShell {
        name = "My website environment";
        buildInputs = with pkgs; [
python311Packages.pip 
python311Packages.pyaudio
python311Packages.google-cloud-speech
python311Packages.pyserial
python311Packages.numpy
pyopencv4
#python311Packages.opencv4
        ];
        shellHook = ''
          source .venv/bin/activate
        '';
      };
    };
}

