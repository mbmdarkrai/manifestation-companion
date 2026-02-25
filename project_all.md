/Users/mbm/R/PROJECT_ALL/
  scripts/
    01_SETX_LCM_MultiRNAflow_MFUZZ_Supervised.R
    02_AR100AR20_LCM_DESeq2_MFuzz.R
    03_iPSC_MultiRNAflow_MFUZZ_Supervised.R
    04_COMPARE_Setx_vs_AR100_vs_iPSC.R
  data/
    (all your count + sample files)
  results/
    _RUNS/
      RUN_20260224_1530/
        SETX/
        LCM_AR100_AR20/
        iPSC/
        COMPARE/


        cd /Users/mbm/Documents/Manifestation
git status
git add .
git commit -m "Upgrade Claude option" --allow-empty
git push origin main


1. Cmd+Shift+G
2. No changes? → git push anyway:
Terminal: git push origin main


#force
git commit --allow-empty -m "Update"
git push origin main --force
