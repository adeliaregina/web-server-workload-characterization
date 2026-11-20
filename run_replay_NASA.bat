@echo off
echo 7 jalan replay, sekitar 75 menit. Jangan memakai komputer selama ini. Jangan tutup jendela server uji.
echo [1/7] SASK ulang skenario a seed 1 (jadwal permintaan identik)
py replay.py hasil_SASK\scenario_a.json --ref hasil_SASK\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 1 --out hasil_SASK\replay_a_s1_ulang > hasil_SASK\log_replay_a_s1_ulang.txt 2>&1
echo [2/7] NASA skenario a seed 1
py replay.py hasil_NASA\scenario_a.json --ref hasil_NASA\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 1 --out hasil_NASA\replay_a_s1 > hasil_NASA\log_replay_a_s1.txt 2>&1
echo [3/7] NASA skenario b seed 1
py replay.py hasil_NASA\scenario_b.json --ref hasil_NASA\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 1 --out hasil_NASA\replay_b_s1 > hasil_NASA\log_replay_b_s1.txt 2>&1
echo [4/7] NASA skenario a seed 2
py replay.py hasil_NASA\scenario_a.json --ref hasil_NASA\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 2 --out hasil_NASA\replay_a_s2 > hasil_NASA\log_replay_a_s2.txt 2>&1
echo [5/7] NASA skenario b seed 2
py replay.py hasil_NASA\scenario_b.json --ref hasil_NASA\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 2 --out hasil_NASA\replay_b_s2 > hasil_NASA\log_replay_b_s2.txt 2>&1
echo [6/7] NASA skenario a seed 3
py replay.py hasil_NASA\scenario_a.json --ref hasil_NASA\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 3 --out hasil_NASA\replay_a_s3 > hasil_NASA\log_replay_a_s3.txt 2>&1
echo [7/7] NASA skenario b seed 3
py replay.py hasil_NASA\scenario_b.json --ref hasil_NASA\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 3 --out hasil_NASA\replay_b_s3 > hasil_NASA\log_replay_b_s3.txt 2>&1
echo SELESAI.
pause
