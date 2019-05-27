from kubernetes import client, config
import logging
import argparse


def k8s_client_config():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    return v1, apps_v1


def base_config():
    logging.basicConfig()
    logger = logging.getLogger('pgbouncer-monitoring')
    logger.setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--pod-name', dest='pod_name', help='pod name to get suffix for', type=str, required=True)
    parser.add_argument('--pod-namespace', dest='pod_namespace', help='namespace where pod is deployed', type=str,
                        required=True)
    args = parser.parse_args()
    return logger, args


def get_pod_suffix(pod_name, pod_namespace, logger):
    suffix = None
    pgbouncer_pods = []
    pgbouncer_rs = {}

    v1, apps_v1 = k8s_client_config()
    pods = v1.list_namespaced_pod(namespace=pod_namespace)
    for pod in pods.items:
        if pod.metadata.labels != None and pod.metadata.labels.get("app") == "pgbouncer":
            replica_set_name = pod.metadata.owner_references[0].name
            pgbouncer_rs[replica_set_name] = pgbouncer_rs.get(replica_set_name, 0) + 1
            pgbouncer_pods.append({"name": pod.metadata.name,
                                   "replicaSet": pod.metadata.owner_references[0].name,
                                   "creationTimestamp": pod.metadata.creation_timestamp.strftime(
                                       "%Y%m%d%H%M%S")})
    logger.info("Discovered pods: {}".format(pgbouncer_pods))
    logger.info("Number of replica-sets: {}".format(len(pgbouncer_rs)))

    # If there is multiple replica set for pgbouncer it means
    # we have rolling update and need to filter out old pods
    if len(pgbouncer_rs) > 1:
        logger.info("Check replica-set status to choose newest one")
        replica_set_details = [apps_v1.read_namespaced_replica_set_status(name=replicaSet, namespace=pod_namespace)
                               for replicaSet in pgbouncer_rs]
        sorted_replica_set_details = sorted(replica_set_details,
                                            key=lambda k: k.metadata.creation_timestamp.strftime("%Y%m%d%H%M%S"))

        latest_replica_set = sorted_replica_set_details[-1]
        sorted_pods = sorted([pod for pod in pgbouncer_pods if pod['replicaSet'] == latest_replica_set.metadata.name],
                             key=lambda k: k['name'])
    else:
        sorted_pods = sorted([pod for pod in pgbouncer_pods], key=lambda k: k['name'])

    logger.info("Sorted and filtered pods: {}".format(sorted_pods))

    # If there is more than one pod we have high availability
    # and need to add suffix to monitoring config to distinguish instances
    if len(sorted_pods) > 1:
        logger.info("Count NewRelic service pod monitoring suffix")
        try:
            for index, pod in enumerate(sorted_pods):
                if pod['name'] == pod_name:
                    logger.info("Found pod {}. Suffix is {}".format(pod_name, index + 1))
                    suffix = "-{}".format(index + 1)
            if not suffix:
                raise KeyError(pod_name)
        except KeyError:
            logger.error("Couldn't find pod {}! Exiting...".format(pod_name))
            raise
    else:
        logger.info("There is only one pod. No need for suffix")
    return suffix


if __name__ == '__main__':
    logger, args = base_config()
    suffix = get_pod_suffix(pod_name=args.pod_name, pod_namespace=args.pod_namespace, logger=logger)
    if suffix:
        with open("suffix.txt", mode="w") as suffix_file:
            suffix_file.write(suffix)
            logger.info("Write suffix value {} to file suffix.txt".format(suffix))
    else:
        logger.info("No suffix provided. Skipping writing to file")
