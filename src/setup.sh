#!/bin/bash

# optional arg: <path_to_bashrc>

echo "Installing dependency"
pip install -r ../requirements.txt

splt_path="`pwd`/splt"
chmod +x $splt_path

if [ $1 ]; then
  bashrc_path="$1"
else
  bashrc_path="$HOME/.bash_profile"
fi

echo "Append 'splt' to path? Enter (y/n):"
read -n 1 resp
if [ "$resp" == 'y' ] || [ "$resp" == 'Y' ]; then
  printf '\n# Added by splter\n' >> $bashrc_path
  echo "export PATH=\$PATH:$splt_path" >> $bashrc_path
  echo "alias splt=$splt_path" >> $bashrc_path
  echo "Appended 'splt' command to path"
fi

source $bashrc_path

echo "Setup complete."
