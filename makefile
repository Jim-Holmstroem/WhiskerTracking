
PWD=`pwd`

install:
	echo "global ROOT_DIRECTORY\nROOT_DIRECTORY='${PWD}'\n" > src/common/settings_machine_specific.py

