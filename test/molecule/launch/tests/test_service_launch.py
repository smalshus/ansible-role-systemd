def test_service_running_and_enabled(host):
    service = host.service("test-service")
    assert service.is_enabled, "test-service should be enabled"
    assert service.is_running, "test-service should be running"

def test_service_unit_file(host):
    unit_file = host.file("/etc/systemd/system/test-service.service")
    assert unit_file.exists, "/etc/systemd/system/test-service.service should exist"
    assert unit_file.user == "root", "Owner of the unit file should be root"
    assert unit_file.group == "root", "Group of the unit file should be root"
    assert unit_file.contains("Description=This is a test service unit"), \
        "Unit file should contain the correct description"
    assert unit_file.contains("ExecStart=/usr/bin/sleep infinity"), \
        "Unit file should contain the ExecStart command"
    assert unit_file.contains("WantedBy=multi-user.target"), \
        "Unit file should contain the correct WantedBy target"
