
dashboardPage(
  
  dashboardHeader(
    title = "Los Angeles Crash Analysis"
  ),
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("Select Data", tabName = "Summary", icon = icon("dashboard"),selectInput("selectData", label = h4("Select DataSet"),choices = list("crash"), selected = 1)
      )
    )


  ),
  
  dashboardBody(
    h1("CRASH ANALYSIS FOR THE CITY OF LOS ANGLES YEARS: 2006 TO 2019", style="color:#3498DB; text-align:center"),
    
    fluidRow(
      tabBox(id = "tabset1", width = 12, height = "1400px",
             

             tabPanel(tags$b("Crash Analysis"),
                      
                      box(
                        selectInput("selectYear", label = h5(tags$b("Select Year")),choices = list("2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019"), selected = 1, multiple = TRUE),
                        
                        radioButtons("days", label = h5(tags$b("Weekday / Weekend")),inline = TRUE,
                                     choices = list("All" = 1, "Weekdays" = 2, "Weekend" = 3), 
                                     selected = 2),
                        
                        radioButtons("severity", label = h5(tags$b("Severity of collision")),inline = FALSE,
                                     choices = list("All" = 0, "Fatal" = 1, "Major" = 2, "Minor" = 3, "Injuries" = 4), 
                                     selected = 0),
                        
                        h5(tags$b("Other Factors")),
                        checkboxInput("chkAlcohol", label = "Alcohol Involved", value = FALSE),
                        checkboxInput("chkIntersection", label = "Intersection", value = FALSE),
                        
                        solidHeader = TRUE, status = "primary", width = 3, title = "Motor Vechicle Collision Analysis", collapsible = TRUE
                      ),
                      box(
                        valueBoxOutput("yearSelect", width = 5),
                        
                        valueBoxOutput("yearMean", width = 5),
                        
                        
                        collapsible = TRUE, solidHeader = TRUE, status = "primary", width = 5, title = "Motor Vechicle Collision Analysis"
                      ),
                      box(
                        withSpinner(plotOutput("timeDay")),
                        withSpinner(plotOutput("yearMonth")),
                        collapsible = TRUE, solidHeader = TRUE, status = "primary", width = 5, title = "Year / Month / hourly trends"
                      ),
                      box(collapsible = TRUE, solidHeader = TRUE, status = "primary", width = 4, title = "Collision trends over the years",
                          
                          withSpinner(plotOutput("TrendsWeeks")),
                          withSpinner(plotOutput("TrendsAllYears"))
                      )
                      
                      
             )

      )
      
    )
  )
)




