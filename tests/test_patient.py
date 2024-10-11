"""Tests for the Patient model."""
import pytest

@pytest.mark.skip
def test_create_patient():
    from inflammation.models import Patient

    name = 'Alice'
    p = Patient(name=name)

    assert p.name == name
