###############################################################################
#                         LOAD PACKAGES AND MODULES                          #
###############################################################################

library(shiny)
library(shinydashboard)
library(dplyr)
library(leaflet)
library(ggplot2)
library(tidyverse)
library(DT)
library(plotly)
library(purrr)
library(glue)
library(rhandsontable)
library(tidyr)
library(shinyalert)
library(shinyjs)
library(supercaliheatmapwidget)
library(lubridate)
library(vistime)
library(timevis)
library(rmarkdown)



###############################################################################
#                               LOAD DATA                                     #
###############################################################################


# raw_data_tasks <- read.csv("./Data/task_tracker.csv")
#raw_data_projects <- read.csv("./Data/project_tracker.csv")
# raw_data_team <- read.csv("./Data/team_tracker.csv")
# raw_data_time <- read.csv("./Data/time_tracker.csv")
# raw_data_time$day <- dmy(raw_data_time$day)


#saveRDS(raw_data_projects,"Projects.rds")


raw_data_projects <- readRDS("Projects.rds")
raw_data_tasks <- readRDS("Tasks.rds")
   
