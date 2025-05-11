
RF_Partition <- function(data, year_start, year_end) {
  
  # Path
  RF_path <- paste0(output_path, "/RF_Gapfill")
  dir.create(RF_path, recursive = TRUE)
  
  # record output
  logf <- file(paste0(RF_path, "/logfile_RF_", run_id, ".txt"))
  sink(logf, type = "output", split = TRUE, append = TRUE)
  sink(logf, append=TRUE, type="message")
  
  # to do: partition NEE from RF gapfilled
  
  # start year is included, end year is NOT included
  df_RF <- data %>% 
    select(
      TIMESTAMP_MIDDLE, 
      USTAR, 
      LW_IN_T1_2_1, 
      PA_GF1_0.9_1, 
      PPFD_IN_T1_2_2, 
      VPD_T1_2_1, 
      SW_IN_T1_2_1,
      TA_T1_2_1, 
      RH_T1_2_1, 
      NEE_L3.1_L3.3_CUT_16_QCF_gfRF, 
      NEE_L3.1_L3.3_CUT_50_QCF_gfRF,
      NEE_L3.1_L3.3_CUT_84_QCF_gfRF,
      LE_L3.1_L3.3_CUT_NONE_QCF_gfRF,
      H_L3.1_L3.3_CUT_NONE_QCF_gfRF
      # Below optional
      # FETCH_90, 
      # RH_EP,
      # SW_IN_POT,
      # VPD_EP,
      # WS,
      # WD,
  )
  
  cat("Data selected \n")
  
  
  # Check timestamp
  cat("Check middle timestamp \n")
  print(head(df_RF$TIMESTAMP_MIDDLE))
  
  # Convert timestamp
  df_RF$TIMESTAMP_MIDDLE <- as.POSIXct(df_RF$TIMESTAMP_MIDDLE, format="%Y-%m-%d %H:%M:%S", tz = "Etc/GMT-1")
  df_RF$TIMESTAMP_END <- df_RF$TIMESTAMP_MIDDLE + minutes(15)
  
  # Check timestamp again
  print(head(df_RF$TIMESTAMP_MIDDLE))
  cat("Check end timestamp \n")
  print(head(df_RF$TIMESTAMP_END))
  print(str(df_RF))
  
  cat("Timestamp converted \n")
  assign("df_RF", df_RF, envir = .GlobalEnv)
  
  # stop and check using browser() 
  # type c in the console
  # Q is quite 
  
  # Prepare EddyProc data
  EddyData.F <- df_RF[FALSE]
  EddyData.F <- EddyData.F %>% 
    mutate(
    TIMESTAMP = df_RF$TIMESTAMP_END,
    NEE_U16 = as.numeric(as.character(df_RF$NEE_L3.1_L3.3_CUT_16_QCF_gfRF)),
    NEE_U50 = as.numeric(as.character(df_RF$NEE_L3.1_L3.3_CUT_50_QCF_gfRF)),
    NEE_U84 = as.numeric(as.character(df_RF$NEE_L3.1_L3.3_CUT_84_QCF_gfRF)),
    LE = as.numeric(as.character(df_RF$LE_L3.1_L3.3_CUT_NONE_QCF_gfRF)),
    H = as.numeric(as.character(df_RF$H_L3.1_L3.3_CUT_NONE_QCF_gfRF)),
    Ustar = as.numeric(as.character(df_RF$USTAR)),
    Rg = as.numeric(as.character(df_RF$SW_IN_T1_2_1)),
    Tair = as.numeric(as.character(df_RF$TA_T1_2_1)),
    RH = as.numeric(as.character(df_RF$RH_T1_2_1)),
    VPD = pmax(as.numeric(as.character(df_RF$VPD_T1_2_1)), 0)
    ) %>% 
    filter(TIMESTAMP >= as.POSIXct(paste0(year_start, '-01-01 00:30:00'))) %>%
    filter(TIMESTAMP <= as.POSIXct(paste0(year_end, '-01-01 00:00:00'))) %>%
    mutate(TIMESTAMP_STRING = as.character(TIMESTAMP)) %>%
    mutate(TIMESTAMP_STRING = ifelse(nchar(TIMESTAMP_STRING) == 10, 
                                     paste0(TIMESTAMP_STRING, " 00:00:00"), 
                                     TIMESTAMP_STRING))


  
  write.csv(EddyData.F, file = paste0(RF_path, "/RF_EddyDataF_", run_id, ".csv"), row.names = FALSE)
  cat("Input data check \n")
  print(str(EddyData.F))
  cat("Input data ready \n")
  assign("RFEddyData.F", EddyData.F, envir = .GlobalEnv)
  

  
  # REddyProc processing
  EddyProc.C <- sEddyProc$new('CH-CHA', EddyData.F,
                              c('NEE_U16', 'NEE_U50', 'NEE_U84', 'LE', 'H', 'Rg', 'Tair', 'Ustar', 'VPD'),
                              ColPOSIXTime = "TIMESTAMP")
  EddyProc.C$sSetLocationInfo(LatDeg = 47.210222, LongDeg = 8.410444, TimeZoneHour = 1)
  
  # Check data
  cat("Check REddyProc timestamp \n")
  print(str(str(EddyProc.C)))
  print(head(EddyProc.C$sDATA$sDateTime))
  print(head(EddyProc.C$sTEMP)) # Middle timestamp
  print(head(EddyProc.C$sDATA))
  
  cat("REddyProc ready \n")
  cat("Start MDS Gapfilling \n")
  
  
  
  # MDS Gap-filling
  EddyProc.C$sMDSGapFill('Tair', FillAll = FALSE)
  EddyProc.C$sMDSGapFill('Rg', FillAll = FALSE)
  EddyProc.C$sMDSGapFill('VPD', FillAll = FALSE)
  cat("Meteo gapfilled \n")
  
  EddyProc.C$sMDSGapFill('NEE_U16', FillAll = TRUE)
  cat("NEE_U16 gapfilled \n")
  
  EddyProc.C$sMDSGapFill('NEE_U50', FillAll = TRUE)
  cat("NEE_U50 gapfilled \n")
  
  EddyProc.C$sMDSGapFill('NEE_U84', FillAll = TRUE)
  cat("NEE_U84 gapfilled \n")
  
  EddyProc.C$sMDSGapFill('LE', FillAll = TRUE, isVerbose = TRUE)
  cat("LE gapfilled \n")
  
  EddyProc.C$sMDSGapFill('H', FillAll = TRUE, isVerbose = TRUE)
  cat("H gapfilled \n")
  
  # Calculate ET from LE (QC=0)
  EddyProc.C$sTEMP$ET_f <- fCalcETfromLE(EddyProc.C$sTEMP$LE_f, EddyProc.C$sTEMP$Tair_f)
  cat("ET calculated \n")
  
  assign("EddyProc.C", EddyProc.C, envir = .GlobalEnv)
  
  # Export filled data
  FillEddyData.F <- EddyProc.C$sExportResults()
  FillEddyData.F$TIMESTAMP <- EddyData.F$TIMESTAMP_STRING
  
  write.csv(FillEddyData.F, file = paste0(RF_path, "/CH-CHA_NEE_RF-GAPF_RP-", run_id, ".csv"), row.names = FALSE)
  cat("Gapfilled done \n")
  assign("RFFillEddyData.F", FillEddyData.F, envir = .GlobalEnv)
  
  

  # New TK Partitioning first
  cat("Start TK partitioning \n")
  EddyProc.C$sTKFluxPartition(suffix = 'U16')
  cat("NEE_U16 TK partitioned \n")

  EddyProc.C$sTKFluxPartition(suffix = 'U84')
  cat("NEE_U84 TK partitioned \n")

  EddyProc.C$sTKFluxPartition(suffix = 'U50')
  cat("NEE_U50 TK partitioned \n")

  # Export partitioned data
  FillTKPartitionEddyData.F <- EddyProc.C$sExportResults()
  FillTKPartitionEddyData.F$TIMESTAMP <- EddyData.F$TIMESTAMP_STRING
  TK_path <- paste0(RF_path, "/TK_Partition")
  dir.create(TK_path, recursive = TRUE)
  write.csv(FillTKPartitionEddyData.F, file = paste0(TK_path, "/CH-CHA_NEE_RF-GAPF_TK-PART_RP-", run_id, ".csv"), row.names = FALSE)

  cat(paste0("Files saved to", TK_path, "\n"))
  assign("RFFillTKPartitionEddyData.F", FillTKPartitionEddyData.F, envir = .GlobalEnv)

  # Plot TK Results
  EddyProc.C$sPlotFingerprint('NEE_U50_orig', Dir = TK_path)
  EddyProc.C$sPlotFingerprint('GPP_DT_U50', Dir = TK_path)
  EddyProc.C$sPlotFingerprint('Reco_DT_U50', Dir = TK_path)
  EddyProc.C$sPlotFingerprint('NEE_U16_orig', Dir = TK_path)
  EddyProc.C$sPlotFingerprint('GPP_DT_U16', Dir = TK_path)
  EddyProc.C$sPlotFingerprint('Reco_DT_U16', Dir = TK_path)
  EddyProc.C$sPlotFingerprint('NEE_U84_orig', Dir = TK_path)
  EddyProc.C$sPlotFingerprint('GPP_DT_U84', Dir = TK_path)
  EddyProc.C$sPlotFingerprint('Reco_DT_U84', Dir = TK_path)
  
  cat("TK Partitioning done \n")
  
  
  # Regular Partitioning
  cat("Start Regular partitioning \n")
  EddyProc.C$sMRFluxPartition(suffix = 'U16')
  EddyProc.C$sGLFluxPartition(suffix = 'U16')
  cat("NEE_U16 partitioned \n")

  EddyProc.C$sMRFluxPartition(suffix = 'U84')
  EddyProc.C$sGLFluxPartition(suffix = 'U84')
  cat("NEE_U84 partitioned \n")

  EddyProc.C$sMRFluxPartition(suffix = 'U50')
  EddyProc.C$sGLFluxPartition(suffix = 'U50')
  cat("NEE_U50 partitioned \n")


  # Export partitioned data
  FillPartitionEddyData.F <- EddyProc.C$sExportResults()
  FillPartitionEddyData.F$TIMESTAMP <- EddyData.F$TIMESTAMP_STRING
  
  Regular_path <- paste0(RF_path, "/Regular_Partition")
  dir.create(Regular_path, recursive = TRUE)
  write.csv(FillPartitionEddyData.F, file = paste0(Regular_path, "/CH-CHA_NEE_RF-GAPF_PART_RP-", run_id, ".csv"), row.names = FALSE)

  cat(paste0("Files saved to", Regular_path, "\n"))
  assign("RFFillPartitionEddyData.F", FillPartitionEddyData.F, envir = .GlobalEnv)

  # Save fingerprint plots
  EddyProc.C$sPlotFingerprint('NEE_U50_orig', Dir = Regular_path)
  EddyProc.C$sPlotFingerprint('NEE_U50_f', Dir = Regular_path)
  EddyProc.C$sPlotFingerprint('Tair_f', Dir = Regular_path)
  EddyProc.C$sPlotFingerprint('Rg_f', Dir = Regular_path)
  EddyProc.C$sPlotFingerprint('VPD_f', Dir = Regular_path)
  EddyProc.C$sPlotFingerprint('GPP_U50_f', Dir = Regular_path)
  EddyProc.C$sPlotFingerprint('GPP_DT_U50', Dir = Regular_path)
  EddyProc.C$sPlotFingerprint('Reco_U50', Dir = Regular_path)
  EddyProc.C$sPlotFingerprint('Reco_DT_U50', Dir = Regular_path)
  EddyProc.C$sPlotFingerprint('LE_orig', Dir = Regular_path)
  EddyProc.C$sPlotFingerprint('LE_f', Dir = Regular_path)
  EddyProc.C$sPlotFingerprint('H_orig', Dir = Regular_path)
  EddyProc.C$sPlotFingerprint('H_f', Dir = Regular_path)
  
  cat("Regular Partitioning done \n")
  
  
  cat("Processing completed. Output saved to:", RF_path, "\n")

  
  sink()
  sink(type='message')
  
}
