echo "Updating commandline interface"
sudo cp -Rf bin/* /bin/
sudo chmod 0777 /bin/jarvis

echo "Copying Library"
mkdir $HOME/.jarvis
cp -Rf lib/* $HOME/.jarvis
