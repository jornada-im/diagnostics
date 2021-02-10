
library(tidyverse)
library(curl)

# Create a data.frame of the current JRN data packages on EDI
# This only works for Searchable Fields that have one value per data package
# See https://pastaplus-core.readthedocs.io/en/latest/doc_tree/pasta_api/data_package_manager_api.html for additional Searachable Fields

jrn.curl <- curl::curl("https://pasta.lternet.edu/package/search/eml?defType=edismax&q=*&fq=scope:knb-lter-jrn&fl=packageid,doi,keyword,title,begindate,enddate,pubdate&rows=700")

# Create text object 
jrn.txt <- readLines(jrn.curl)

# Function to parse EML text
eml.parse <- function(field) {
  jrn.txt %>%
    grep(pattern = paste0("<",field)) %>%  # Find lines where field tag occurs
    jrn.txt[.] %>% # Subset the lines of interest
    strsplit(split = paste0("<",field,">|</",field,">")) %>% # Split the text strings by the field tags; this creates a list
    sapply("[", 2) # Select the second element in the list
  }

packageIDs <- eml.parse("packageid")
titles <- eml.parse("title")
begindates <- eml.parse("begindate")
enddates <- eml.parse("enddate")
pubdates <- eml.parse("pubdate")
dois <- eml.parse("doi")

# Create a data.frame
data.packages <- data.frame(packageID = packageIDs, title = titles, start_date = begindates, end_date = enddates, posting_date = pubdates, doi = dois, stringsAsFactors = FALSE)

setwd('~/GitHub/diagnostics/')
# Export as a CSV
write.csv(data.packages, paste0("tables_out/JRN_datapackages", Sys.Date(),".csv"), row.names = FALSE)

