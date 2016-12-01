Usage:

* Copy the csv file from the labview output to the data files
* Add the information in the data.py file. Here is a copy of the header explaining how to use:

	  The lines here follow an EXCEL style: the first line in the CSV file is number 2 and the first and last line are included in the averages
	  You create a new data taking period by using

	       dataInfo(title, csvfile, channels)

	  and then the method

	      addCondition(power, firstLine, lastLine)

	  Channels encodes the entries as defined in the labview code used to acquire the data. It is written in the channels.py file with a ROOT tree notation.
	  Temperature measurments are encoded by the channels defined above. The following have to be defined:

	      coolant
	      tubing
              triangle
              backplate
              sensor
              module
              ambient

* You may have to create another channel description in the channels.py file
* I still have to think how to add different setups. I think in a next version, I will make the plots configurable.


