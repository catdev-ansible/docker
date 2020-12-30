import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_docker_is_installed(host):
    pkg = host.package("docker-ce")

    assert pkg.is_installed
    assert pkg.version.startswith("5:19.03")


def test_docker_running_and_enabled(host):
    svc = host.service("docker")

    assert svc.is_running
    assert svc.is_enabled


def test_docker_config_values(host):
    info = host.run("docker info | tr -d ' '").stdout

    assert "LiveRestoreEnabled:true" in info
    assert "LoggingDriver:json-file" in info


def test_docker_networks(host):
    networks = host.run("docker network inspect demo")

    assert networks.rc == 0
