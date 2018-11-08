
# cluster_id = 5
#
# sql = "UPDATE `RUNNING_SERVICES` SET `running_svc_status`='{rning_svc_stat}' WHERE `cluster_id`='{iclus}' AND `service_id`='{isvc}';"
#
# print sql.format(rning_svc_stat='hello', iclus=cluster_id, isvc='667')

import re

word = 'ud[7]'

print re.compile("=?\[(.*)\]").search(word).group(1)
