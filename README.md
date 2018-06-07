# Jacobi

### Overview  
Jacobi is a way to get around typing out really long query strings or messing around with the interface too much in Moloch. [Moloch](https://github.com/aol/moloch) is a packet analysis tool similar to wireshark, but with an Elasticsearch back end and add on capabilities with Cyber Chef.  
### General Use  
This tool is intended to be a network hunt/baseline starting point. If you are already ingesting your PCAP into Moloch, then running these queries will highlight any traffic that requires further investigation. More queries will come with future releases, and I have the notes for more within the code as well. Happy hunting!  
### Setup  
Jacobi was written for Python 2.7. It doesn't require any other dependencies other than Moloch and Elasticsearch running. The current default browser is set to firefox (see line 276 to change) and the default Moloch location is http://localhost:8005 (see line 277 to change). Note that both of these configurations can be changed per session in the Global Variables menu.  
### Running  
Simply using "python jacobi.py" to start the script, and the menu options are fairly self explanatory. I've included a Help menu to try and explain a little more of the Global Variables and what exactly they do. Each individual query should have enough information in their menu to explain what is happening. If you really need to know more, you'll see the query in the URL it generates and can refer to the function call to find the code. Lastly, you'll notice a text file caled "jacobi_queries.txt" in the running folder. This is keeping track of: the query ran, the date/time, and the command ran to open the browser with the associated URL.  
### Noteworthy Bugs
The only issue I wasn't able to overcome, was the curses menu erroring when the terminal window is too small. I was able to add an Exception handler so the window won't crash, however you'll be prompted to resize the window before needing to restart the script. Let me know if you find anything else!  
