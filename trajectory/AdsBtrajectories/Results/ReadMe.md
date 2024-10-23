 ## launch a cmd window

move to the folder containing the tile to upload
cd "C:\Users\rober\git\flight-profile\trajectory\AdsBtrajectories\Results"
 
 
 ## define an alias
 
   mc.exe alias set dc24 https://s3.opensky-network.org/ ZG58zJvKhts2bkOX eU95azmBpK82kg96mE0TNzsWov3OvP2d
 Added `dc24` successfully.
 
 ## read the content of the 
 
 
PS C:\Users\rober\git\flight-profile\trajectory\AdsBtrajectories\Results> mc.exe ls dc24/competition-data/
[2024-10-09 01:48:12 CEST] 539MiB STANDARD 2022-01-01.parquet
[2024-10-09 01:51:22 CEST] 734MiB STANDARD 2022-01


 ## upload a file
 
 mc.exe cp ./team_exuberant_hippo_v1_f8afb85a-8f3f-4270-b0bd-10f9ba83adf4.csv dc24/submissions/team_exuberant_hippo_v1_f8afb85a-8f3f-4270-b0bd-10f9ba83adf4.csv

warning : version must be in lower case

team_exuberant_hippo_v6_f8afb85a-8f3f-4270-b0bd-10f9ba83adf4.csv
 
 PS C:\Users\rober\git\flight-profile\trajectory\AdsBtrajectories\Results>
 
 
 ## own results for each version
 v6 -> 3,634.46
    -> with extreme boost -> The root mean squared error (MSE) on test set: 3365.5117
    -> with extreme boost and n_estimators=5000 -> The root mean squared error (MSE) on test set: 3152.6824
    -> modelXgb = XGBRegressor(n_estimators=15000,max_depth=13,eta=0.1,subsample=0.9)     --> The root mean squared error (MSE) on test set: 3032.6191
    -> added average climb and descent rate -> The root mean squared error (MSE) on test set: 2968.7519
 v7 on the rankings page -> 3,036.23
    -> encode the adep and ades -> The root mean squared error (MSE) on test set: 2952.5519
    -> encode ades and adep country -> The root mean squared error (MSE) on test set: 2898.6048
    
 