import pytest

@pytest.mark.parametrize(
    "file_path,owner,group,mode,content_matches",
    [
        (
            "/usr/local/lib/systemd/system/default-test-service.service",
            "root",
            "root",
            0o644,
            ["Description=", "ExecStart=", "WantedBy="],
        ),
        (
            "/etc/systemd/system/test-service.socket",
            "root",
            "root",
            0o644,
            ["Description=", "ListenStream=", "WantedBy="],
        ),
        (
            "/run/systemd/system/tmp-stdin.mount",
            "root",
            "root",
            0o644,
            ["Description=", "What=", "WantedBy="],
        ),
        (
            "/etc/systemd/system/test-target.target",
            "root",
            "root",
            0o644,
            ["Description=", "Wants=", "PartOf="],
        ),
        (
            "/lib/systemd/system/getty@.service.d/test-drop-in.conf",
            "root",
            "root",
            0o644,
            ["ExecStart=", "ExecStart=-/sbin/agetty -a muru --noclear %I $TERM"],
        ),
        (
            "/home/sduser/.config/systemd/user/user-test-service.service",
            "sduser",
            "sduser",
            0o644,
            ["Description=", "ExecStart=", "WantedBy=default.target"],
        ),
    ],
)
def test_unit_files(host, file_path, owner, group, mode, content_matches):
    unit_file = host.file(file_path)
    assert unit_file.exists, f"{file_path} should exist"
    assert unit_file.user == owner, f"{file_path} owner should be {owner}"
    assert unit_file.group == group, f"{file_path} group should be {group}"
    assert oct(unit_file.mode) == oct(mode), f"{file_path} mode should be {oct(mode)}"
    for content in content_matches:
        assert content in unit_file.content_string, f"{content} not found in {file_path}"

@pytest.mark.parametrize("service_name", ["default-test-service"])
def test_default_service_not_enabled(host, service_name):
    service = host.service(service_name)
    assert not service.is_enabled, f"Service {service_name} should not be enabled"

@pytest.mark.parametrize("service_name", ["test-service"])
def test_service_enabled(host, service_name):
    service = host.service(service_name)
    assert service.is_enabled, f"Service {service_name} should be enabled"


def test_user_unit_loaded_in_user_scope(host):
    show = host.run(
        "runuser -u sduser -- env XDG_RUNTIME_DIR=/run/user/$(id -u sduser) "
        "systemctl --user show user-test-service.service -p LoadState --value"
    )
    assert show.rc == 0, show.stderr
    assert show.stdout.strip() == "loaded", show.stdout


def test_user_unit_path_owned_by_user(host):
    for path in (
        "/home/sduser/.config",
        "/home/sduser/.config/systemd",
        "/home/sduser/.config/systemd/user",
    ):
        directory = host.file(path)
        assert directory.is_directory, f"{path} should be a directory"
        assert directory.user == "sduser", f"{path} owner should be sduser"
        assert directory.group == "sduser", f"{path} group should be sduser"
