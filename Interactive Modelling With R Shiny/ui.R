

library(shiny)
library(shinydashboard)
library(maps)
library(dplyr)
library(leaflet)
library(shinycssloaders)
library(shinythemes)
library(datadigest)
library(rio)
library(DT)
library(stargazer)


dashboardPage(
  dashboardHeader(title = "Machine Learning", dropdownMenuOutput("msgOutput")),
  dashboardSidebar(
    sliderInput(
      "Slider1",
      label = h3("Train/Test Split %"),
      min = 0,
      max = 100,
      value = 75
    ),
    textOutput("cntTrain"),
    textOutput("cntTest"),
    br()
    
    #
    # menuItem(
    #   "Generate Report",
    #   tabName = "sectors",
    #   icon = icon("download"),
    #   radioButtons(
    #     'format',
    #     'Document format',
    #     c('HTML', 'Word'),
    #     inline = FALSE,
    #     selected = 1
    #   ),
    #   downloadButton("report", "Download Report", class = "butt"),
    #   tags$head(tags$style(".butt{color: blue !important;}"))
    # )
    
  ),
  dashboardBody(
    fluidPage(
    box(
      selectInput(
        "SelectX",
        label = "Select variables:",
        choices = names(mtcars),
        multiple = TRUE,
        selected = names(mtcars)
      ),
      solidHeader = TRUE,
      width = "3",
      status = "primary",
      title = "X variable"
    ),
    box(
      selectInput("SelectY", label = "Select variable to predict:", choices = names(mtcars)),
      solidHeader = TRUE,
      width = "3",
      status = "primary",
      title = "Y variable"
    )
    
    
    
  ),
  
  fluidPage(  
    
      tabBox(
      id = "tabset1",
      height = "1000px",
      width = 12,
     
      tabPanel("Data",
               box(withSpinner(DTOutput(
                 "Data"
               )), width = 12)),
      tabPanel(
        "Data Summary",
        box(withSpinner(verbatimTextOutput("Summ")), width = 6),
        box(withSpinner(verbatimTextOutput("Summ_old")), width = 6)
      ),
      
      # 
      # tabPanel("Data Strucure",
      #          # box(
      #          #   withSpinner(verbatimTextOutput("structure")), width = "100%"
      #          # ),
      #          explorerOutput("digest")
      #          ),
      tabPanel("Plots",
               box(withSpinner(plotOutput(
                 "Corr"
               )), width = 12)),
      #box(withSpinner(verbatimTextOutput("CorrMatrix")), width = 12),
      tabPanel(
        "Model",
        box(
          withSpinner(verbatimTextOutput("Model")),
          width = 6,
          title = "Model Summary"
        ),
        # box(
        #   withSpinner(verbatimTextOutput("Model_new")),
        #   width = 6,
        #   title = "Model Summary"
        # ),
        # 
        box(
          withSpinner(verbatimTextOutput("ImpVar")),
          width = 5,
          title = "Variable Importance"
        )
      ),
      #textOutput("correlation_accuracy"),
      tabPanel(
        "Prediction",
        box(withSpinner(plotOutput("Prediction")), width = 6, title = "Best Fit Line"),
        box(withSpinner(plotOutput("residualPlots")), width = 6, title = "Diagnostic Plots")
      )
    )
  )
  )
)
