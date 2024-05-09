#!/bin/sh
echo "$num"
p=$(pwd)
echo $p

cd ~
for i in {1..14}
do
	echo ""
        echo "** $i **"
	case ${i} in
		1) echo "updating ...."
		sudo apt update -y
		echo "...updated"
		;;
		2) echo "upgrading ....."
		sudo apt upgrade -y
		echo "...upgraded"
		;;
		3) echo "Installing python 3.8"
		py=$(python3.8 -V)
		py=${py:0:10}
		if [[ $py == "Python 3.8" ]]
		then
		echo "...Python 3.8 already installed"
		else
			sudo apt install python3.8
			py=$(python3.8 -V)
			py=${py:0:10}
			if [[ $py == "Python 3.8" ]]
			then
			echo "...Python 3.8 successfully installed"
			else
				echo "Python 3.8 not installed"
				exit 0
			fi
		fi
		;;
		4) echo "Installing Pip"
		pi=$(python3.8 -m pip -V)
		pi=${pi:(-4):(-1)}
		pp=${py:(-3)}
		if [[ $pi == $pp ]]
		then
		echo "...Pip already installed"
		else
			sudo apt install python3-pip -y
                	pi=$(python3.8 -m pip -V)
        	        pi=${pi:(-4):(-1)}
   	            	pp=${py:(-3)}
			if [[ $pi == $pp ]]
			then
			echo "...Pip successfully installed"
			else
				echo "Pip not installed"
				exit 0
			fi
		fi
		;;
		5) echo "Upgrading Pip"
		python3.8 -m pip install --upgrade pip
		echo $(python3.8 -m pip -V)
		echo "...Pip upgraded"
		;;
		6) echo "Installing ffmpeg"
		ffm=$(apt -qq list ffmpeg)
		ffm=${ffm:(-10):(-1)}
		if [[ $ffm == 'installed' ]]
		then
		echo "...ffmpeg already installed"
		else
			sudo apt install ffmpeg -y
			ffm=$(apt -qq list ffmpeg)
	                #ffm=${ffm:(-10):(-1)}
	                echo $ffm
			if [[ $ffm == *'installed'* ]]
			then
			echo "...ffmpeg successfully installed"
			else
				echo "ffmpeg install error"
				exit 0
			fi
		fi
		;;
		7)echo "Installing git..."
		git=$(apt -qq list git)
                #git=${git:(-10):(-1)}
                if [[ $git == *'installed'* ]]
		then
		echo "...Git already installed"
		else
			sudo apt install git -y
			git=$(apt -qq list git)
			git=${git:(-10):(-1)}
	                if [[ $git == 'installed' ]]
			then
			echo "... Git succssfully installed"
			else
				echo "Git install error"
				exit 0
			fi
		fi
		;;
		8)echo "cloning from github..."
		git clone-------------
		echo "...cloning complete"
		;;
		9)echo "Installing venv"
		ven=$(apt -qq list python*venv)
		#ven=${ven:(-10):(-1)}
		if [[ $ven == *'installed'* ]]
		then
		echo "...venv already installed"
                else
                        sudo apt install python3.8-venv -y
                        ven=$(apt -qq list python*venv)
                	#ven=${ven:(-10):(-1)}
			if [[ $ven == *'installed'* ]]
                        then
                        echo "...Venv successfully installed"
                        else
                                echo "Venv not installed"
                                exit 0
                        fi
                fi
		;;
		10)echo "creating virtual environment..."
		python3.8 -m venv firedet
		echo "...Virtual environment created"
		;;
		11) echo "Activating Environment..."
		. ./firedet/bin/activate
		ven=${VIRTUAL_ENV##*/}

		#ven=${ven:(-4)}
		echo $ven
		if [[ "$ven" == "firedet" ]]
		then
		python3.8 -m pip install --upgrade pip
		echo "...Virual Environment Activated"
		else
			echo "Virtual Environment Error"
			exit 0
		fi
		;;
		12)echo "Installing libgeos-dev..."
		sudo apt-get install libgeos-dev -y
		echo "...libgeos Installed"
		;;
		13)echo "Installing requirements.txt..."
		lib=$(cat ~/Documents/fyp/fyp_yolov8/requirements.txt|xargs)
		for i in $lib
		do
		pak=$(echo $i)
		pk=$(echo $i | cut -d "=" -f 1)
		chk=$(python3.8 -m pip show $pk 2>/dev/null)
		chk=${chk:0:4}
		if [[ $chk == "Name" ]]
		then
		echo "$pk already installed"
		echo ""
		else
		        python3.8 -m pip install $pak 2>/dev/null
		        chk=$(python3.8 -m pip show $pk 2>/dev/null)
		        chk=${chk:0:4}
		        if [[ $chk == "Name" ]]
		        then
		        echo "...Successfully installed"
		        echo ""
		        else
		                echo "** $pk installation error **"
		                echo ""
		        fi
		fi
		done
		echo "...Requirements.txt installed"
		;;
		14)echo "Running detection.py"
		cd ~/Documents/fyp/fyp_yolov8
		python detection_v8.py

		;;
	esac
done
echo "                             **********************"
echo "                             ***Set up Completed***"
echo "                             **********************"
