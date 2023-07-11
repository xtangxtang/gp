if [[ $(date +%u) -gt 5 ]]; then
    echo 'Sorry, you cannot run this program on the weekend.'
    exit
fi

./run_get_capital.sh
./run_get_trade_daily.sh

cd analysis
python3 analysis_daily.py
python3 analysis_bk.py
python3 analysis_gg.py
cd ../

cd weibo
./get_weibo.sh
cd ../


# ./run_self_list.sh
# git add .
# git commit -m "update"
# git push
