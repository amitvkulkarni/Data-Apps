setwd("C:/Users/kulkarna4029/OneDrive - ARCADIS/Studies/R/Code Orange")


shinyServer(function(input, output, session){ 

  
  InputDataset <- reactive({observe({print(input$selectData)})
    
    if(input$selectData == "crash"){
      dt <- crash
    }
    
    
  })
  
  
  yearSelect <- reactive({observe({print(input$selectYear)})
    
    yearSelect <- input$selectYear
    
  })
  

  output$Data <- DT::renderDataTable(InputDataset())
  
  Collap_tree <- reactive({collapsibleTree(LA_crash, c("Category","Column", "Data_type", "Summary"), collapsed = TRUE, fill = "lightsteelblue", zoomable = TRUE, width = 800)})
  output$DataMap <- renderCollapsibleTree(Collap_tree())
  
  output$dataStructure <- renderPrint(str(InputDataset()))
  output$dataSummary <- renderPrint(summary(InputDataset()))
 # output$univariate <- renderPlot(plot_histogram(InputDataset()))

  
  
  
  ###############################################################################
  #                 Crash Analysis tab :Filter data by selected year            #
  ############################################################################### 
  df_crashAnalysis_year <- reactive({#observe({print(input$selectYear)})
    if (!is.null(input$selectYear)) {
      collision_year <- InputDataset() %>% 
        filter(InputDataset()$accident_year %in% input$selectYear)
    }
    else
      collision_year <- InputDataset()
        
  })
  
  
  
  output$yearSelect <- renderValueBox({
    valueBox(
      value = tags$p(nrow(df_crashAnalysis_year()), style = "font-size: 75%;"),
      subtitle = tags$p("Collisions for selected year", style = "font-size: 125%;"),
      icon = icon("fas fa-calendar-alt")
    )
  })
  

  ##############################################################################################
  #                 Crash Analysis tab :dataframe prepration for the valuebox loading           #
  ##############################################################################################
  
  df_crashAnalysis_days <- reactive({#observe({print(input$severity)})
    if(input$days == 2){
      collision_days <- InputDataset() %>%
          filter(InputDataset()$day_of_week %in% c("Monday", "Tuesday", "Wednesday", "Thursday","Friday"),
                 InputDataset()$accident_year == input$selectYear)
                 
    }
    else if(input$days == 3){
      collision_days <- InputDataset() %>%
          filter(InputDataset()$day_of_week %in% c("Saturday", "Sunday"),
                 InputDataset()$accident_year == input$selectYear)
                 
      }
    else if(input$days == 1){
      collision_days <- InputDataset() %>%
          filter(InputDataset()$accident_year == input$selectYear)
                 
      }

  })

  #   filter(accident_year %in% c(2006,2007))
  
  df_crashAnalysis_history <- reactive({#observe(print(input$chkIntersection))
    if(input$days == 2){
      if (!is.null(input$selectYear)) {
        collision_days <- InputDataset() %>%
          filter(InputDataset()$day_of_week %in% c("Monday", "Tuesday", "Wednesday", "Thursday","Friday"), 
                 InputDataset()$collision_severity == input$severity,
                 InputDataset()$alcohol_involved == input$chkAlcohol,
                 InputDataset()$intersection == input$chkIntersection,
                 InputDataset()$accident_year %in% input$selectYear)

      }
      else{
        collision_days <- InputDataset() %>%
          filter(InputDataset()$day_of_week %in% c("Monday", "Tuesday", "Wednesday", "Thursday","Friday"), 
                 InputDataset()$collision_severity == input$severity,
                 InputDataset()$alcohol_involved == input$chkAlcohol,
                 InputDataset()$intersection == input$chkIntersection)
                 
      }
 
      
    }
    else if(input$days == 3){
      if(!is.null(input$selectYear)){
        collision_days <- InputDataset() %>%
          filter(InputDataset()$day_of_week %in% c("Saturday", "Sunday"),
                 InputDataset()$collision_severity == input$severity,
                 InputDataset()$alcohol_involved == input$chkAlcohol,
                 InputDataset()$intersection == input$chkIntersection,
                 InputDataset()$accident_year %in% input$selectYear)
      }
      else{
        collision_days <- InputDataset() %>%
          filter(InputDataset()$day_of_week %in% c("Saturday", "Sunday"),
                 InputDataset()$collision_severity == input$severity,
                 InputDataset()$alcohol_involved == input$chkAlcohol,
                 InputDataset()$intersection == input$chkIntersection)
                 
      }

      
    }
    else{ 
      if(!is.null(input$selectYear)){observe(print(input$selectYear))
        collision_days <- InputDataset() %>%
          filter(InputDataset()$collision_severity == input$severity,
                 InputDataset()$alcohol_involved == input$chkAlcohol,
                 InputDataset()$intersection == input$chkIntersection,
                 InputDataset()$accident_year %in% input$selectYear)
      }
      else{
        collision_days <- InputDataset() %>%
          filter(InputDataset()$collision_severity == input$severity,
                 InputDataset()$alcohol_involved == input$chkAlcohol,
                 InputDataset()$intersection == input$chkIntersection)
                 
      }

    }
    
  })
  

  
  
  crashAnalysis_history <- reactive({

      df_crashAnalysis_history() %>%
      group_by(df_crashAnalysis_history()$accident_year) %>%
      summarize(Mean = n()) %>%
      summarize(Avg = mean(Mean))

  })
    
  
  output$yearMean <- renderValueBox({
    valueBox(
      value = tags$p(round(crashAnalysis_history(),0), style = "font-size: 75%;"),
      subtitle = tags$p("Number of collisions for selected factors", style = "font-size: 125%;"),
      icon = icon("fas fa-ambulance")
    )
  })

  
  ###############################################################################
  #      Crash Analysis trends over all years                                   #
  ###############################################################################
  
  #Crash analysis over the years
  
  
  output$TrendsAllYears <- renderPlot(
    ggplot(df_crash, aes(x= df_crash$accident_year))+
      geom_bar(color="blue", fill="steelblue", width = 0.5)+ 
      labs(title = "Collision Trends Over Years", subtitle = "Los Angeles: 2006-2019") + 
      xlab("years") + ylab("Number of collisions") +
      theme_minimal()
  )
  

  
  ###############################################################################
  #      Crash Analysis trends over all days based on user selection            #
  ###############################################################################
  
  # crash analysis daywise
  df_dayCrash <-   df_crash %>% 
    group_by(day_of_week) %>% 
    summarise(sum(cnt)) 
  
  
  # To ensure the weekdays are in specific order on the bar chart
  x <- c("Monday","Tuesday", "Wednesday","Thursday","Friday", "Saturday","Sunday")
  df_dayCrash$day_of_week <- factor(df_dayCrash$day_of_week,x)
  
  output$TrendsWeeks <- renderPlot(
    ggplot(df_dayCrash, aes(x= df_dayCrash$day_of_week, y = df_dayCrash$`sum(cnt)`)) +
      geom_bar(stat = "identity", fill = "steelblue", width = 0.3)+
      labs(title = "Collision Trends Day Wise", subtitle = "Los Angeles") +
      xlab("Days") + ylab("Number of collisions 2006-2019") +
      theme_minimal()
    

  )
  
  
  ##############################################################################################
  #      Crash Analysis: Pie chart for severity for selected year / weekdays / weekend        #
  ##############################################################################################
  
 
  output$TrendsAllYears <-  renderPlot(
    ggplot(df_crash, aes(df_crash$accident_year, df_crash$cnt), xlab("Years") + ylab("Number of collision")) +
      geom_bar(stat = "identity", width = 0.5, fill = "steelblue")+
      theme_classic() + xlab("Year") + ylab("COunt of colissions")
  )
  


  ##############################################################################################
  #      Crash Analysis: Code for heat map for day and hourly split      #
  ##############################################################################################

  
  #Assign color variables
  col1 = "#AED6F1"
  col2 = "#21618C"


  dayHour <- reactive({
    df_crashAnalysis_history() %>% 
    group_by(hour, wday) %>% 
    select("hour", "wday") %>% 
    summarize(N = n())
  })
  


  output$timeDay <- renderPlot(

    ggplot(dayHour(), aes(dayHour()$hour, dayHour()$wday)) + geom_tile(aes(fill = N),colour = "white", na.rm = TRUE) +
      scale_fill_gradient(low = col1, high = col2) +
      guides(fill=guide_legend(title="Total Incidents")) +
      theme_bw() + theme_minimal() +
      labs(title = "Heat map of Los Angeles collision by Day of Week and Hour",
           x = "Collisions Per Hour", y = "Day of Week") +
      theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())
  )

  
  yearMonth <- crash %>% 
    group_by(year,month) %>% 
    select("year", "month") %>% 
    summarize(N = n())
  
  output$yearMonth <- renderPlot(
  
  ggplot(yearMonth, aes(year, month)) + geom_tile(aes(fill = N),colour = "white") +
    scale_fill_gradient(low = col1, high = col2) +
    guides(fill=guide_legend(title="Total Collisions")) +
    labs(title = "Heat map of Los Angeles collisions by Month and Year",
         x = "Year", y = "Month") +
    theme_bw() + theme_minimal()
)

  
  
  
})




