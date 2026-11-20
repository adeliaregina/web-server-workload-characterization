@echo off
echo Replay SASK: 6 jalan, sekitar 10 menit per jalan. Jangan tutup jendela server uji.
echo [1/6] skenario a, seed 1
py replay.py hasil_SASK\scenario_a.json --ref hasil_SASK\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 1 --out hasil_SASK\replay_a_s1 > hasil_SASK\log_replay_a_s1.txt 2>&1
echo [2/6] skenario b, seed 1
py replay.py hasil_SASK\scenario_b.json --ref hasil_SASK\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 1 --out hasil_SASK\replay_b_s1 > hasil_SASK\log_replay_b_s1.txt 2>&1
echo [3/6] skenario a, seed 2
py replay.py hasil_SASK\scenario_a.json --ref hasil_SASK\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 2 --out hasil_SASK\replay_a_s2 > hasil_SASK\log_replay_a_s2.txt 2>&1
echo [4/6] skenario b, seed 2
py replay.py hasil_SASK\scenario_b.json --ref hasil_SASK\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 2 --out hasil_SASK\replay_b_s2 > hasil_SASK\log_replay_b_s2.txt 2>&1
echo [5/6] skenario a, seed 3
py replay.py hasil_SASK\scenario_a.json --ref hasil_SASK\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 3 --out hasil_SASK\replay_a_s3 > hasil_SASK\log_replay_a_s3.txt 2>&1
echo [6/6] skenario b, seed 3
py replay.py hasil_SASK\scenario_b.json --ref hasil_SASK\scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 3 --out hasil_SASK\replay_b_s3 > hasil_SASK\log_replay_b_s3.txt 2>&1
echo SELESAI. Semua hasil ada di folder hasil_SASK.
pause
