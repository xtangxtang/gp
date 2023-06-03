#!/bin/sh -e

# rm -rf gp_list/*.xls
# rm -rf gp_list/*.xlsx

# python3 get_gplist.py

# mv *.xls gp_list/
# sleep 5
# mv ShowReport.xlsx gp_list/sz.xlsx

while true
do
    python3 get_trade_daily.py -m 1 -s 1
done


