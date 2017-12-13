PIHOME=/home/pi
DEXTER=Dexter
DEXTER_PATH=$PIHOME/$DEXTER
RASPBIAN=$PIHOME/di_update/Raspbian_For_Robots
curl --silent https://raw.githubusercontent.com/DexterInd/script_tools/master/install_script_tools.sh | bash

# needs to be sourced from here when we call this as a standalone
source $PIHOME/$DEXTER/lib/$DEXTER/script_tools/functions_library.sh

# Check for a GoPiGo directory.  If it doesn't exist, create it.
GOPIGO_DIR=$DEXTER_PATH/GoPiGo
if folder_exists $GOPIGO_DIR; then
    echo "GoPiGo Directory Exists"
    cd $DEXTER_PATH/GoPiGo  # Go to directory
    git fetch origin       # Hard reset the git files
    git reset --hard
    git merge origin/master
else
    cd $DEXTER_PATH
    git clone https://github.com/DexterInd/GoPiGo
    cd $DEXTER_PATH/GoPiGo
fi
change_branch  $BRANCH # change to a branch we're working on.

pushd $DEXTER_PATH/GoPiGo/Setup > /dev/null
feedback "--> UPDATING LIBRARIES"
feedback "------------------"
bash ./install.sh
popd > /dev/null
