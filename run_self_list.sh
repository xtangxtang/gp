#!/bin/sh -e

if [[ $(date +%u) -gt 5 ]]; then
    echo 'Sorry, you cannot run this program on the weekend.'
    exit
fi

# rm -rf gp_list/*.xls
# rm -rf gp_list/*.xlsx

# python3 get_gplist.py

# mv *.xls gp_list/
# sleep 5
# mv ShowReport.xlsx gp_list/sz.xlsx

 python3 get_selflist_daily.py -m 1 -s 2


