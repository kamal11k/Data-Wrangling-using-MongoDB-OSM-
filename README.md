# Data-Wrangling-using-MongoDB-OSM-
* Chose Kolkata city and used data munging techniques to assess the quality of the data for validity, accuracy, completeness, consistency
and uniformity.

* At first, to make analysis faster, I created a sample from the original XML file using create_sample.py .

* Then parsed the file through tags and audited unstructured street names, park names, PIN codes etc. audit.py demonstartes it.

* Updated these to proper readable format. Converted the XML file to JSON file .The updation can be viewed in data.py file.

* Imported to MongoDB database to run some exploratory queries against it. The file analysis.py contains some queries I performed
using pymongo and the final analysis is in the project_document.pdf .
