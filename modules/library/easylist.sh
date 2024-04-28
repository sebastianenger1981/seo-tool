# Download AdBlock Lists (EasyList, EasyPrivacy, Fanboy Annoyance / Social Blocking)
curl -s -L https://easylist-downloads.adblockplus.org/easylistgermany%2Beasylist.txt https://raw.githubusercontent.com/zpacman/Blockzilla/master/Blockzilla.txt https://easylist-downloads.adblockplus.org/antiadblockfilters.txt https://easylist-downloads.adblockplus.org/adwarefilters.txt https://easylist-downloads.adblockplus.org/fanboy-annoyance.txt https://easylist-downloads.adblockplus.org/malwaredomains_full.txt http://www.kiboke-studio.hr/i-dont-care-about-cookies/abp/ https://raw.githubusercontent.com/Dawsey21/Lists/master/adblock-list.txt https://easylist-downloads.adblockplus.org/easylistgermany%2Beasylist.txt https://easylist.to/easylist/easylist.txt https://easylist.to/easylist/easyprivacy.txt https://easylist.to/easylist/fanboy-annoyance.txt https://easylist.to/easylist/fanboy-social.txt > adblock.unsorted

# Look for: ||domain.tld^
sort -u adblock.unsorted | grep ^\|\|.*\^$ | grep -v \/ > adblock.sorted

# Remove extra chars and put list under lighttpd web root
sed 's/[\|^]//g' < adblock.sorted > /var/www/html/adblock.hosts

# Remove files we no longer need
rm adblock.unsorted adblock.sorted

pihole -g

exit