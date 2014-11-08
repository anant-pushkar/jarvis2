echo "Creating commandline interface"
sudo cp -Rf bin/* /bin/
sudo chmod 0777 /bin/jarvis

echo "Copying Templates"
mkdir $HOME/Documents/jarvis
cp -Rf Documents/* $HOME/Documents/jarvis

echo "Copying Library"
mkdir $HOME/.jarvis
cp -Rf lib/* $HOME/.jarvis

echo "Creating workspace"
mkdir $HOME/jarvis_workspace/
mkdir $HOME/jarvis_workspace/c
mkdir $HOME/jarvis_workspace/cpp
mkdir $HOME/jarvis_workspace/python

echo "Install complete"
