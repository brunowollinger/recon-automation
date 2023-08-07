# Before starting

These automation scripts uses opendistro as DB, before running docker-compose it's necessary to set vm.max_map_count=262144 once using `sysctl -w vm.max_map_count=262144` or permanently by appending `vm.max_map_count=262144` to /etc/sysctl.conf and rebooting, you can verify this metric using `sysctl vm.max_map_count`.
