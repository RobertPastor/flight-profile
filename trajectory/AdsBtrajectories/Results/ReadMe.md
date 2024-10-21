 ## launch a cmd window
 
 
 ## define an alias
 
   mc.exe alias set dc24 https://s3.opensky-network.org/ ZG58zJvKhts2bkOX eU95azmBpK82kg96mE0TNzsWov3OvP2d
 Added `dc24` successfully.
 
 ## read the content of the 
 
 
PS C:\Users\rober\git\flight-profile\trajectory\AdsBtrajectories\Results> mc.exe ls dc24/competition-data/
[2024-10-09 01:48:12 CEST] 539MiB STANDARD 2022-01-01.parquet
[2024-10-09 01:51:22 CEST] 734MiB STANDARD 2022-01


 ## upload a file
 
 mc.exe cp ./team_exuberant_hippo_V1_f8afb85a-8f3f-4270-b0bd-10f9ba83adf4.csv dc24/submissions/team_exuberant_hippo_V1_f8afb85a-8f3f-4270-b0bd-10f9ba83adf4.csv
 
 PS C:\Users\rober\git\flight-profile\trajectory\AdsBtrajectories\Results>
 -02.parquet
 
 ##
 results v3
 
  {
        "name": "team_exuberant_hippo",
        "files": [
            {
                "rmse": 4454.58,
                "processed": true,
                "file_version": "v4",
                "num_lines": 158149,
                "submission_date": "2024-10-21T15:15:53.54Z"
            },
            {
                "rmse": 4466.52,
                "processed": true,
                "file_version": "v3",
                "num_lines": 158149,
                "submission_date": "2024-10-21T12:15:46.185Z"
            }
        ]
    },