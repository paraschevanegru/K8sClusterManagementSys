import subprocess
from blacksheep import FromJSON, json
from blacksheep.server.application import Application
from blacksheep.server.controllers import Controller, get, post
from blacksheep.messages import Response
from dataclasses import dataclass
from pathlib import Path

from app.controllers.k8s import K8sBase


@dataclass
class InfrastructureCommands:
    etapa: str

# Clasa Home ofera functii pentru diferitele view-uri din program
class Home(Controller):
    def __init__(self) -> None:
        super().__init__()
        self.k8sBase = None

    @get()
    def index(self):
        """
        Returneaza view-ul cu pagina principala, dupa ce infrastructura a fost creata cu succes.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            return self.view()

    @get("/letscreate")
    def letscreate(self):
        """
        Returneaza view-ul cu pagina in care se creeaza infrastructura.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.view("letscreate")
        else:
            return self.see_other("/")

    @get("/apps")
    def apps(self):
        """
        Returneaza view-ul cu in care se creeaza aplicatiile.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.view("letscreate")
        else:
            return self.view("apps")

    @get("/createjob")
    def createjob(self, a: str, b: str):
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            job = self.k8sBase.create_job_object(a, b)
            self.k8sBase.create_job(job)

    @get("/cleanup")
    def cleanup(self):
        """"""
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            self.k8sBase.cleanup_finished_jobs()
            self.k8sBase.stergere_pods_inactive()

    @get("/cluster")
    def cluster(self):
        """
        Returneaza view-ul cu informatiile legate de cluster daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            cluster_role_bindings = self.k8sBase.obtinere_k8s_Cluster_Role_Binding()
            cluster_role = self.k8sBase.obtinere_k8s_Cluster_Role()
            cluster_namespaces = self.k8sBase.obtinere_k8s_namespaces()

            return self.view(
                "cluster",
                {
                    "listed_cluster_role_bindings": cluster_role_bindings,
                    "listed_cluster_role": cluster_role,
                    "listed_namespaces": cluster_namespaces,
                },
            )

    @get("/nodes")
    def nodes(self):
        """
        Returneaza view-ul cu informatiile legate de noduri daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            noduri_disponibile = self.k8sBase.afisare_k8s_nodes()
            node_resources = self.k8sBase.afisare_k8s_nodes_resources()

            return self.view(
                "nodes",
                {
                    "listed_nodes": noduri_disponibile,
                    "listed_node_resources": node_resources,
                },
            )

    @get("/overview")
    def overview(self):
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            pods_disponibile = self.k8sBase.obtinere_k8s_PodsData()
            deployments_disponibile = self.k8sBase.obtinere_k8s_DeploymentsData()
            daemonsets_disponibile = self.k8sBase.obtinere_k8s_Daemon_Sets()
            statefulsets_disponibile = self.k8sBase.obtinere_k8s_StatefulSetsData()
            replicasets_disponibile = self.k8sBase.obtinere_k8s_ReplicaSetsData()
            jobs_disponibile = self.k8sBase.obtinere_k8s_JobsData()
            cronjobs_disponibile = self.k8sBase.obtinere_k8s_CronJobsData()
            configmaps_disponibile = self.k8sBase.obtinere_k8s_Config_Maps()
            secrets_disponibile = self.k8sBase.obtinere_k8s_Secrets()
            services_disponibile = self.k8sBase.obtinere_k8s_ServicesData()
            endpoints_disponibile = self.k8sBase.obtinere_k8s_EndpointsData()
            ingresses_disponibile = self.k8sBase.obtinere_k8s_IngressesData()
            volumeclaims_disponibile = self.k8sBase.obtinere_k8s_Persistent_Volume_ClaimData()
            volumes_disponibile = self.k8sBase.obtinere_k8s_Persistent_VolumeData()
            storageclasses_disponibile = self.k8sBase.obtinere_k8s_Storage_Classes()

            noOfPods = len(pods_disponibile)
            noOfDeployments = len(deployments_disponibile)
            noOfDaemonSets = len(daemonsets_disponibile)
            noOfStatefulSets = len(statefulsets_disponibile)
            noOfReplicaSets = len(replicasets_disponibile)
            noOfJobs = len(jobs_disponibile)
            noOfCronJobs = len(cronjobs_disponibile)
            noOfConfigMaps = len(configmaps_disponibile)
            noOfSecrets = len(secrets_disponibile)
            noOfServices = len(services_disponibile)
            noOfEndpoints = len(endpoints_disponibile)
            noOfIngresses = len(ingresses_disponibile)
            noOfVolumeClaims = len(volumeclaims_disponibile)
            noOfVolumes = len(volumes_disponibile)
            noOfStorageClasses = len(storageclasses_disponibile)

            return self.view(
                "overview",
                {
                    "numarPods": noOfPods,
                    "numarDeployments": noOfDeployments,
                    "numarDaemonSets": noOfDaemonSets,
                    "numarStatefulSets": noOfStatefulSets,
                    "numarReplicaSets": noOfReplicaSets,
                    "numarJobs": noOfJobs,
                    "numarCronJobs": noOfCronJobs,
                    "numarConfigMaps": noOfConfigMaps,
                    "numarSecrets": noOfSecrets,
                    "numarServices": noOfServices,
                    "numarEndpoints": noOfEndpoints,
                    "numarIngresses": noOfIngresses,
                    "numarVolumeClaims": noOfVolumeClaims,
                    "numarVolumes": noOfVolumes,
                    "numarStorageClasses": noOfStorageClasses
                },
            )

    @get("/mongodb")
    def mongodb(self):
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            self.k8sBase.deploy_mongodb()

    @get("/manageinfrastructure")
    def manageinfrastructure(self):
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            return self.view()

    @get("/pods")
    def pods(self):
        """
        Returneaza view-ul cu informatiile legate de pod-uri daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            pods_disponibile = self.k8sBase.obtinere_k8s_PodsData()

            return self.view("pods", {"listed_pods": pods_disponibile})

    @get("/deployments")
    def deployments(self):
        """
        Returneaza view-ul cu informatiile legate de deployment-uri daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            deployments_disponibile = self.k8sBase.obtinere_k8s_DeploymentsData()
            return self.view(
                "deployments", {"listed_deployments": deployments_disponibile}
            )

    @get("/replicasets")
    def replicasets(self):
        """
        Returneaza view-ul cu informatiile legate de replica sets daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            replicasets_disponibile = self.k8sBase.obtinere_k8s_ReplicaSetsData()
            return self.view(
                "replicasets", {"listed_replicasets": replicasets_disponibile}
            )

    @get("/daemonsets")
    def daemonsets(self):
        """
        Returneaza view-ul cu informatiile legate de daemon sets daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            daemonsets_disponibile = self.k8sBase.obtinere_k8s_Daemon_Sets()
            return self.view("daemonsets", {"listed_daemonsets": daemonsets_disponibile})

    @get("/statefulsets")
    def statefulsets(self):
        """
        Returneaza view-ul cu informatiile legate de stateful sets daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            statefulsets_disponibile = self.k8sBase.obtinere_k8s_StatefulSetsData()
            return self.view(
                "statefulsets", {"listed_statefulsets": statefulsets_disponibile}
            )

    @get("/jobs")
    def jobs(self):
        """
        Returneaza view-ul cu informatiile legate de job-uri daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            jobs_disponibile = self.k8sBase.obtinere_k8s_JobsData()
            return self.view("jobs", {"listed_jobs": jobs_disponibile})

    @get("/cronjobs")
    def cronjobs(self):
        """
        Returneaza view-ul cu informatiile legate de cron job-uri daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            cronjobs_disponibile = self.k8sBase.obtinere_k8s_CronJobsData()
            return self.view("cronjobs", {"listed_cronjobs": cronjobs_disponibile})

    @get("/services")
    def services(self):
        """
        Returneaza view-ul cu informatiile legate de servicii daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            services_disponibile = self.k8sBase.obtinere_k8s_ServicesData()
            return self.view("services", {"listed_services": services_disponibile})

    @get("/configmaps")
    def configmaps(self):
        """
        Returneaza view-ul cu informatiile legate de config maps daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            configmaps_disponibile = self.k8sBase.obtinere_k8s_Config_Maps()
            return self.view("configmaps", {"listed_configmaps": configmaps_disponibile})

    @get("/secrets")
    def secrets(self):
        """
        Returneaza view-ul cu informatiile legate de secrete daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            secrets_disponibile = self.k8sBase.obtinere_k8s_Secrets()
            return self.view("secrets", {"listed_secrets": secrets_disponibile})

    @get("/namespaces")
    def namespaces(self):
        """
        Returneaza view-ul cu informatiile legate de namespace daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            available_namespaces = self.k8sBase.obtinere_k8s_namespaces()
            return self.view("namespaces", {"listed_namespaces": available_namespaces})

    @get("/storageclasses")
    def storageclasses(self):
        """
        Returneaza view-ul cu informatiile legate de storage classes daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            storageclasses_disponibile = self.k8sBase.obtinere_k8s_Storage_Classes()
            return self.view(
                "storageclasses", {"listed_storageclasses": storageclasses_disponibile}
            )

    @get("/volumeclaims")
    def volumeclaims(self):
        """
        Returneaza view-ul cu informatiile legate de volume claims daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            volumeclaims_disponibile = self.k8sBase.obtinere_k8s_Persistent_Volume_ClaimData()
            return self.view(
                "volumeclaims", {"listed_volumeclaims": volumeclaims_disponibile}
            )

    @get("/volumes")
    def volumes(self):
        """
        Returneaza view-ul cu informatiile legate de volumes daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            volumes_disponibile = self.k8sBase.obtinere_k8s_Persistent_VolumeData()
            return self.view("volumes", {"listed_volumes": volumes_disponibile})

    @get("/endpoints")
    def endpoints(self):
        """
        Returneaza view-ul cu informatiile legate de endpoints daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            endpoints_disponibile = self.k8sBase.obtinere_k8s_EndpointsData()
            return self.view("endpoints", {"listed_endpoints": endpoints_disponibile})

    @get("/ingresses")
    def ingresses(self):
        """
        Returneaza view-ul cu informatiile legate de ingresses daca infrastructura este creata.
        """
        try:
            self.k8sBase = K8sBase()
        except:
            return self.see_other("/letscreate")
        else:
            ingresses_disponibile = self.k8sBase.obtinere_k8s_IngressesData()
            return self.view("ingresses", {"listed_ingresses": ingresses_disponibile})

    @post("/infrastructure")
    async def infrastructure(self, input: FromJSON[InfrastructureCommands]):
        """Gestionarea infrastructurii in functie de etapa care se executa:
        crearea planului de executie, crearea infrastructurii si distrugerea infrastructurii."""
        data = input.value
        if data.etapa == "plan":
            check_terraform_process = subprocess.Popen(
                "cd rke2-terraform && make check-terraform && make tf-init && make tf-plan",
                stderr=subprocess.STDOUT,
                shell=True,
            )
        elif data.etapa == "apply":
            tf_apply_process = subprocess.Popen(
                "cd rke2-terraform && make add-keypair && make tf-apply && make create-k8s-file",
                stderr=subprocess.STDOUT,
                shell=True,
            )
        elif data.etapa == "destroy":
            tf_destroy_process = subprocess.Popen(
                "cd rke2-terraform && make tf-destroy",
                stderr=subprocess.STDOUT,
                shell=True,
            )
            path_to_config_file = (
                Path(__file__).parent.parent.parent / "rke2-terraform/k8s.yaml"
            )
            path_to_config_file.unlink()
