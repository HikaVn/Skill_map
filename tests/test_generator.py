import pytest

from skill_manager.generator import generate_skill


def test_generator_create_and_no_overwrite(tmp_path):
    out = generate_skill("new-skill", str(tmp_path))
    assert (out / "SKILL.md").is_file()
    with pytest.raises(FileExistsError):
        generate_skill("new-skill", str(tmp_path))


def test_generator_rejects_unsafe_name(tmp_path):
    with pytest.raises(ValueError):
        generate_skill("../danger", str(tmp_path))
