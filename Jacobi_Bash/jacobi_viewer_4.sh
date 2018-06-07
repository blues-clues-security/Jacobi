#!/bin/bash
set -x
function query_1 {
	
	times=("Specify Start/End Date & Time" \
		   	  "Hours Ago" 
		   	  "Quit")
	echo ""
	echo "This query will examine KT-C to KT-C connections"

	select time in "${times[@]}"
	do
		case $time in
			"Specify Start/End Date & Time")
				local startTime=""
				local endTime=""				
				echo "Enter Date/Time in format: YYYY/MM/DD HH:MM:SS"
				echo "Start Time"				
				#while [[ ! $startTime=~ (0-3)[0-9]		#Need to add input validation, just dont feel like doing regexp atm
				read startTime
				echo ""
				echo "End Time"
				#while [[ ! $endTime=~ (0-3)[0-9]		#Need to add input validation, just dont feel like doing regexp atm
				read endTime
				#google-chrome "http://192.168.108.136:8005/sessions?stopTime=$starttime&startTime=$endtime" 2>/dev/null &		#Only after the IP is entered does a browser need to be opened
				break ;;
			"Hours Ago")
				local startHours=""				
				echo "How many hours back do you want to start analysis?"
				read startHours	
				#google-chrome "http://192.168.108.136:8005/sessions?date=$startHours" 2>/dev/null &		#Only after the IP is entered does a browser need to be opened
				echo ""			
				break ;;
			"Quit")
				echo "Select another query"			
				break ;;
			*) echo "My responses are limited, you must ask the right questions..."
		 		echo "";;
		esac
	done

	echo "Select the appropriate IP options"
	ips=("Specify targets file" \
		   	"Specify CIDR notation"
		   	"Quit")

	select ip in "${ips[@]}"	
	do
		case $iptoption in 
			"Specify targets file")
				local ipTargs=""
				local ipTargsList=""
				echo "Enter the absolute path to the appropriate targets file (NOTE* file must be line break delimited)"				
				read ipTargs
				cat ipTargs | head -n 1 > ipTargsList
				if [ $startHours -neq 0 ]; then
					google-chrome "http://192.168.108.136:8005/sessions?date=$startHours&expression=ip.src%3D%3D$ipTargs" 2>/dev/null &
				else
					google-chrome "http://192.168.108.136:8005/sessions?stopTime=$starttime&startTime=$endtime&expression=ip.src%3D%3D$ipTargs" 2>/dev/null &
				fi
				break ;;
			"Specify CIDR notation")
				echo "cidr"
				local cidr=""
				echo "Please enter information in the format XXX.XXX.XXX.XXX/XX"
				read cidr
				echo cidr | cut -f2 -d"/"
				break ;;
			"Quit")
				echo "Select another query"			
				break ;;
		esac
	done
}

echo "[*] Welcome to Jacobi Viewer for Moloch"
echo "[*] Below you will see predetermined queries for network analysis"
echo "[*] Please select a query and give the appropriate input to open a Google Chrome session with the selected view"
echo ""

PS3='Please select your query '
options=("Key Terrain to Key Terrain connections" \
 	"Time traffic is at its highest levels" \
	"Time traffic is at its lowest levels" \
	"Inbound Connections" \
	"Outbound Connections" \
	"Key Terrain to Key Terrain Connections" 
	"Quit")
select opt in "${options[@]}"
do 
	case $opt in
		"Key Terrain to Key Terrain connections")
			
			query_1	;;		
			
		"Time traffic is at its highest levels")
			echo "Query 2 output string is: $opt" 
			google-chrome "http://moloch.url1" 2>/dev/null & ;;

		"Time traffic is at its lowest levels")
			echo "Query 3 output string is: $opt" 
			google-chrome "http://moloch.url1" 2>/dev/null & ;;

		"Inbound Connections")
			echo "Query 3 output string is: $opt" 
			google-chrome "http://moloch.url1" 2>/dev/null & ;;

		"Outbound Connections")
			echo "Query 3 output string is: $opt" 
			google-chrome "http://moloch.url1" 2>/dev/null & ;;


		"Key Terrain to Key Terrain Connections")
			echo "Query 3 output string is: $opt" 
			google-chrome "http://moloch.url1" 2>/dev/null & ;;


		"Quit")
			echo "Later nerd"			
			break ;;
		*) echo "My responses are limited, you must ask the right questions..."
		   echo "" ;;
	esac
done

