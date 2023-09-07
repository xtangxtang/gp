#!/bin/bash -e

if [[ $(date +%u) -gt 5 ]]; then
    echo 'Sorry, you cannot run this program on the weekend.'
    exit
fi

# export TODAY="2023-08-24"

./run_get_capital.sh
./run_get_trade_daily.sh

cd analysis
python3 analysis_daily.py
python3 analysis_bk.py
python3 analysis_gg_captial.py
python3 analysis_ths_bk.py
python3 daily_report.py
cd ../

# cd weibo
# ./get_weibo.sh
# cd ../


# ./run_self_list.sh
# git add .
# git commit -m "update"
# git push
