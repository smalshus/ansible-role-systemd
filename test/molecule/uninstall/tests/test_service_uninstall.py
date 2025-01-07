def test_service_removed(host):
    try:
        service = host.service("test-service")
        assert not service.is_running, "test-service should not be running after uninstallation"
        assert not service.is_enabled, "test-service should not be enabled after uninstallation"
    except AssertionError as e:
        # Handle unexpected exit code due to service not found
        assert "not-found" in host.check_output("systemctl is-enabled test-service"), \
            "test-service should not exist after uninstallation"

def test_service_unit_file_removed(host):
    unit_file = host.file("/etc/systemd/system/test-service.service")
    assert not unit_file.exists, "/etc/systemd/system/test-service.service should not exist after uninstallation"
