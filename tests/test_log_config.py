from unittest.mock import Mock

from fyndiq_helpers.log_config import HealthFilter


class TestHealthFilter():
    health_filter_class = HealthFilter()

    def test_filter_should_find_health_requests(self):
        record = Mock()
        record.request = "GET http://10.32.3.15:7000/health"

        result = self.health_filter_class.filter(record)
        assert result is False

    def test_filter_should_ignore_non_health_requests(self):
        record = Mock()
        record.request = "GET http://10.32.3.15:7000/articles"

        result = self.health_filter_class.filter(record)
        assert result is True
