#! /bin/bash

PIHOME=/home/pi
DEXTER=Dexter
DEXTER_PATH=$PIHOME/$DEXTER
RASPBIAN=$PIHOME/di_update/Raspbian_For_Robots
GOPIGO_DIR=$DEXTER_PATH/GoPiGo
DEXTERSCRIPT=$DEXTER_PATH/lib/Dexter/script_tools

# whether to install the dependencies or not (avrdude, apt-get, wiringpi, and so on)
installdependencies=true
updaterepo=true
install_pkg_scriptools=true

# the following 3 options are mutually exclusive
systemwide=true
userlocal=false
envlocal=false
usepython3exec=true

# the following option tells which branch has to be used
selectedbranch="master"

declare -a optionslist=("--system-wide")
# iterate through bash arguments
for i; do
  case "$i" in
    --no-dependencies)
      installdependencies=false
      ;;
    --no-update-aptget)
      updaterepo=false
      ;;
    --bypass-pkg-scriptools)
      install_pkg_scriptools=false
      ;;
    --user-local)
      userlocal=true
      systemwide=false
      declare -a optionslist=("--user-local")
      ;;
    --env-local)
      envlocal=true
      systemwide=false
      declare -a optionslist=("--env-local")
      ;;
    --system-wide)
      ;;
    develop|feature/*|hotfix/*|fix/*|DexterOS*|v*)
      selectedbranch="$i"
      ;;
  esac
done

# show some feedback for the GoPiGo
echo "  _____            _                                ";
echo " |  __ \          | |                               ";
echo " | |  | | _____  _| |_ ___ _ __                     ";
echo " | |  | |/ _ \ \/ / __/ _ \ '__|                    ";
echo " | |__| |  __/>  <| ||  __/ |                       ";
echo " |_____/ \___/_/\_\\\__\___|_|          _            ";
echo " |_   _|         | |         | |      (_)           ";
echo "   | |  _ __   __| |_   _ ___| |_ _ __ _  ___  ___  ";
echo "   | | | '_ \ / _\ | | | / __| __| '__| |/ _ \/ __| ";
echo "  _| |_| | | | (_| | |_| \__ \ |_| |  | |  __/\__ \ ";
echo " |_____|_| |_|\__,_|\__,_|___/\__|_|  |_|\___||___/ ";
echo "                                                    ";
echo "                                                    ";
echo "  ______  _____   _____  _____  ______  _____ "
echo " |  ____ |     | |_____]   |   |  ____ |     |"
echo " |_____| |_____| |       __|__ |_____| |_____|"
echo " "

# show some feedback on the console
if [ -f $DEXTERSCRIPT/functions_library.sh ]; then
  source $DEXTERSCRIPT/functions_library.sh
  feedback "Welcome to GoPiGo Installer."
else
  echo "Welcome to GoPiGo Installer."
fi
echo "Updating GoPiGo for $selectedbranch branch with the following options:"
([[ $installdependencies = "true" ]] && echo "  --no-dependencies=false") || echo "  --no-dependencies=true"
([[ $updaterepo = "true" ]] && echo "  --no-update-aptget=false") || echo "  --no-update-aptget=true"
([[ $install_pkg_scriptools = "true" ]] && echo "  --bypass-pkg-scriptools=false") || echo "  --bypass-pkg-scriptools=true"
echo "  --user-local=$userlocal"
echo "  --env-local=$envlocal"
echo "  --system-wide=$systemwide"

# in case the following packages are not installed and `--no-dependencies` option has been used
if [[ $installdependencies = "false" ]]; then
  command -v git >/dev/null 2>&1 || { echo "I require \"git\" but it's not installed. Aborting." >&2; exit 1; }
  command -v python >/dev/null 2>&1 || { echo "Executable \"python\" couldn't be found. Don't use --no-dependencies option. Aborting." >&2; exit 2; }
  command -v python3 >/dev/null 2>&1 || { echo "Executable \"python3\" couldn't be found. Don't use --no-dependencies option. Aborting." >&2; exit 3; }
  command -v pip >/dev/null 2>&1 || { echo "Executable \"pip\" couldn't be found. Don't use --no-dependencies option. Aborting." >&2; exit 4; }
  command -v pip3 >/dev/null 2>&1 || { echo "Executable \"pip3\" couldn't be found. Don't use --no-dependencies option. Aborting." >&2; exit 5; }
fi

# create rest of list of arguments for script_tools call
optionslist+=("$selectedbranch")
[[ $usepython3exec = "true" ]] && optionslist+=("--use-python3-exe-too")
[[ $updaterepo = "true" ]] && optionslist+=("--update-aptget")
[[ $installdependencies = "true" ]] && optionslist+=("--install-deb-deps")
[[ $install_pkg_scriptools = "true" ]] && optionslist+=("--install-python-package")

echo "Options used for script_tools script: \"${optionslist[@]}\""

# update script_tools first
curl --silent -kL dexterindustries.com/update_tools > $PIHOME/tmp_script_tools.sh
echo "Installing script_tools. This might take a while.."
bash $PIHOME/tmp_script_tools.sh ${optionslist[@]} > /dev/null
rm $PIHOME/tmp_script_tools.sh

# HAVE TO UNCOMMENT ONCE check_internet makes it to script_tools
# check if there's internet access,
# otherwise straight out exit the script
# check_internet

# needs to be sourced from here when we call this as a standalone
source $DEXTERSCRIPT/functions_library.sh

# create folders recursively if they don't exist already
mkdir -p $DEXTER_PATH
cd $DEXTER_PATH

# it's simpler and more reliable (for now) to just delete the repo and clone a new one
# otherwise, we'd have to deal with all the intricacies of git
sudo rm -rf $GOPIGO_DIR
git clone --quiet --depth=1 -b $selectedbranch https://github.com/DexterInd/GoPiGo.git
cd $GOPIGO_DIR

echo "Installing GoPiGo dependencies and package. This might take a while.."

# installing dependencies
pushd $GOPIGO_DIR/Setup > /dev/null
sudo chmod +x install.sh
[[ $installdependencies = "true" ]] && sudo bash ./install.sh
popd > /dev/null

install_python_packages() {
  [[ $systemwide = "true" ]] && sudo python setup.py install --force \
              && [[ $usepython3exec = "true" ]] && sudo python3 setup.py install --force
  [[ $userlocal = "true" ]] && python setup.py install --force --user \
              && [[ $usepython3exec = "true" ]] && python3 setup.py install --force --user
  [[ $envlocal = "true" ]] && python setup.py install --force \
              && [[ $usepython3exec = "true" ]] && python3 setup.py install --force
}

# remove old libraries, as Mutex is being searched in here instead of
# the proper place - this will only work with system-wide packages,
# which was the original way of installing packages and still is
sudo pip uninstall gopigo -y > /dev/null
sudo pip3 uninstall gopigo -y > /dev/null

# installing the package itself
pushd $GOPIGO_DIR/Software/Python > /dev/null
install_python_packages
popd > /dev/null

# installing the DHT package
pushd $GOPIGO_DIR/Software/Python/sensor_examples/dht/Adafruit_Python_DHT > /dev/null
install_python_packages
popd > /dev/null
