###############################################################################
#                         LOAD PACKAGES AND MODULES                          #
###############################################################################

library(shiny)
library(shinydashboard)
library(dplyr)
library(ggplot2)
library(tidyverse)
library(shinycssloaders)
library(shinythemes)
library(lubridate)
library(shinyWidgets)




###############################################################################
#                               LOAD DATA                                     #
###############################################################################

# Download data set from the site -- https://hub.arcgis.com/datasets/66d96f15d4e14e039caa6134e6eab8e5_0

#crash <- read.csv("Los_Angeles_Collisions_2012through2018.csv",stringsAsFactors = FALSE)

crash$ymd <- crash$collision_date
crash$month <- month(crash$ymd, label = TRUE)
crash$year <- crash$accident_year
crash$wday <- wday(crash$ymd, label = TRUE)
crash$hour <- crash$Hours


crash$day_of_week[crash$day_of_week == "1"] <- "Monday"
crash$day_of_week[crash$day_of_week == "2"] <- "Tuesday"
crash$day_of_week[crash$day_of_week == "3"] <- "Wednesday"
crash$day_of_week[crash$day_of_week == "4"] <- "Thursday"
crash$day_of_week[crash$day_of_week == "5"] <- "Friday"
crash$day_of_week[crash$day_of_week == "6"] <- "Saturday"
crash$day_of_week[crash$day_of_week == "7"] <- "Sunday"


crash$alcohol_involved[crash$alcohol_involved == "Y"] <- TRUE
crash$alcohol_involved[crash$alcohol_involved == "N" |crash$alcohol_involved == "" ] <- FALSE

crash$intersection[crash$intersection == "Y"] <- TRUE
crash$intersection[crash$intersection == "N" | crash$intersection == ""] <- FALSE

crash$pedestrian_accident[crash$pedestrian_accident == "Y"] <- TRUE
crash$pedestrian_accident[crash$pedestrian_accident == "N"] <- FALSE

crash$bicycle_accident[crash$bicycle_accident == "Y"] <- TRUE
#crash$bicycle_accident[crash$bicycle_accident == "N"] <- FALSE

crash$motorcycle_accident[crash$motorcycle_accident == "Y"] <- TRUE
crash$motorcycle_accident[crash$motorcycle_accident == "N"] <- FALSE

crash$truck_accident[crash$truck_accident == "Y"] <- TRUE
#crash$truck_accident[crash$truck_accident == "N"] <- FALSE



df_crash <- crash %>% 
  group_by(accident_year, month, day_of_week, collision_severity, number_injured,number_killed, hit_and_run, pedestrian_accident,bicycle_accident, motorcycle_accident,truck_accident) %>% 
  summarise(cnt = n())


dataMap1 <- read.csv("collapse_tree.csv") 
LA_crash <- data.frame(lapply(dataMap1,as.character), stringsAsFactors = FALSE  )










