#!/bin/bash


echo "[*] Welcome to Jacobi Viewer for Moloch"
echo "[*] Below you will see predetermined queries for network analysis"
echo "[*] Please select a query and give the appropriate input to open a Google Chrome session with the selected view"
echo ""

PS3='Please select your query '
options=("Characterization of network bandwidth usage" \
 	"Time traffic is at its highest levels" \
	"Time traffic is at its lowest levels" \
	"Inbound Connections" \
	"Outbound Connections" \
	"Key Terrain to Key Terrain Connections" 
	"Quit")
suboptions=("Last Hour" \
	  "Last 6 Hours" \
	  "Custom Start/End Time" 
	  "Quit")
select opt in "${options[@]}"
do 
	case $opt in
		"Characterization of network bandwidth usage")
			select subopt in "${suboptions[@]}"
			do
				case $subopt in 
					"Last Hour") 
						google-chrome "http://192.168.108.136:8005/sessions?date=1" 2>/dev/null ;;
					"Last 6 Hours")
						google-chrome "http://192.168.108.136:8005/sessions?date=1" 2>/dev/null ;;
					"Custom Start/End Time")						
						echo "Please enter start time"
						read starttime
						echo "Please enter end time"
						read endtime
						google-chrome "http://192.168.108.136:8005/sessions?stopTime=$starttime&startTime=$endtime" 2>/dev/null &
						break 2 ;;
					"Quit")
						echo "Back to selecting queries"
						break ;;
				esac
			done
			
			echo "Query 1 output string is $opt/$subopt" ;;
			
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

