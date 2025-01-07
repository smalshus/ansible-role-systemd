def test_service_removed(host):
    # Attempt to check if the service is enabled
    result = host.run("systemctl is-enabled test-service")

    # Assert exit code 4 (service not found) or a valid non-enabled state
    assert result.rc in [0, 1, 4], (
        f"Unexpected exit code {result.rc} when checking service status. "
        f"stdout: {result.stdout}, stderr: {result.stderr}"
    )

    # Additional assertions based on the specific exit code
    if result.rc == 4:
        assert "not-found" in result.stdout, "Service should not exist after uninstallation"
    elif result.rc in [0, 1]:
        assert not result.stdout.strip() == "enabled", "Service should not be enabled after uninstallation"

def test_service_unit_file_removed(host):
    unit_file = host.file("/etc/systemd/system/test-service.service")
    assert not unit_file.exists, "/etc/systemd/system/test-service.service should not exist after uninstallation"
