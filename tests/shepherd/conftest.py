import pytest
import json
import os.path as path
from io import BytesIO
import os.path as path

from cxworker.constants import DEFAULT_PAYLOAD_PATH, INPUT_DIR
from cxworker.shepherd.config import load_worker_config
from cxworker.shepherd import Shepherd
from cxworker.api.models import ModelModel


@pytest.fixture()
def valid_config_file():
    yield path.join('examples', 'configs', 'cxworker-bare.yml')


@pytest.fixture()
def valid_config_env_file():
    yield path.join('examples', 'configs', 'cxworker-bare-env.yml')


@pytest.fixture()
def invalid_config_env_file():
    yield path.join('examples', 'configs', 'cxworker-bare-env-invalid.yml')


@pytest.fixture()
def invalid_config_file(tmpdir):
    """Invalid worker configuration with missing mandatory sections."""
    invalid_config_filepath = path.join(str(tmpdir), 'config.yml')
    with open(invalid_config_filepath, 'w') as file:
        file.write('logging:\n  level: debug')
    yield invalid_config_filepath


@pytest.fixture()
def valid_config(valid_config_file):
    with open(valid_config_file) as file:
        yield load_worker_config(file)


@pytest.fixture()
def shepherd(valid_config, minio):
    """Shepherd with a single bare sheep which runs a cxflow runner that doubles its inputs."""
    shepherd = Shepherd(valid_config.sheep, valid_config.data_root, minio, valid_config.registry)
    yield shepherd
    shepherd.close()


@pytest.fixture()
def job(bucket, minio):
    job_id = bucket
    data = json.dumps({'key': [1000]}).encode()
    minio.put_object(bucket, DEFAULT_PAYLOAD_PATH, BytesIO(data), len(data))
    yield job_id, ModelModel(dict(name='cxflow-test', version='test2'))


@pytest.fixture()
def bad_job(bucket, minio):
    """Job with wrong input name should cause recoverable runner runtime error."""
    job_id = bucket
    data = json.dumps({'key': [1000]}).encode()
    minio.put_object(bucket, INPUT_DIR + '/some_other_file.json', BytesIO(data), len(data))
    yield job_id, ModelModel(dict(name='cxflow-test', version='latest'))


@pytest.fixture()
def bad_configuration_job(bucket, minio):
    """Job with wrong model name should cause sheep configuration error."""
    job_id = bucket
    data = json.dumps({'key': [1000]}).encode()
    minio.put_object(bucket, DEFAULT_PAYLOAD_PATH, BytesIO(data), len(data))
    yield job_id, ModelModel(dict(name='wrong-model', version='latest'))


@pytest.fixture()
def bad_runner_job(bucket, minio):
    """cxflow-test:test model has bad runner configuration; thus, the runner should fail (and stop)."""
    job_id = bucket
    data = json.dumps({'key': [1000]}).encode()
    minio.put_object(bucket, DEFAULT_PAYLOAD_PATH, BytesIO(data), len(data))
    yield job_id, ModelModel(dict(name='cxflow-test', version='test'))
