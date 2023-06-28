if [[ $(date +%u) -gt 5 ]]; then
    echo 'Sorry, you cannot run this program on the weekend.'
    exit
fi

./run_get_capital.sh
./run_get_trade_daily.sh
./run_self_list.sh

# git add .
# git commit -m "update"
# git push
