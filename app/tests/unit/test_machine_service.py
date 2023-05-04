import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Machine, Site
from app.database.schemas import MachineCreate, MachineType
from app.services.shared.errors import SiteEnergyError
from app.services.machine_service import create_machine


@pytest.fixture
def db_mock_setup():
    db_mock = AsyncMock(spec=AsyncSession)

    result_proxy_mock = MagicMock()
    db_mock.execute.return_value = result_proxy_mock

    return db_mock, result_proxy_mock


@pytest.mark.asyncio
@patch('app.services.machine_service.get_site_accumulated_energy')
async def test_create_machine_with_valid_data(get_site_accumulated_energy_mock, db_mock_setup):
    db_mock, result_proxy_mock = db_mock_setup
    machine_data = MachineCreate(
        name="Test Machine", nominal_power=100, site_id=1, type=MachineType.FURNACE)

    site_mock = Site(id=1, max_power=500)
    result_proxy_mock.scalars.return_value.one_or_none.return_value = site_mock

    get_site_accumulated_energy_mock.return_value = 200

    result = await create_machine(db_mock, machine_data)

    assert isinstance(result, Machine)
    assert result.name == "Test Machine"
    assert result.nominal_power == 100
    assert result.site_id == 1

    get_site_accumulated_energy_mock.assert_called_once_with(db_mock, 1)
    db_mock.add.assert_called_once_with(result)
    db_mock.commit.assert_awaited_once()
    db_mock.refresh.assert_awaited_once_with(result)


@pytest.mark.asyncio
@patch('app.services.machine_service.get_site_accumulated_energy')
async def test_create_machine_with_exceeded_site_energy_limit(get_site_accumulated_energy_mock, db_mock_setup):
    db_mock, result_proxy_mock = db_mock_setup
    machine_data = MachineCreate(
        name="Test Machine", nominal_power=100, site_id=1, type=MachineType.FURNACE)

    site_mock = Site(id=1, max_power=400)
    result_proxy_mock.scalars.return_value.one_or_none.return_value = site_mock

    get_site_accumulated_energy_mock.return_value = 400

    with pytest.raises(SiteEnergyError):
        await create_machine(db_mock, machine_data)

    get_site_accumulated_energy_mock.assert_called_once_with(db_mock, 1)
    db_mock.add.assert_not_called()
    db_mock.commit.assert_not_awaited()
    db_mock.refresh.assert_not_awaited()
