from datetime import datetime
import logging
from kubernetes import client, config
from pint import UnitRegistry
from collections import defaultdict
from pathlib import Path
from kubernetes.client.rest import ApiException
import yaml

JOB_NAME = "calc-job"


class K8sBase:
    """Clasa de Baza"""

    def __init__(self) -> None:
        try:
            # Calea catre fisierul de configurare
            path_to_config_file = (
                Path(__file__).parent.parent.parent / "rke2-terraform/k8s.yaml"
            )
            # Incarcarea fisierului de configurare daca acesta exista
            if path_to_config_file.is_file():
                config.load_kube_config(config_file=path_to_config_file.as_posix())
            else:
                # Se emite o exceptie in cazul in care fisierul nu exista
                print(f"The file {path_to_config_file} does not exist")
                raise FileNotFoundError
        except config.ConfigException:
            raise

        self.api_core = client.CoreV1Api()
        self.api_app = client.AppsV1Api()
        self.api_batch = client.BatchV1Api()
        self.api_customObject = client.CustomObjectsApi()
        self.api_rbac_authorization = client.RbacAuthorizationV1Api()
        self.api_storage = client.StorageV1Api()
        self.api_network = client.NetworkingV1Api()

    def afisare_k8s_nodes(self):
        """Afisarea nodurilor din clusterul Kubernetes."""
        api = self.api_core.list_node()
        result = []
        for i in api.items:
            result.append(i.metadata.name)
        return result

    def afisare_k8s_nodes_resources(self):
        """Afisarea resurselor de care dispun nodurile din clusterul Kubernetes."""
        ureg = UnitRegistry()
        # Incarcarea definitiilor unitatilor de masura
        ureg.load_definitions(f"{Path(__file__).resolve().parent}/units.txt")

        Q_ = ureg.Quantity
        data = {}

        api = self.api_core.list_node()

        for node in api.items:
            stats = {}
            node_name = node.metadata.name
            allocatable = node.status.allocatable
            max_pods = int(int(allocatable["pods"]) * 1.5)
            field_selector = (
                "status.phase!=Succeeded,status.phase!=Failed,"
                + "spec.nodeName="
                + node_name
            )

            stats["cpu_alloc"] = Q_(allocatable["cpu"])
            stats["mem_alloc"] = Q_(allocatable["memory"])

            pods = self.api_core.list_pod_for_all_namespaces(
                limit=max_pods, field_selector=field_selector
            ).items

            cpureqs, cpulmts, memreqs, memlmts = [], [], [], []
            for pod in pods:
                for container in pod.spec.containers:
                    res = container.resources
                    reqs = defaultdict(lambda: 0, res.requests or {})
                    lmts = defaultdict(lambda: 0, res.limits or {})
                    cpureqs.append(Q_(reqs["cpu"]))
                    memreqs.append(Q_(reqs["memory"]))
                    cpulmts.append(Q_(lmts["cpu"]))
                    memlmts.append(Q_(lmts["memory"]))

            stats["cpu_req"] = sum(cpureqs)
            stats["cpu_lmt"] = sum(cpulmts)
            stats["cpu_req_per"] = stats["cpu_req"] / stats["cpu_alloc"] * 100
            stats["cpu_lmt_per"] = stats["cpu_lmt"] / stats["cpu_alloc"] * 100

            stats["mem_req"] = sum(memreqs)
            stats["mem_lmt"] = sum(memlmts)
            stats["mem_req_per"] = stats["mem_req"] / stats["mem_alloc"] * 100
            stats["mem_lmt_per"] = stats["mem_lmt"] / stats["mem_alloc"] * 100

            data[node_name] = stats
        return data

    def citire_k8s_nodes(self, node_name):
        """ Citirea starii nodurilor din clusterul Kubernetes."""
        capacity = self.api_core.read_node_status(node_name)

    def obtinere_k8s_namespaces(self):
        """Obtinere Namespaces din clusterul Kubernetes."""
        api = self.api_core.list_namespace(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
                # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {"name": i.metadata.name, "label": _labels, "phase": i.status.phase}
            )
        return result

    def obtinere_k8s_DeploymentsData(self):
        """Obtinere informatii Deployments din clusterul Kubernetes."""
        api = self.api_app.list_deployment_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace,
                    "image": i.spec.template.spec.containers[0].image,
                    "label": _labels,
                }
            )
        return result

    def obtinere_k8s_StatefulSetsData(self):
        """Obtinere informatii Stateful Sets din clusterul Kubernetes."""
        api = self.api_app.list_stateful_set_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace,
                    "image": i.spec.template.spec.containers[0].image,
                    "label": _labels,
                }
            )
        return result

    def obtinere_k8s_ServicesData(self):
        """Obtinere informatii Services din clusterul Kubernetes."""
        api = self.api_core.list_service_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace,
                    "label": _labels,
                    "type": i.spec.type,
                    "cluster_ip": i.spec.cluster_ip,
                }
            )
        return result

    def obtinere_k8s_PodsData(self):
        """Obtinere informatii Pods din clusterul Kubernetes."""
        api = self.api_core.list_pod_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "image": i.spec.containers[0].image,
                    "label": _labels,
                    "node": i.spec.node_name,
                    "state": i.status.phase,
                }
            )

        return result

    def obtinere_k8s_JobsData(self):
        """Obtinere informatii Jobs din clusterul Kubernetes."""
        api = self.api_batch.list_job_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace,
                    "image": i.spec.template.spec.containers[0].image,
                    "label": _labels,
                }
            )
        return result

    def obtinere_k8s_CronJobsData(self):
        """Obtinere informatii Cron Jobs din clusterul Kubernetes."""
        api = self.api_batch.list_cron_job_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace,
                    "image": i.spec.job_template.spec.template.spec.containers[0].image,
                    "label": _labels,
                }
            )
        return result

    def obtinere_k8s_ReplicaSetsData(self):
        """Obtinere informatii Replica Sets din clusterul Kubernetes."""
        api = self.api_app.list_replica_set_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace,
                    "image": i.spec.template.spec.containers[0].image,
                    "label": _labels,
                }
            )
        return result

    def obtinere_k8s_Cluster_Role_Binding(self):
        """Obtinere informatii Cluster Role Binding din clusterul Kubernetes."""
        api = self.api_rbac_authorization.list_cluster_role_binding(watch=False)
        result = []
        for i in api.items:
            time_since_creation = (
                datetime.now() - i.metadata.creation_timestamp.replace(tzinfo=None)
            )
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {"name": i.metadata.name, "created": f"{time_since_creation.days} days"}
            )
        return result

    def obtinere_k8s_Cluster_Role(self):
        """Obtinere informatii Cluster Role din clusterul Kubernetes."""
        api = self.api_rbac_authorization.list_cluster_role(watch=False)
        result = []
        for i in api.items:
            time_since_creation = (
                datetime.now() - i.metadata.creation_timestamp.replace(tzinfo=None)
            )
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {"name": i.metadata.name, "created": f"{time_since_creation.days} days"}
            )
        return result

    def obtinere_k8s_Config_Maps(self):
        """Obtinere informatii Config Maps din clusterul Kubernetes."""
        api = self.api_core.list_config_map_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace,
                    "label": _labels,
                }
            )
        return result

    def obtinere_k8s_Secrets(self):
        """Obtinere informatii Secrets din clusterul Kubernetes."""
        api = self.api_core.list_secret_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace,
                    "label": _labels,
                    "type": i.type,
                }
            )
        return result

    def obtinere_k8s_Daemon_Sets(self):
        """Obtinere informatii Daemon Sets din clusterul Kubernetes."""
        api = self.api_app.list_daemon_set_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace,
                    "image": i.spec.template.spec.containers[0].image,
                    "label": _labels,
                }
            )
        return result

    def obtinere_k8s_Storage_Classes(self):
        """Obtinere informatii Storage Classes din clusterul Kubernetes."""
        api = self.api_storage.list_storage_class(watch=False)
        result = []
        for i in api.items:
            # Adaugarea intr-o lista a informatiilor necesare
            result.append({"name": i.metadata.name, "provisioner": i.provisioner})
        return result

    def obtinere_k8s_Persistent_Volume_ClaimData(self):
        """Obtinere informatii Persistent Volume Claim din clusterul Kubernetes."""
        api = self.api_core.list_persistent_volume_claim_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
                _storage = ", ".join(f" {v}" for k, v in i.status.capacity.items())
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace,
                    "label": _labels,
                    "status": i.status.phase,
                    "volume": i.spec.volume_name,
                    "capacity": _storage,
                    "accessMode": i.spec.access_modes[0],
                    "storage_class": i.spec.storage_class_name,
                }
            )
        return result

    def obtinere_k8s_Persistent_VolumeData(self):
        """Obtinere informatii Persistent Volume din clusterul Kubernetes."""
        api = self.api_core.list_persistent_volume(watch=False)
        result = []
        for i in api.items:
            _storage = ", ".join(f" {v}" for k, v in i.spec.capacity.items())
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "capacity": _storage,
                    "accessMode": i.spec.access_modes[0],
                    "reclaimPolicy": i.spec.persistent_volume_reclaim_policy,
                    "status": i.status.phase,
                    "claim": i.spec.claim_ref.namespace + "/" + i.spec.claim_ref.name,
                    "storage_class": i.spec.storage_class_name,
                }
            )
        return result

    def obtinere_k8s_EndpointsData(self):
        """Obtinere informatii Endpoints din clusterul Kubernetes."""
        api = self.api_core.list_endpoints_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            _endpoints = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
            if i.subsets:
                _endpoints = (
                    i.subsets[0].addresses[0].ip + ":" + str(i.subsets[0].ports[0].port)
                )
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace,
                    "label": _labels,
                    "endpoint": _endpoints,
                }
            )
        return result

    def obtinere_k8s_IngressesData(self):
        """Obtinere informatii Ingresses din clusterul Kubernetes."""
        api = self.api_network.list_ingress_for_all_namespaces(watch=False)
        result = []
        for i in api.items:
            _labels = "-"
            _hosts = "-"
            if i.metadata.labels:
                _labels = ", ".join(f"{k}: {v}" for k, v in i.metadata.labels.items())
            if i.spec:
                _hosts = i.spec.rules[0].host
            # Adaugarea intr-o lista a informatiilor necesare
            result.append(
                {
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace,
                    "label": _labels,
                    "host": _hosts,
                }
            )
        return result

    def create_job_object(self, a, b):
        """Creare obiectului de tip Job."""
        container = client.V1Container(
            name="python",
            command=["python"],
            image="python:3.9-alpine",
            args=[
                "-c",
                "import sys; a, b = sys.argv[1:3]; summ = int(a) + int(b); print(f'sum is {summ}')",
                a,
                b,
            ],
        )
        # Template
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"name": "calc-job"}),
            spec=client.V1PodSpec(restart_policy="OnFailure", containers=[container]),
        )
        # Specificatii
        spec = client.V1JobSpec(template=template)

        # Instantiere obiect Job
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=JOB_NAME),
            spec=spec,
        )

        return job

    def create_job(self, job):
        """Creare Job pentru suma a doua numere."""
        api_response = self.api_batch.create_namespaced_job(
            body=job, namespace="default"
        )
        print("Job creat. Status='%s'" % str(api_response.status))

    def stergere_pods_inactive(self, namespace="default", phase="Succeeded"):
        """Stergerea Pod-urilor inactive."""
        try:
            pods = self.api_core.list_namespaced_pod(
                namespace, pretty=True, timeout_seconds=60
            )
        except ApiException as e:
            logging.error("Exceptie la apelul CoreV1Api->list_namespaced_pod: %s\n" % e)

        for pod in pods.items:
            logging.debug(pod)
            podname = pod.metadata.name
            try:
                if pod.status.phase == phase:
                    api_response = self.api_core.delete_namespaced_pod(
                        podname, namespace
                    )
                    logging.info("Pod: {} sters!".format(podname))
                    logging.debug(api_response)
                else:
                    logging.info(
                        "Pod: {} ..... Phase: {}".format(podname, pod.status.phase)
                    )
            except ApiException as e:
                logging.error(
                    "Exceptie la apelul CoreV1Api->delete_namespaced_pod: %s\n" % e
                )

        return

    def cleanup_finished_jobs(self, namespace="default", state="Finished"):
        """Stergerea Job-urilor care si-au terminat executia."""
        try:
            jobs = self.api_batch.list_namespaced_job(
                namespace, pretty=True, timeout_seconds=60
            )
        except ApiException as e:
            print("Exceptie la apelul BatchV1Api->list_namespaced_job: %s\n" % e)

        for job in jobs.items:
            logging.debug(job)
            jobname = job.metadata.name
            jobstatus = job.status.conditions
            if job.status.succeeded == 1:
                logging.info(
                    "Clean up la Job-ul: {}. S-a terminat la: {}".format(
                        jobname, job.status.completion_time
                    )
                )
                try:
                    api_response = self.api_batch.delete_namespaced_job(
                        jobname,
                        namespace,
                    )
                    logging.debug(api_response)
                except ApiException as e:
                    print(
                        "Exceptie la apelul BatchV1Api->delete_namespaced_job: %s\n" % e
                    )
            else:
                if jobstatus is None and job.status.active == 1:
                    jobstatus = "active"
                logging.info(
                    "Job: {} nu a fost sters. Status curent: {}".format(
                        jobname, jobstatus
                    )
                )

        self.stergere_pods_inactive(namespace)
        return

    def mongoDB_deployment(self):
        """Incarcare fisier yaml pt crearea deployment-ului pentru mongoDB."""
        with open(
            Path(__file__).parent.parent.parent
            / "rke2-terraform/mongodb-deployment.yml"
        ) as f:
            dep = yaml.safe_load(f)
            api = self.api_app.create_namespaced_deployment(
                body=dep, namespace="default"
            )
            print("Deployment creat. Status='%s'" % api.metadata.name)

    def mongoDB_service(self):
        """Incarcare fisier yaml pt crearea service-ului pentru mongoDB."""
        with open(
            Path(__file__).parent.parent.parent / "rke2-terraform/mongodb-service.yml"
        ) as f:
            dep = yaml.safe_load(f)
            api = self.api_core.create_namespaced_service(body=dep, namespace="default")
            print("Service creat. Status='%s'" % api.metadata.name)

    def mongoDB_configmap(self):
        """Incarcare fisier yaml pt crearea configmap-ului pentru mongoDB."""
        with open(
            Path(__file__).parent.parent.parent / "rke2-terraform/mongodb-configmap.yml"
        ) as f:
            dep = yaml.safe_load(f)
            api = self.api_core.create_namespaced_config_map(
                body=dep, namespace="default"
            )
            print("Config Map creat. Status='%s'" % api.metadata.name)

    def mongoDB_secret(self):
        """Incarcare fisier yaml pt crearea secretului pentru mongoDB."""
        with open(
            Path(__file__).parent.parent.parent / "rke2-terraform/mongodb-secret.yml"
        ) as f:
            dep = yaml.safe_load(f)
            api = self.api_core.create_namespaced_secret(body=dep, namespace="default")
            print("Secret creat. Status='%s'" % api.metadata.name)

    def deploy_mongodb(self):
        """Incarcarea fisierelor de creare a aplicatiei mongoDB."""
        self.mongoDB_configmap()
        self.mongoDB_secret()
        self.mongoDB_deployment()
        self.mongoDB_service()
